#!/usr/bin/env python3
"""
Route module for the API
"""
# Import necessary modules
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None


# Check the value of AUTH_TYPE and initialize auth variable accordingly
if getenv("AUTH_TYPE") == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv("AUTH_TYPE") == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif getenv("AUTH_TYPE") == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif getenv("AUTH_TYPE") == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def request_filter() -> None:
    """ Checks if request needs authorization
    """
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    # Check if authentication is required for the requested path
    if auth and auth.require_auth(request.path, excluded_paths):
        # Check if authorization header is present
        if auth.authorization_header(request) is None and auth.session_cookie(
                request) is None:
            abort(401)
        # Check if current user is authorized
        if auth.current_user(request) is None:
            abort(403)
        request.current_user = auth.current_user(request)


# Define an error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 Not Found errors
    """
    return jsonify({"error": "Not found"}), 404

# Define an error handler for 401 Unauthorized errors


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles 401 Unauthorized errors
    """
    return jsonify({"error": "Unauthorized"}), 401


# Define an error handler for 403 Forbidden errors
@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles 403 Forbidden errors
    """
    return jsonify({"error": "Forbidden"}), 403


# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    '''Read API_HOST and API_PORT from environment
    variables or use default values
    '''
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    # Start the Flask application
    app.run(host=host, port=port)
