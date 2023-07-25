#!/usr/bin/python3
""" view for review objects that handles all default restful api actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """retrieves all reviews from place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
        
    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
    """ Retrieves a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ deletes a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(review_id):
    """ method for creating a review """
    if not request.is_json:
        abort(400, "Not a JSON")
        
    data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    place_id = data["place_id"]
    new_review = Review(**data)
    storage.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id)
    """ method that updates a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ('id', 'user_id', 'place_id', 'created_at', 'updated_at'):
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())