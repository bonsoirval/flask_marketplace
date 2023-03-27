from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from kesandu import db, login
from sqlalchemy import Column, ForeignKey, Integer
from flask_authorize import RestrictionsMixin, AllowancesMixin
from sqlalchemy.dialects.mysql import TINYINT, DATE,DECIMAL, SMALLINT, FLOAT, TEXT,INTEGER, VARCHAR, FLOAT, DECIMAL, CHAR, DOUBLE, ENUM,   DATETIME
from kesandu.models import UserGroup, UserRole


class Seller(db.Model, UserMixin):
    __tablename__ = 'sellers'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, default='bonsoirval@gmail.com')
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

    # roles and groups are reserved words that *must* be defined
    # on the User model to use group- or role-based authorization.
    # roles = db.relationship('Role', secondary=UserRole)
    # groups = db.relationship('Group', secondary=UserGroup)

    
    def __repr__(self):
        return '<Seller {}>'.format(self.username)  
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def seller_id():
        return Seller.query.get(int(id))
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Seller.query.get(int(id))
       
    

@login.user_loader
def load_user(id):
    return Seller.query.get(int(id))


# class category(db.Model):
#     id = Column(INTEGER(11),  primary_key = True, nullable = False)
#     image = Column(VARCHAR(255), nullable = True)
#     parent_id  = Column(INTEGER(11),  nullable = False, default= '0')
#     top  = Column(TINYINT(1), nullable = False)
#     column  = Column(INTEGER(3), nullable = False)
#     sort_order  = Column(INTEGER(3), nullable = False, default= '0')
#     status  = Column(TINYINT(1), nullable = False)
#     date_added = Column(DATETIME, nullable = False)
#     date_modified  = Column(DATETIME, nullable = False)

# class category_description(db.Model):
#     id  = Column(INTEGER(11),  nullable = False)
#     language_id  = Column(INTEGER(11),  nullable = False)
#     name  = Column(VARCHAR(255), nullable = False)
#     description  = Column(TEXT, nullable = False)
#     meta_title  = Column(VARCHAR(255), nullable = False)
#     meta_description  = Column(VARCHAR(255), nullable = False)
#     meta_keyword  = Column(VARCHAR(255), nullable = False)


# class category_filter(db.Model):
#     id = Column(INTEGER(11), primary_key = True, nullable = False)
#     filter_id = Column(INTEGER(11),  nullable = False)

# class category_path(db.Model):
#     id = Column(INTEGER(11), primary_key= True, nullable = False)
#     path_id = Column(INTEGER(11),  nullable = False)
#     level = Column(INTEGER(11),  nullable = False)

# class category_to_google_product_category(db.Model):
#     google_product_category = Column(VARCHAR(10), nullable = False)
#     store_id = Column(INTEGER(11),  nullable = False, default= '0')
#     category_id = Column(INTEGER(11),  nullable = False)

# class category_to_layout(db.Model):
#     id = Column(INTEGER(11),  nullable = False)
#     store_id = Column(INTEGER(11),  nullable = False)
#     layout_id = Column(INTEGER(11),  nullable = False)

# class category_to_store(db.Model):
#     id = Column(INTEGER(11),  primary_key = True, nullable = False)
#     store_id = Column(INTEGER(11), nullable = False)


# class country(db.Model):
#     id = Column(INTEGER(11), primary_key=True,  nullable = False)
#     name = Column(VARCHAR(128), nullable = False)
#     iso_code_2 = Column(VARCHAR(2), nullable = False)
#     iso_code_3 = Column(VARCHAR(3), nullable = False)
#     address_format = Column(TEXT, nullable = False)
#     postcode_required = Column(TINYINT(1), nullable = False)
#     status = Column(TINYINT(1), nullable = False, default= '1')
