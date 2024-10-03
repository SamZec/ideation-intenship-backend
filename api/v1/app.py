#!/bin/python3
"""Flask application server module"""
from flask_cors import CORS
from models import storage
from flasgger import Swagger
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {'title': 'IDEATION API DESIGN', 'uiversion': 3}
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

Swagger(app)
storage.connect()

@app.errorhandler(405)
def not_allowed(error):
    """405 error handler"""
    return jsonify({
        'error': 405,
        'description': error.description
        })


@app.errorhandler(500)
def sever_error(error):
    """500 error handler"""
    return jsonify({
        'error': 500,
        'description': error.description
        })


@app.errorhandler(400)
def bad_request(error):
    """400 error hadler"""
    return jsonify({
        'error': 400,
        'description': error.description
        })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'error': 404,
        'description': error.description
        })


if __name__ == '__main__':
    app.run(debug=True)
