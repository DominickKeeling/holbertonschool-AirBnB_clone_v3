#!/usr/bin/python3
""" routing index file """

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns a status as json"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def count():
    """ Returns number of each objects by type as json """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
