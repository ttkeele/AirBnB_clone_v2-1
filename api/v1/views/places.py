#!/usr/bin/python3
"""
Flask route for places
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_in_city(city_id):
    """
    place routes
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)

    if request.method == 'GET':
        all_places = storage.all('Place')
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404)
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        storage.new(new_object)
        storage.save()
        return jsonify(new_object.to_dict()), 201
