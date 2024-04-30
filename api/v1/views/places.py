#!/usr/bin/python3
"""
create states route
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_place(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    if not storage.get(City, city_id):
        abort(404)
    else:
        places = storage.all(Place).values()
        associated_place_list = [
            place.to_dict() for place in places if place.city_id == city_id
        ]
        return jsonify(associated_place_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    get place from id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    delete Place from id
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
)
def create_place(city_id):
    """
    create place
    """
    if not storage.get(City, city_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()

    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')

    if not storage.get(User, kwargs("user_id")):
        abort(404)

    if 'name' not in kwargs:
        abort(400, 'Missing name')
    kwargs["city_id"] = city_id
    place = Place(**kwargs)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    update place
    """
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
