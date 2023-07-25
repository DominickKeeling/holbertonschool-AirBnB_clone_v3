#!/usr/bin/python3
""" Starts a web flask application """
from models import storage
from flask import Flask, make_response
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(self):
    """ Closes Current Session """
    storage.close()


@app.errorhandler(404)
def it_borked(error):
    """ Handles 404 errors and returns a JSON 404 status code """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default=5000)

    app.run(hosts=host, ports=port, threaded=True)
