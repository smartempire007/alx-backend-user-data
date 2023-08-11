#!/usr/bin/env python3
""" 
Module of Session Auth

This module contains the implementation of session-based authentication endpoints.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    """ 
    Logout a user session

    This endpoint handles the deletion of a user session by sending a
    DELETE request to '/api/v1/auth_session/logout'.

    Args:
        None

    JSON body:
        - session id

    Returns:
        - Empty JSON response

    Raises:
        404 error if the session cannot be destroyed
    """
    from api.v1.app import auth

    logout = auth.destroy_session(request)
    if not logout:
        abort(404)

    return jsonify({}), 200


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ 
    Login a user with session authentication

    This endpoint handles the authentication and login process
    for a user using session-based authentication
    by sending a POST request to '/api/v1/auth_session/login'.

    Args:
        None

    JSON body:
        - email: The email address of the user
        - password: The password of the user

    Returns:
        - JSON representation of the authenticated User object

    Raises:
        400 error if the email or password is missing
        404 error if no user is found for the provided email
        401 error if the password is incorrect
    """

    user_email = request.form.get('email')
    user_pswd = request.form.get('password')

    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pswd:
        return jsonify({"error": "password missing"}), 400

    try:
        search_users = User.search({'email': user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not search_users:
        return jsonify({"error": "no user found for this email"}), 404

    user = search_users[0]
    if not user.is_valid_password(user_pswd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_cookie = getenv("SESSION_NAME")
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(session_cookie, session_id)

    return response
