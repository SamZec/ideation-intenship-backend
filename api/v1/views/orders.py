#!/bin/python3
"""product views module"""
from models.users import User
from api.v1.views import app_views
from models.products import Product
from models.orders import Order
from flasgger.utils import swag_from
from flask import jsonify, abort, request
from api.v1.views.pipelines import get_orders


@app_views.route('/orders', strict_slashes=False)
@swag_from('documentation/orders/get_orders.yml')
def orders():
    """lists all orders"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    sort = request.args.get('sort')
    start = (page - 1) * limit
    end = start + limit
    try:
        response = None
        if sort:
            response = Order.sort(sort)
        else:
            response = Order.all()
        if response:
            remainig = len(response) - end
            return jsonify({
                'orders': response[start:end],
                'total': len(response),
                'next': remainig if remainig >= 0 else 0,
                'status': 'ok'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'orders not found')


@app_views.route('/orders/<order_id>', strict_slashes=False)
@swag_from('documentation/orders/get_order.yml')
def get_order(order_id):
    """get order by id"""
    try:
        order = Order.objects(id=order_id).first()
        if order:
            return jsonify({'order': order.to_dict(),
                'status': 'oik'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'order not found')


@app_views.route('/orders', methods=['POST'], strict_slashes=False)
@swag_from('documentation/orders/create_order.yml')
def create_order():
    """create new order"""
    data = {}
    if request.is_json:
         data = request.get_json()

    user_id = data.get('user_id', request.form.get('user_id'))
    if not user_id:
        abort(400, 'user id required')

    products = data.get('products', request.form.get('products'))
    if not products:
        abort(400, 'products required')
    if type(products) is not str and type(products) is not list:
        abort(400, 'product must be a string or list of products')
    if type(products) is str:
        products = products.split(',')
    try:
        order = Order().add(user_id, products)
        data = order.to_dict()
    except Exception as e:
        abort(500, str(e))
    return jsonify({
        'msg': 'product created',
        'details': data,
        'status': 'ok'
        }), 201


@app_views.route('/orders/<order_id>', methods=['DELETE'],
        strict_slashes=False)
@swag_from('documentation/orders/delete_order.yml')
def delete_order(order_id):
    """remove order from database"""
    try:
        order = Order.objects(id=order_id).first()
        if order:
            order.delete()
            return jsonify({
                'msg': 'delete successful',
                'status': 'ok'
                })
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'order not found')
