#!/bin/python3
"""init file for defining API blueprint"""
from flask import Blueprint
from models import storage


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
@app_views.teardown_app_request
def close(f):
    storage.disconnect()
from api.v1.views.status import *
from api.v1.views.users import *
from api.v1.views.products import *
from api.v1.views.orders import *
