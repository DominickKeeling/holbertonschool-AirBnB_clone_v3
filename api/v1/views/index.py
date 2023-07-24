#!/usr/bin/python3
"""
Not sure whats happening here
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    classes = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    stats = {}
    for cls in classes:
        stats[cls] = storage.count(cls)
    return jsonify(stats)