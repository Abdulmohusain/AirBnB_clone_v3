#!/usr/bin/python3
"""
create flask app, app_views
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """

    """
    response = {'status' : 'OK'}
    return jsonify(response)