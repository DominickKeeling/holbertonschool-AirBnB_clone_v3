#!/usr/bin/python3
"""
Starts a web flask application
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

# Creating Flask app instance
app = Flask(__name__)

# Registers the app_view blueprint
app.register_blueprint(app_views)

# Declaring a method handler app teardown that closes the storage
@app.teardown_appcontext
def teardown_app(self):
    """ Method to handle app teardown """
    storage.close()


@app.errorhandler(404)
def it_borked(error):
    """ Handles 404 errors and returns a JSON 404 status code """
    return make_response(jsonify({"error": "Not found"}), 404)
    

# This starts the Flask application
if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
