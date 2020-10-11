import os
from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.initialize import initialize
from api.list_reviews import list_reviews as do_list_reviews  
from api.get_review import get_review as do_get_reviews
from api.update_review import update_review as do_update_reviews  

# Initialize Database
if os.environ['CONNECTION_STRING'] is None:
    raise Exception("Missing environment variable 'CONNECTION_STRING'")
initialize(os.environ['CONNECTION_STRING'])

# Initalize flask service
app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home():
    return """
<html><body>
    <h1>Reviews</h1>
    <ul>
        <li>GET /reviews - List reviews</li>
        <li>GET /reviews/<review_id> - Get a specific review</li>
        <li>PUT /reviews/<review_id> - Update a specific review</li>
    </ul>
</body></html>
"""

@app.route("/reviews", methods=['GET'])
def listReviews(): return do_list_reviews()

@app.route("/reviews/<review_id>", methods=['GET'])
def getReview(review_id): return do_get_reviews(review_id)
    
@app.route("/reviews/<review_id>", methods=['PUT'])
def updateReview(review_id): return do_update_reviews(review_id)