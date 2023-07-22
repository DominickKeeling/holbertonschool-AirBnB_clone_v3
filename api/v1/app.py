#!/usr/bin/python3
"""
Starts a web flask application
"""

from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontex
def teardown_app():
    """ Method to handle app teardown """
    storage.close()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)