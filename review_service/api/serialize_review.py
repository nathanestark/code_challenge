from database.models.review import Review

# The API's JSON properties may be different than the DB properties
# translate between them

def serialize_review(review, is_favorite=False):
    ret = {
        'id': review.review_id,
        'userId': review.user_id,
        'businessId': review.business_id,
        'stars': review.stars,
        'useful': review.useful,
        'funny': review.funny,
        'cool': review.cool,
        'text': review.text,
        'date': review.date.isoformat() + "Z", #ISO8601 format for timestamp transmission over the wire
        'continuationToken': review.continuation_token 
    }
    if is_favorite: ret['isFavorite'] = True
    return ret