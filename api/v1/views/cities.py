#!/usr/bin/python3
"""
create states route
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    if not storage.get(State, state_id):
        abort(404)
    else:
        cities = storage.all(City).values()
        associated_city_list = [
            city.to_dict() for city in cities if city.state_id == state_id
        ]
        return jsonify(associated_city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """
    get city from id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    delete state from id
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>/cities',
        methods=['POST'],
        strict_slashes=False
)
def create_city(state_id):
    """
    create city
    """
    if not storage.get(State, state_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, 'Missing name')

    setattr(kwargs, "state_id", state_id)
    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update city
    """
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
