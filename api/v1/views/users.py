#!/usr/bin/python3
"""users routes"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """routes for users"""
    if request.method == 'GET':
        res = []
        for user in storage.all(User).values():
            res.append(user.to_dict())
        return jsonify(res)
    elif request.method == 'POST':
        user_dict = request.get_json()
        if not user_dict:
            abort(400, "Not a JSON")
        if 'name' not in user_dict.keys():
            abort(400, "Missing name")
        if 'email' not in user_dict.keys():
            abort(400, "Missing email")
        if 'password' not in user_dict.keys():
            abort(400, "Missing password")
        user = User(**user_dict)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
