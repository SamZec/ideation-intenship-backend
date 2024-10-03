#!/bin/python3
"""module for mongodb aggregation pipelines"""

get_users = [
        {'$project': {
            '_id': 0,
            'id': {'$toString': '$_id'},
            'first_name': '$first_name',
            'last_name': '$last_name',
            'email': '$email',
            'phone': '$phone'
            }
        }
    ]


get_products = [
        {'$project': {
            '_id': 0,
            'id': {'$toString': '$_id'},
            'name': '$name',
            'price': '$price',
            'category': '$category'
            }
        }
    ]


get_products = [
        {'$project': {
            '_id': 0,
            'id': {'$toString': '$_id'},
            'name': '$name',
            'price': '$price',
            'category': '$category'
            }
        }
    ]


get_orders = [
        {'$project': {
            '_id': 0,
            'id': {'$toString': '$_id'},
            'name': '$name',
            'price': '$price',
            'category': '$category'
            }
        }
    ]

