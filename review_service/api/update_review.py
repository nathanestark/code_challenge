from flask import abort, request, jsonify

from api.serialize_review import serialize_review

from database.initialize import get_session
from database.models.review import Review
from database.models.favorite import Favorite

def update_review(review_id):

    # For now, the only property they can update is isFavorite
    body = request.json
    if body is not None and 'isFavorite' in body:
        if not isinstance(body['isFavorite'], bool):
            abort(400, "Property 'isFavorite' must be a boolean")

        try:
            session = get_session()

            result = session.query(
                Review,
                Favorite,
            ).join(
                Favorite, Favorite.review_id == Review.id, isouter=True
            ).filter(
                Review.review_id == review_id
            ).first()

            # Has to exist.
            if result is None:
                abort(404, "Review '"+ review_id +"' does not exist")

            review = result[0]
            favorite = result[1]
            db_is_favorite = favorite is not None

            # If the favorite conditions don't match, update it.
            if db_is_favorite != body['isFavorite']:
                if body['isFavorite']:
                    # Insert a new row to favorites.
                    session.add(Favorite(review_id=review.id))
                else:
                    # Delete existing row in favorites.
                    session.delete(favorite)

                session.commit()

            return serialize_review(review, body['isFavorite'])
        except:
            session.rollback()
            raise
        finally:
            session.close()

    else:
        # If there is nothing to update, this acts as a get.
        try:
            session = get_session()

            result = session.query(
                Review,
                (Favorite.review_id).label('is_favorite'),
            ).join(
                Favorite, Favorite.review_id == Review.id, isouter=True
            ).filter(
                Review.review_id == review_id
            ).first()
            
            review = result[0]
            isFavorite = result[1] == True

            # Has to exist.
            if review is None:
                abort(404, "Review '"+ review_id +"' does not exist")

            return serialize_review(review, isFavorite)
        except:
            session.rollback()
            raise
        finally:
            session.close()
