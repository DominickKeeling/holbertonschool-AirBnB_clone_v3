#!/usr/bin/python3
""" view for state that handles all default api actions """

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


# Route to get all states
@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """method retrieves list of all State objects in JSON format"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


# route to get the state id
@app_views.route("states/<state_id>", methods=['GET'], strict_slashes=False)
def state(state_id):
    """ this method obtains the state object in json format"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


# Route to delete a state
@app_views.route("states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """method for deleting state objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


# Route to add a new state
@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """ method creates a new state object """
    # checking to see if the incoming request is in json format
    if not request.is_json:
        abort(400, 'Request is not in JSON format')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing "name" field')

    new_state = State(name=data['name'])
    new_state.save()

    return jsonify(new_state.to_dict()), 201


# Route to update an existing state by ID
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Method updates an existing State object"""

    # Get the existing state object based on the provided state_id
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Request is not in JSON format')

    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing "name" field')

    ignore_attributes = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_attributes:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
