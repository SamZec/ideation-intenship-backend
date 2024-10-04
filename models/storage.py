#!/bin/python3
"""storage ,odule for difining storage class"""
import os
from models.config import host
from mongoengine import connect, disconnect


class Storage():
    """storage object class"""
    def connect(self):
        """connect to mongodb databse"""
        if os.getenv('local'):
            connect('IDEATION_API')
        else:
            connect(host=host, db='IDEATION_API')

    def disconnect(self):
        """close connection"""
        disconnect()
