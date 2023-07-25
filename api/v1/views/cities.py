#!/usr/bin/python3
""" view for state that handles all default api actions """

from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views
from models.state import State


# Route to get all cities of a state
@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all cities objects of a State or city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


# route to get the city id
@app_views.route("cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ this method obtains the cities object in json format"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())
    

# Route to delete a city
@app_views.route("cities/<city_id>", methods=['GET'], strict_slashes=False)
def delete_city(city_id):
    """method for deleting a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    

# Route to add a new city under its state
@app_views.route("/states/state_id/cities", methods=['DELETE'], strict_slashes=False)
def post_city(state_id):
    """ method creates a new city """
    # checking to see if the incoming request is in json format
    if not request.is_json:
        abort(400, 'Request is not in JSON format')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing "name" field')
        
    new_city = City(name=data['name'])
    new_city.save()

    return jsonify(new_city.to_dict()), 201


# Route to update an existing city
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Method updates an existing city"""

    # Get the existing city based on the provided city_id
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Request is not in JSON format')

    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing "name" field')

    ignore_attributes = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_attributes:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
