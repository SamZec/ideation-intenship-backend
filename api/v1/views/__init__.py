#!/bin/python3
"""init file for defining API blueprint"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.status import *
from api.v1.views.users import *
from api.v1.views.products import *
from api.v1.views.orders import *
