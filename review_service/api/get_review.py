from flask import abort, request, jsonify

from api.serialize_review import serialize_review

from database.initialize import get_session
from database.models.review import Review
from database.models.favorite import Favorite

def get_review(review_id):
    session = get_session()
    try:
        review = session.query(
            Review,
            (Favorite.review_id).label('is_favorite')
        ).join(
            Favorite, Favorite.review_id == Review.id, isouter=True
        ).filter(
            Review.review_id == review_id
        ).first()

        # Has to exist.
        if review is None:
            abort(404, "Review '"+ review_id +"' does not exist")

        return jsonify(serialize_review(review[0], review[1]))
    except:
        session.rollback()
        raise
    finally:
        session.close()
