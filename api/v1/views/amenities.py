#!/usr/bin/python3
""" view for amenity objects that handles all default restful api actions"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


# Route to get all amenities
@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenity objects"""
    amenities = storage.get(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])

# route to get the amenity by id
@app_views.route("amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """ this method obtains the amenity object in json format"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())
    

# Route to delete a amenity
@app_views.route("amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def delete_amenity(amenity_id):
    """method for deleting amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    

# Route to add a new amenity
@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """ method creates a new amenity object """
    # checking to see if the incoming request is in json format
    if not request.is_json:
        abort(400, 'Request is not in JSON format')

    data = request.get_json
    if 'name' not in data:
        abort(400, 'Missing "name" field')
        
    new_amenity = Amenity(name=data['name'])
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


# Route to update an existing amenity by ID
@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Method updates an existing Amenity object"""

    # Get the existing amenity object based on the provided amenity_id
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Request is not in JSON format')

    data = request.get_json
    if 'name' not in data:
        return abort(400, 'Missing "name" field')

    ignore_attributes = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_attributes:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict())