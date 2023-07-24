#!/usr/bin/python3
""" Init file """

from flask import Blueprint


# Creating a blueprint instance for API 
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# importing everything from index
from api.v1.views.index import *
from api.v1.views.states import *