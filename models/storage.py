#!/bin/python3
"""storage ,odule for difining storage class"""
import os
from decouple import config
from mongoengine import connect, disconnect


class Storage():
    """storage object class"""
    def connect(self):
        """connect to mongodb databse"""
        if config('DB_URI', None): #specified enviroment connection
            connect(host=config('DB_URI'), db='IDEATION_API')

        else: #default localhost connection
            connect('IDEATION_API')

    def disconnect(self):
        """close connection"""
        disconnect()
