#!/bin/python3
"""user views module"""
from models.users import User
from models.orders import Order
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import jsonify, abort, request
from api.v1.views.pipelines import get_users


@app_views.route('/users', strict_slashes=False)
@swag_from('documentation/users/get_users.yml')
def get():
    """lists all users"""
    try:
        cursor = User.objects.aggregate(get_users)
        response = list(cursor)
        if response:
            return jsonify({
                'users': response,
                'status': 'ok'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'users not found')

@app_views.route('/users/<user_id>', strict_slashes=False)
@swag_from('documentation/users/get_user.yml')
def get_user(user_id):
    """get user by id"""
    try:
        match = {'$match':
                {'$expr': {'$eq': ['$_id', {'$toObjectId': user_id}]}}}
        get_users.insert(0, match)
        cursor = User.objects.aggregate(get_users)
        del get_users[0]
        response = list(cursor)
        if response:
            return jsonify({'user': response[0],
                'status': 'ok'})
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'user not found')


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/users/create_user.yml')
def create():
    """create new user"""
    data = {}
    if request.is_json:
         data = request.get_json()

    first_name = data.get('first_name', request.form.get('first_name'))
    if not first_name:
        abort(400, 'first name required')

    last_name = data.get('last_name', request.form.get('last_name'))
    email = data.get('email', request.form.get('email'))
    if not email:
        abort(400, 'email required')

    phone = data.get('phone', request.form.get('phone'))
    if not phone:
        abort(400, 'phone number required')
    user_exits = User.objects(email=email).first()
    if user_exits:
        abort(400, 'email already exist')
    try:
        user = User(**data).save()
        data['id'] = str(user.id)
    except Exception as e:
        abort(500, str(e))
    return jsonify({
        'msg': 'user created',
        'details': data,
        'status': 'ok'
        }), 201


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/users/delete_user.yml')
def delete(user_id):
    """remove user from database"""
    try:
        user = User.objects(id=user_id).first()
        if user:
            user.delete()
        return jsonify({
            'msg': 'delete successful',
            'status': 'ok'
            })
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'user not found')


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/users/update_user.yml')
def update(user_id):
    """update user details"""
    user = User.objects(id=user_id).first()
    if not user:
        abort(404, 'user not found')
    data = {}
    update = {}
    if request.is_json:
        data = request.get_json()
    email = data.get('email', request.form.get('email'))
    if email:
        update['email'] = email
    phone = data.get('phone', request.form.get('phone'))
    if phone:
        update['phone'] = phone
    last_name = data.get('last_name', request.form.get('last_name'))
    if last_name:
        update['last_name'] = last_name
    first_name = data.get('first_name', request.form.get('first_name'))
    if first_name:
        update['first_name'] = first_name
    try:
        update_user = user.update(**update)
        match = {'$match':
                {'$expr': {'$eq': ['$_id', {'$toObjectId': update_user}]}}}
        get_users.insert(0, match)
        cursor = User.objects.aggregate(get_users)
        del get_users[0]
        return jsonify({
            'details': list(cursor),
            'msg': 'update successful'})
    except Exception as e:
        return abort(500, str(e))


@app_views.route('/users/<user_id>/orders', strict_slashes=False)
@swag_from('documentation/users/get_user_orders.yml')
def get_user_order(user_id):
    """get user orders"""
    try:
        orders = Order.all(user_id)
        if orders:
            return jsonify({
                'orders': orders,
                'status': 'ok'
                })
    except Exception as e:
        abort(500, str(e))
    return abort(404, 'orders not found')

