#!/usr/bin/env python3
"""20. End-to-end integration test"""
import requests

base_url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Tests User Registration endpoint"""
    r = requests.post(base_url + '/users',
                      data={"email": email,
                            "password": password})
    data = r.json()
    assert data == {"email": email,
                    "message": "user created"}
    assert r.status_code == 201

    r = requests.post(base_url + '/users',
                      data={"email": email,
                            "password": password})
    data = r.json()
    assert data == {"message": "email already registered"}
    assert r.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests Login URI with wrong credentials"""
    r = requests.post(base_url + '/sessions',
                      data={"email": email,
                            "password": password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests Login URI with correct credentials"""
    r = requests.post(base_url + '/sessions',
                      data={"email": email,
                            "password": password})
    data = r.json()
    assert data == {"email": email, "message": "logged in"}
    assert 'session_id' in r.cookies
    assert r.cookies.get('session_id') is not None
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test profile URI without session_id"""
    r = requests.get(base_url + '/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile URI with session_id"""
    headers = {'Cookie': 'session_id=' + session_id}
    r = requests.get(base_url + '/profile', headers=headers)
    data = r.json()
    assert 'email' in data
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """Test User logout URI with session_id"""
    headers = {'Cookie': 'session_id=' + session_id}
    r = requests.delete(base_url + '/sessions', headers=headers)

    assert len(r.history) != 0
    assert r.history[0].is_redirect
    assert r.history[0].status_code == 302
    data = r.json()
    assert data == {'message': 'Bienvenue'}
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """Test reset_password POST URI using email"""
    r = requests.post(base_url + '/reset_password',
                      data={"email": email})
    data = r.json()
    assert r.status_code == 200
    assert all(['email' in data, 'reset_token' in data])
    return data.get('reset_token')


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Test reset_password PUT URI using all required creden..."""
    r = requests.put(base_url + '/reset_password',
                     data={"email": email,
                           "reset_token": reset_token,
                           "new_password": new_password})
    data = r.json()
    assert r.status_code == 200
    assert all(['email' in data, 'message' in data])
    assert data == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
