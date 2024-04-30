#!/usr/bin/python3
"""
create new flask app
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resource={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(status_code=None):
    """closes the db session by calling .close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HOST, port=PORT, threaded=True)
