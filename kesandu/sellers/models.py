from datetime import datetime 
from hashlib import md5
from time import time
from flask import current_app 
from kesandu import db, login
from sqlalchemy import Column, ForeignKey, Table
from kesandu.system.models import User as baseUser


class Seller(baseUser):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(125), nullable=False)
    lastName = db.Column(db.String(125), nullable=False) 
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(25), nullable = False)
    address = db.Column(db.Text(), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20),  nullable=False)
    confirmCode = db.Column(db.String(10), nullable=False)
    # product_id = Column(INTEGER(11), db.ForeignKey('products.id'), nullable=True)
    # product = db.relationship('Product', backref='products', lazy=True)
    
    
    def __repr__(self):
        return '<Seller {}>'.format(self.username) 