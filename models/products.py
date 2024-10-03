#!/bin/python3
"""product module for product class definition"""
from mongoengine import Document, StringField, DecimalField


class Product(Document):
    """class for defining product objects"""
    name = StringField(required=True)
    price = DecimalField(required=True)
    category = StringField(required=True)

    meta = {'collection': 'products'}

    def update(self, **data):
        """upadte user with data"""
        if not data or not all(hasattr(self, i) for i in data.keys()):
            raise AttributeError('invalid attributes')
        for key, value in data.items():
            if not value:
                continue
            setattr(self, key, value)
        self.save()
        return self.id
