#!/usr/bin/env python3
"""Flask application
"""

from flask import Flask, jsonify, request, make_response, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
