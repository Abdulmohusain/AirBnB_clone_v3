#!/usr/bin/python3
"""
create states route
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Place objects of a City
    """
    if not storage.get(Place, place_id):
        abort(404)
    else:
        reviews = storage.all(Review).values()
        associated_review_list = [
            review.to_dict() for review in reviews if review.place_id == place_id
        ]
        return jsonify(associated_review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """
    get Review from id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    delete review from id
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
)
def create_review(place_id):
    """
    create review
    """
    if not storage.get(Place, place_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()

    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')

    if not storage.get(User, kwargs["user_id"]):
        abort(404)

    if 'text' not in kwargs:
        abort(400, 'Missing text')
    kwargs["place_id"] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update review
    """
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
