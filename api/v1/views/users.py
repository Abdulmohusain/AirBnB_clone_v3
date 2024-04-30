#!/usr/bin/python3
"""
create states route
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_users():
    """
    get all amenities
    """
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """
    get user from id
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    delete user from id
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    create user
    """
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400, "Not a JSON")
    kwargs = request.get_json()

    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
        '/users/<user_id>',
        methods=['PUT'],
        strict_slashes=False
)
def update_user(user_id):
    """
    update user
    """
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
