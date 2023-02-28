#!/usr/bin/env python3
"""Flask application
"""

from flask import Flask, jsonify, request
from flask import make_response, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """Index Route
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def users():
    """Users Endpoint
    """
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Sessions Endpoint
    """
    email = request.form['email']
    password = request.form['password']
    is_valid_user = AUTH.valid_login(email, password)
    if not is_valid_user:
        abort(401)
    session = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie('session_id', session)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """DELETE Sessions Endpoint
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
def profile():
    """GET a users profile with session_id cookies set.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password_token():
    """Sessions Endpoint
    """
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def reset_password():
    """Sessions Endpoint
    """
    email = request.form['email']
    reset_token = request.form['reset_token']
    password = request.form['password']
    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
