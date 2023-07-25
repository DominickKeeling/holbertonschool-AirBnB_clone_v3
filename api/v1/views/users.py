#!/usr/bin/python3
""" view for user objects that handles all default restful api actions"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


# Route to get all users
@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all user objects"""
    users = storage.get(User)
    return jsonify([user.to_dict() for user in users.values()])

# route to get the user by id
@app_views.route("users/<user_id>", methods=['GET'], strict_slashes=False)
def user(user_id):
    """ this method obtains the user object in json format"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())
    

# Route to delete a user
@app_views.route("users/<user_id>", methods=['GET'], strict_slashes=False)
def delete_user(user_id):
    """method for deleting user objects"""
    user = storage.delete(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    

# Route to add a new user
@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """ method creates a new user object """
    # checking to see if the incoming request is in json format
    if not request.is_json:
        abort(400, 'Request is not in JSON format')

    data = request.get_json
    if 'email' not in data:
        abort(400, 'Missing email')
    
    if 'password' not in data:
       abort(400, 'Missing password')
        
    new_user = User(email=data['email'], password=data['password'])
    new_user.save()

    return jsonify(new_user.to_dict()), 201


# Route to update an existing user by ID
@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Method updates an existing User object"""

    # Get the existing user object based on the provided user_id
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')

    data = request.get_json()

    ignore_attributes = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_attributes:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict())