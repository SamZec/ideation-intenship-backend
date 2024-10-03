#!/bin/python3
"""orders module for order class definition"""
from datetime import datetime
from models.users import User
from models.products import Product
from mongoengine import Document, StringField, ListField
from mongoengine import DateTimeField, DecimalField, ReferenceField


class Order(Document):
    """class for defining order objects"""
    user = ReferenceField('User', reverse_delete_rule=2, required=True)
    products = ListField(ReferenceField('Product'), required=True)
    total = DecimalField(required=True)
    date = DateTimeField(defaults=datetime.now())

    meta = {'collection': 'orders'}

    @classmethod
    def all(cls, user_id=None):
        """get all orders in dict notation"""
        if user_id:
            return [i.to_dict() for i in cls.objects(user=user_id)]
        return [i.to_dict() for i in cls.objects()]

    @classmethod
    def sort(cls, sort):
        """sorts the results by 'sort' """
        if not sort:
            raise AttributeError('sort missing one argument "sort"')
        orders = cls.objects().order_by(sort)
        if orders:
            return [i.to_dict() for i in orders]
        return []


    def add(self, user_id, products):
        """create new order"""
        if not products:
            raise AttributeError("products can't be empty")
        if type(products) is not list and type(products) is not str:
            raise AttributeError('products must be string or list')
        user = User.objects(id=user_id).first()
        if not user:
            raise AttributeError("user doesn't exists")
        if type(products) is str:
            product = products.title()
            product_obj = Product.objects(name=product).first()
            if not product_obj:
                raise AttributeError(f"product {products} does not exists")
            self.user = user
            self.products.append(product_obj)
            self.total = product_obj.price
            self.date = datetime.now()
            self.save()
            return self
        list_product = []
        total = 0.0
        for product in products:
            product = product.title()
            product_obj = Product.objects(name=product).first()
            if not product_obj:
                raise AttributeError(f"product {product} does not exists")
            total += float(product_obj.price)
            list_product.append(product_obj)
        self.user = user
        self.products = list_product
        self.total = total
        self.date = datetime.now()
        self.save()
        return self

    def to_dict(self):
        """json notation of object"""
        return {
                'id': str(self.id),
                'user_id': str(self.user.id),
                'products': [i.name for i in self.products],
                'total': float(self.total),
                'date': self.date.strftime("%d-%b-%Y, %H:%M:%S")
                }
