#!/bin/python3
"""storage ,odule for difining storage class"""
import os
from mongoengine import connect, disconnect


class Storage():
    """storage object class"""
    def connect(self):
        """connect to mongodb databse"""
        if os.getenv('local'):
            connect('IDEATION_API')
        else:
            connect(host=os.getenv('DB_URI'), db='IDEATION_API')

    def disconnect(self):
        """close connection"""
        disconnect()
