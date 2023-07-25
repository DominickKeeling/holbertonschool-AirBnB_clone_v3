#!/usr/bin/python3
""" view for user objects that handles all default restful api actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User 


# Route to get all Place by city
@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_place(city_id):
    """Retrieves the list of all place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places.values()])

# route to get the place by id
@app_views.route("places/<place_id>", methods=['GET'], strict_slashes=False)
def place(place_id):
    """ this method obtains the place object in json format"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())
    

# Route to delete a Place
@app_views.route("places/<place_id>", methods=['GET'], strict_slashes=False)
def delete_place(place_id):
    """method for deleting place objects"""
    place = storage.delete(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    

# Route to add a new place
@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ method creates a new place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # checking to see if the incoming request is in json format
    if not request.is_json:
        abort(400, 'Request is not in JSON format')

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    user = storage.get(User, data'[user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    
    new_place = Place(name=data['name'], city_id=city_id, user_id=data['user_id'])
    storage.save()

    return jsonify(new_place.to_dict()), 201


# Route to update an existing place by ID
@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Method updates an existing Place object"""

    # Get the existing user object based on the provided user_id
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')

    data = request.get_json()

    ignore_attributes = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_attributes:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
 
