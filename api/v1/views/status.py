#!/bin/python3
"""API staus module"""
from flask import jsonify
from api.v1.views import app_views
from flasgger.utils import swag_from


@app_views.route('/status', strict_slashes=False)
@swag_from('documentation/status/status.yml')
def status():
    """return the status of the API"""
    return jsonify({
        'project': 'API DESIGN AND DEVELOPMENT',
        'assigner': 'IDEATION AXIS',
        'assignee': 'AFFUM SAMUEL',
        'status': 'OK'
        })
