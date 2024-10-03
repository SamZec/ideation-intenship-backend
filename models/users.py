#!/bin/python3
"""user module for handling user class definition"""
from mongoengine import Document, StringField


class User(Document):
    """User objects class definition"""
    first_name = StringField(required=True)
    last_name = StringField()
    email = StringField(required=True)
    phone = StringField(required=True)

    meta = {'collection': 'users'}

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

