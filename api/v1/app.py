#!/usr/bin/python3
"""
Starts a web flask application
"""

from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app():
    """ Method to handle app teardown """
    storage.close()


@app.errorhandler(404)
def it_borked(error):
    """ Handles 404 errors and returns a JSON 404 status code """
    return jsonify({"error": "Not found"}), 404

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
