from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from kesandu import db, login
from flask_authorize import RestrictionsMixin, AllowancesMixin



class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(14), nullable=False)
    reg_time = db.Column(db.DateTime, default=datetime.utcnow)
    online = db.Column(db.String(1), nullable=False,default='0')
    activation = db.Column(db.String(3), nullable=False, default='no')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(125), nullable=False)
    lastName = db.Column(db.String(125), nullable=False) 
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(25), nullable = False)
    address = db.Column(db.Text(), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20),  nullable=False)
    confirmCode = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return '<Admin {}>'.format(self.username)    
    

class Order(db.Model):
    __tablename__='orders'
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    uid = db.Column(db.Integer, nullable=True)
    ofname = db.Column(db.Text(), nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    oplace = db.Column(db.Text(), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    dstatus = db.Column(db.String(10), nullable=False, default='no')
    odate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    ddate = db.Column(db.Date(), nullable=False)
    
    
class Product(db.Model):
    __tablename__='products'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    product_code = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    
    
class ProductLevel(db.Model):
    __tablename__='product_levels'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    v_shape = db.Column(db.String(10), nullable=False, default='no')
    polo = db.Column(db.String(10), nullable=False, default='no')
    clean_text = db.Column(db.String(10), nullable=False, default='no')
    design = db.Column(db.String(10), nullable=False, default='no')
    chain = db.Column(db.String(10), nullable=False, default='no')
    leather = db.Column(db.String(10), default='no', nullable=False)
    hook = db.Column(db.String(10), default='no', nullable=False)
    color = db.Column(db.String(10), nullable=False, default='no')
    formal = db.Column(db.String(10), nullable=False, default='no')
    converse = db.Column(db.String(10), nullable=False, default='no')
    loafer = db.Column(db.String(10), nullable=False, default='no')
    
    
class ProductView(db.Model):
    __tablename__='product_views'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    
# Authorize RBAC tables
#mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


# models
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)


class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


# class Article(db.Model, PermissionsMixin):
#     __tablename__ = 'articles'
#     __permissions__ = dict(
#         owner=['read', 'update', 'delete', 'revoke'],
#         group=['read', 'update'],
#         other=['read']
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), index=True, nullable=False)
#     content = db.Column(db.Text)
    
    
