from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from database.models.review import Review

Base = declarative_base()


# For now, Favorites and Reviews are one-to-one. # This is due to 'Favorites'
# starting out very basic. However, once user identity is implemented, 
# Favorites will of course be owned by individual users, normalizing them
# into the Reviews table would be inappropriately. So we'll start out
# assuming that that is the clear direction, and keep them separate,
# and make the relationship one-to-man (relationship-to-favorites).

class Favorite(Base):
    __tablename__='favorites'

    id = Column(Integer, primary_key=True)
    review_id = Column(String(32), ForeignKey(Review.id))
    