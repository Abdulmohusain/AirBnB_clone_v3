#!/usr/bin/python3
"""
creating flask routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    """
    Status route
    """
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """
    Stats route
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count('City'),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    return jsonify(stats)
