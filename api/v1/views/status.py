#!/bin/python3
"""API staus module"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """return the status of the API"""
    return jsonify({
        'project': 'API DESIGN AND DEVELOPMENT',
        'assignee': 'IDEATION AXIS',
        'status': 'OK'
        })
