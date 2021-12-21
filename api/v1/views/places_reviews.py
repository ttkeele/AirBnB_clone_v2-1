#!/usr/bin/python3
'''reviews routes'''
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, request, abort
from models.place import Place


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def place_review(place_id):
    """ gets places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    res = []
    for review in place.reviews:
        res.append(review.to_dict())
    return jsonify(res)


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    rev_place = storage.get(Review, review_id)
    if rev_place is None:
        abort(404)
    else:
        return jsonify(rev_place.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes place"""
    review_dict = storage.get(Review, review_id)
    if review_dict is None:
        abort(404)
    else:
        storage.delete(review_dict)
        storage.save()
        return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def make_review(place_id):
    """makes review"""
    place = storage.get(Place, place_id)
    review_dict = request.get_json()
    if not place:
        abort(404)
    elif not review_dict:
        abort(400, "Not a JSON")
    elif "name" not in review_dict.keys():
        abort(400, "Missing name")
    if "text" not in review_dict.keys():
        abort(400, "Missing text")
    user_id = review_dict.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    elif storage.get('User', user_id) is None:
        abort(404)
    else:
        review = Review(**review_dict)
        review.place_id = place.id
        storage.new(review)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates place"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    else:
        for key in res:
            if key not in ['id',
                           'user_id',
                           'place_id',
                           'created_at',
                           'updated_at']:
                setattr(obj, key, res[key])
        obj.save()
        new_obj = obj.to_dict()
        return jsonify(new_obj), 200
