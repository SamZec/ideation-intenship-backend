#!/bin/python3
"""storage ,odule for difining storage class"""
from mongoengine import connect


class Storage():
    """storage object class"""
    def connect(self):
        """connect to mongodb databse"""
        connect('IDEATION_API')
