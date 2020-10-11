from sqlalchemy import Column, String, Integer, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Ideally this entire file should be imported for DRY purposes.
class Review(Base):
    __tablename__='reviews'

    id = Column(Integer, primary_key=True)
    review_id = Column(String(22))
    user_id = Column(String(22))
    business_id = Column(String(22))
    stars = Column(Float)
    useful = Column(Integer)
    funny = Column(Integer)
    cool = Column(Integer)
    text = Column(String)
    date = Column(TIMESTAMP)
    continuation_token = Column(String(56))