#!/usr/bin/python3
"""
routing index file
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


# route for obtaining the status of the API
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

# route for obtaining the count for all objects
@app_views.route('/stats', methods=['GET'])
def stats():
    classes = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    stats = {}
    for cls in classes:
        stats[cls] = storage.count(cls)
    return jsonify(stats)