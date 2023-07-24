#!/usr/bin/python3
"""Starts a web flask application"""

from flask import Flask
from api.v1.views import app_views
from models import storage

# Creating Flask app instance
app = Flask(__name__)

# Registers the app_view blueprint
app.register_blueprint(app_views)

# Declaring a method handler app teardown that closes the storage
@app.teardown_appcontext
def teardown_app():
    """ Method to handle app teardown """
    storage.close()
    
# This starts the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)