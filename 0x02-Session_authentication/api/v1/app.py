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
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
# from api.v1.auth.session_auth import SessionAuth


# Create Flask application instance
app = Flask(__name__)

# Register blueprints for API views
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for API routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication variable
auth = None

# Read AUTH_TYPE from environment variable
AUTH_TYPE = os.getenv("AUTH_TYPE")

# Check the value of AUTH_TYPE and initialize auth variable accordingly
if AUTH_TYPE == 'auth':
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    auth = SessionAuth()

# Define a before_request function to run before each request


@app.before_request
def before_request():
    """
    Performs pre-processing tasks before handling each request
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        excluded_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                         '/api/v1/auth_session/login/', '/api/v1/forbidden/']

        # Check if authentication is required for the requested path
        if auth.require_auth(request.path, excluded_list):
            cookie = auth.session_cookie(request)
            # Check if authorization header is present
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            # Check if current user is authorized
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')

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
