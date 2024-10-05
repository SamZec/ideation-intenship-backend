#!/bin/python3
"""product views module"""
from api.v1.views import app_views
from models.products import Product
from flasgger.utils import swag_from
from flask import jsonify, abort, request
from api.v1.views.pipelines import get_products


@app_views.route('/products', strict_slashes=False)
@swag_from('documentation/products/get_products.yml')
def all_products():
    """lists all products"""
    try:
        cursor = Product.objects.aggregate(get_products)
        response = list(cursor)
        if response:
            return jsonify({
                'products': response,
                'status': 'ok'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'products not found')


@app_views.route('/products/<product_id>', strict_slashes=False)
@swag_from('documentation/products/get_product.yml')
def get_product(product_id):
    """get product by id"""
    try:
        match = {'$match':
                {'$expr': {'$eq': ['$_id', {'$toObjectId': product_id}]}}}
        get_products.insert(0, match)
        cursor = Product.objects.aggregate(get_products)
        del get_products[0]
        response = list(cursor)
        if response:
            return jsonify({'product': response[0],
                'status': 'ok'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'product not found')


@app_views.route('/products', methods=['POST'], strict_slashes=False)
@swag_from('documentation/products/create_product.yml')
def create_product():
    """create new product"""
    data = {}
    if request.is_json:
         data = request.get_json()

    name = data.get('name', request.form.get('name'))
    if not name:
        abort(400, 'name required')

    price = data.get('price', request.form.get('price'))
    if not price:
        abort(400, 'price required')
    try:
        float(price)
    except Exception:
        abort(400, 'price must be number in two decimal place')
    category = data.get('category', request.form.get('category'))
    if not category:
        abort(400, 'category required')
    product_exits = Product.objects(name=name).first()
    if product_exits:
        abort(400, 'product already exists')
    data['name'] = name
    data['price'] = price
    data['category'] = category
    try:
        product = Product(**data).save()
        data['id'] = str(product.id)
    except Exception as e:
        abort(500, str(e))
    return jsonify({
        'msg': 'product created',
        'details': data,
        'status': 'ok'
        }), 201


@app_views.route('/products/<product_id>', methods=['DELETE'],
        strict_slashes=False)
@swag_from('documentation/products/delete_product.yml')
def delete_product(product_id):
    """remove product from database"""
    try:
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return jsonify({
                'msg': 'delete successful',
                'status': 'ok'
                })
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'product not found')


@app_views.route('/products/<product_id>', methods=['PUT'],
        strict_slashes=False)
@swag_from('documentation/products/update_product.yml')
def update_product(product_id):
    """update product details"""
    product = Product.objects(id=product_id).first()
    if not product:
        abort(404, 'user not found')
    data = {}
    if request.is_json:
        data = request.get_json()
    else:
        data['name'] = request.form.get('name')
        data['price'] = request.form.get('price')
        data['category'] = request.form.get('category')
    try:
        update_product = product.update(**data)
        match = {'$match':
                {'$expr': {'$eq': ['$_id', {'$toObjectId': update_product}]}}}
        get_products.insert(0, match)
        cursor = Product.objects.aggregate(get_products)
        del get_products[0]
        return jsonify({
            'product': list(cursor),
            'msg': 'update successful',
            'status': 'ok'})
    except Exception as e:
        return abort(500, str(e))
