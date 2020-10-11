import datetime

from flask import abort, request, jsonify

from database.initialize import get_session
from database.models.review import Review
from database.models.favorite import Favorite


def list_reviews():
    # Determine if we want special filter for favorites.
    favorites_only = 'favorites' in request.args

    # Determine if there is a continuation token.
    continuation_token = request.args.get('continuationToken')

    # Allow for an 'after' date
    before = request.args.get('before')
    # Python doesn't believe in ISO8601
    if before is not None:
        if before[-1] == 'Z': before = before[:-1]
        elif before[-6] == '+':
            if before[-6:] == '+00:00': before = before[:-6]
            else:
                abort(400, "Parameter 'before' must be in UTC")

    # Determine if there is a predefined limit, or set a default
    limit = min(1000, int(request.args.get('limit'))) if 'limit' in request.args else 1000

    session = get_session()
    try:
        query = session.query(
            Review.review_id,
            Review.stars,
            Review.date,
            Review.text,
            Review.continuation_token,
            (Favorite.review_id).label('is_favorite')
        ).join(
            Favorite, Favorite.review_id == Review.id, isouter=True
        ).order_by(
            Review.date.desc(), Review.continuation_token.desc()
        )

        if continuation_token is not None:
            query = query.filter(Review.continuation_token < continuation_token)
        elif before is not None:
            try:
                dt_before = datetime.datetime.fromisoformat(before)
            except:
                abort(400, "Parameter 'before' is an invalid ISO8601 date time")
            query = query.filter(Review.date <= dt_before)
        if favorites_only:
            query = query.filter(Favorite.review_id != None)

        query = query.limit(limit)

        def build_review_list_item(review):
            ret = {
                'id': review[0],
                'stars': review[1],
                'date': review[2].isoformat() + "Z", #ISO8601 format for timestamp transmission over the wire
                'text': review[3][:64], # For list items, only give a brief of the text.
                'continuationToken': review[4]
            }
            if review[5] is not None:
                ret['isFavorite'] = True
            return ret

        # Build list response
        return jsonify([build_review_list_item(review) for review in query])
    except:
        raise
    finally:
        session.close()
