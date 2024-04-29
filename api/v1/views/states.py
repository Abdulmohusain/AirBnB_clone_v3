#!/usr/bin/python3
"""
create states route
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_states():
    """
    get all states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
    get state from id
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    delete state from id
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    create state
    """
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(404, "Not a JSON")
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    update state
    """
    if request.content_type != "application/json":
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
