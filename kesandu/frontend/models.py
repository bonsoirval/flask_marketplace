from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from kesandu import db, login
from sqlalchemy import Column
from flask_authorize import RestrictionsMixin, AllowancesMixin
from sqlalchemy.dialects.mysql import DATE, FLOAT, TINYINT, TEXT, INTEGER, VARCHAR, FLOAT, DECIMAL


# for flask_authorize use
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


class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, default='bonsoirval@gmail.com')
    username = db.Column(db.String(50), nullable=False, default='bonsoirval@gmail.com')
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(14), nullable=False, default='1234567890123')
    reg_time = db.Column(db.DateTime, default=datetime.utcnow)
    online = db.Column(db.String(1), nullable=False,default='0')
    activation = db.Column(db.String(3), nullable=False, default='no')
    
    # roles and groups are reserved words that *must* be defined
    # on the User model to use group- or role-based authorization.
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)

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


class Seller(db.Model, UserMixin):
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
    product = db.relationship('Product', backref='product', lazy=True)
    
    
    def __repr__(self):
        return '<Seller {}>'.format(self.username)    
    

# class Order(db.Model):
#     __tablename__='orders'
    
#     id = db.Column(db.Integer, nullable=False, primary_key=True)
#     uid = db.Column(db.Integer, nullable=True)
#     ofname = db.Column(db.Text(), nullable=False)
#     pid = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     oplace = db.Column(db.Text(), nullable=False)
#     mobile = db.Column(db.String(15), nullable=False)
#     dstatus = db.Column(db.String(10), nullable=False, default='no')
#     odate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
#     ddate = db.Column(db.Date(), nullable=False)
    
    
class Product(db.Model):
    __tablename__='products'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    product_code = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.Text(), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'),default=0)
    keywords = db.Column(db.String(120), nullable = False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    # seller = db.relationship('Sellers', backref='seller', lazy=True)
    
    
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


class Cart(db.Model):
    __tablename__='cart'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    api_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    session_id = db.Column(db.String(32), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    recurring_id = db.Column(db.Integer, nullable=False)
    option = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    invoice_no = db.Column(db.Integer, nullable=False, default='0')
    invoice_prefix = db.Column(db.String(26), nullable=False)
    seller_id = db.Column(db.Integer, nullable=False, default='0')
    # store_name = db.Column(db.String(64) , nullable=False)
    store_url  = db.Column(db.String(255) , nullable=False )
    user_id  = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False , default =  '0')
    customer_group_id  = db.Column(db.Integer , nullable=False , default =  '0')
    firstname = db.Column( db.String(32) , nullable=False )
    lastname  = db.Column(db.String(32) , nullable=False)
    email  = db.Column(db.String(96) , nullable=False)
    telephone  = db.Column(db.String(32) , nullable=False)
    fax  = db.Column(db.String(32) , nullable=False)
    custom_field  = db.Column(db.Text , nullable=False)
    payment_firstname  = db.Column(db.String(32) , nullable=False)
    payment_lastname  = db.Column(db.String(32) , nullable=False)
    payment_company  = db.Column(db.String(60) , nullable=False)
    payment_address_1  = db.Column(db.String(128) , nullable=False)
    payment_address_2  = db.Column(db.String(128) , nullable=False)
    payment_city  = db.Column(db.String(128) , nullable=False)
    payment_postcode  = db.Column(db.String(10) , nullable=False)
    payment_country  = db.Column(db.String(128) , nullable=False)
    payment_country_id = db.Column(db.Integer, nullable=False)
    payment_zone  = db.Column(db.String(128) , nullable=False)
    payment_zone_id = db.Column(db.Integer, nullable=False)
    payment_address_format = db.Column(db.Text , nullable=False)
    payment_custom_field = db.Column(db.Text , nullable=False)
    payment_method  = db.Column(db.String(128) , nullable=False)
    payment_code  = db.Column(db.String(128) , nullable=False)
    shipping_firstname  = db.Column(db.String(32), nullable=False)
    shipping_lastname  = db.Column(db.String(32), nullable=False)
    shipping_company  = db.Column(db.String(40) , nullable=False)
    shipping_address_1  = db.Column(db.String(128) , nullable=False)
    shipping_address_2  = db.Column(db.String(128) , nullable=False)
    shipping_city  = db.Column(db.String(128) , nullable=False)
    shipping_postcode  = db.Column(db.String(10) , nullable=False)
    shipping_country  = db.Column(db.String(128) , nullable=False)
    shipping_country_id = db.Column(db.Integer, nullable=False)
    shipping_zone  = db.Column(db.String(128) , nullable=False)
    shipping_zone_id = db.Column(db.Integer, nullable=False)
    shipping_address_format = db.Column(db.Text, nullable=False)
    shipping_custom_field = db.Column(db.Text , nullable=False)
    shipping_method  = db.Column(db.String(128) , nullable=False)
    shipping_code  = db.Column(db.String(128) , nullable=False)
    comment = db.Column(db.Text , nullable=False)
    total = db.Column(db.Float(15,4) , nullable=False , default =  '0.0000')
    order_status_id = db.Column(db.Integer, nullable=False , default =  '0')
    affiliate_id = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Float(15,4) , nullable=False)
    marketing_id = db.Column(db.Integer, nullable=False)
    tracking  = db.Column(db.String(64) , nullable=False)
    language_id  = db.Column(db.Integer, nullable=False)
    currency_id = db.Column(db.Integer, nullable=False)
    currency_code  = db.Column(db.String(3) , nullable=False)
    currency_value = db.Column(db.Float(15,8) , nullable=False , default =  '1.00000000')
    ip  = db.Column(db.String(40) , nullable=False)
    forwarded_ip  = db.Column(db.String(40), nullable=False)
    user_agent  = db.Column(db.String(255), nullable=False)
    accept_language  = db.Column(db.String(255) , nullable=False)
    date_added = db.Column(db.DateTime , nullable=False)
    date_modified = db.Column(db.DateTime , nullable=False)
    

# Authorize RBAC tables
#mapping tables
# models
# class User(db.Model):
#     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True} 

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)

#     # roles and groups are reserved words that *must* be defined
#     # on the User model to use group- or role-based authorization.
#     roles = db.relationship('Role', secondary=UserRole)
#     groups = db.relationship('Group', secondary=UserGroup)


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
    
    
# troubleshooting classes

# class Product(db.Model):
#     __tablename__='product'
#     id = db.Column(db.Integer, nullable=True, primary_key=True)
#     seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'),default=0)
#     model = db.Column(db.String(64), nullable=False)
#     sku = db.Column(db.String(64), nullable = False)
#     upc = db.Column(db.String(12), nullable = False)
#     ean = db.Column(db.String(14), nullable = False)
#     jan = db.Column(db.String(13),nullable = False)
#     isbn = db.Column(db.String(17), nullable = False)
#     mpn = db.Column(db.String(64), nullable = False)
#     location = db.Column(db.String(128), nullable = False)
#     quantity = db.Column(db.Integer, nullable = False, default = '0')
#     stock_status_id = db.Column(db.Integer, nullable = False)
#     image = db.Column(db.String(255), nullable = True)
#     manufacturer_id = db.Column(db.Integer, nullable = False)
#     shipping = db.Column(TINYINT(1), nullable = False, default = '1')
#     price = db.Column(db.Float(15, 4), nullable = False, default = '0.0000')
#     points = db.Column(db.Integer, nullable = False, default = '0')
#     tax_class_id = db.Column(db.Integer, nullable = False)
#     date_available = db.Column(db.DateTime, nullable = False, default = '0000-00-00')
#     weight = db.Column(db.Float(15,8), nullable = False, default = '0.00000000')
#     weight_class_id = db.Column(db.Integer, nullable = False, default = '0')
#     length = db.Column(db.Float(15,8), nullable = False, default = '0.00000000')
#     width = db.Column(db.Float(15,8), nullable = False, default = '0.00000000')
#     height = db.Column(db.Float(15, 8), nullable = False, default = '0.00000000')
#     length_class_id = db.Column(db.Integer, nullable = False, default = '0')
#     subtract = db.Column(TINYINT(1), nullable = False, default = '1')
#     minimum = db.Column(db.Integer, nullable = False, default = '1')
#     sort_order = db.Column(db.Integer, nullable = False, default = '0')
#     status = db.Column(TINYINT(1), nullable = False, default = '0')
#     viewed = db.Column(db.Integer, nullable = False, default = '0')
#     date_added = db.Column(db.DateTime, nullable = False)
#     date_modified = db.Column(db.DateTime, nullable = False)
    

# class product_description(db.Model):
#     id = Column(db.Integer, nullable=False, primary_key=True)
#     language_id  = Column(INTEGER(11), nullable = False)
#     name = Column(VARCHAR(255), nullable = False)
#     description = Column(TEXT, nullable = False)
#     tag = Column(TEXT, nullable = False)
#     meta_title = Column(VARCHAR(255), nullable = False)
#     meta_description = Column(VARCHAR(255), nullable = False)
#     meta_keyword = Column(VARCHAR(255), nullable = False)
    
from sqlalchemy.dialects.mysql import CHAR, DOUBLE, TINYINT, TEXT, ENUM,INTEGER, VARCHAR, FLOAT, DECIMAL, DATETIME

class address(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  nullable = False)
    firstname = Column(VARCHAR(32), nullable = False)
    lastname = Column(VARCHAR(32), nullable = False)
    company  = Column(VARCHAR(40), nullable = False)
    address_1  = Column(VARCHAR(128), nullable = False)
    address_2  = Column(VARCHAR(128), nullable = False)
    city  = Column(VARCHAR(128), nullable = False)
    postcode  = Column(VARCHAR(10), nullable = False)
    country_id  = Column(INTEGER(11),  nullable = False, default= '0')
    zone_id  = Column(INTEGER(11),  nullable = False, default= '0')
    custom_field  = Column(TEXT, nullable = False)
    
class advertise_google_target(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  nullable = False, default= '0')
    campaign_name = Column(VARCHAR(255), nullable = False)
    country  = Column(VARCHAR(2), nullable = False)
    budget  = Column(DECIMAL(15,4), nullable = False, default=0.0000)
    feeds = Column(TEXT, nullable = False)
    status  = Column(ENUM('paused','active'), nullable = False, default= 'paused')


class api(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable = False)
    username  = Column(VARCHAR(64), nullable = False)
    key  = Column(TEXT, nullable = False)
    status  = Column(TINYINT(1), nullable = False)
    date_added  = Column(DATETIME, nullable = False)
    date_modified  = Column(DATETIME, nullable = False)

class api_ip(db.Model):
  id  = Column(INTEGER(11),  nullable = False, primary_key=True)
  api_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
  ip  = Column(VARCHAR(40), nullable = False)



class api_session(db.Model):
  id = Column(INTEGER(11),  nullable = False)
  api_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
  session_id  = Column(VARCHAR(32), nullable = False)
  ip  = Column(VARCHAR(40), nullable = False)
  date_added  = Column(DATETIME, nullable = False)
  date_modified  = Column(DATETIME, nullable=False)
  
  
class attribute(db.Model):
    id  = Column(INTEGER(11), primary_key =False, nullable = False)
    attribute_group_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    sort_order  = Column(INTEGER(3), nullable = False)
  

class attribute_description(db.Model):
    id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    language_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    name  = Column(VARCHAR(64), nullable = False)

class attribute_group(db.Model):
    id  = Column(INTEGER(11), primary_key = True, nullable = False)
    sort_order  = Column(INTEGER(3), nullable = False)
    
class attribute_group_description(db.Model):
    id  = Column(INTEGER(11), primary_key = True, nullable = False)
    language_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    name  = Column(VARCHAR(64), nullable = False)

class banner(db.Model):
    id  = Column(INTEGER(11),  primary_key = True, nullable = False)
    name  = Column(VARCHAR(64), nullable = False)
    status  = Column(TINYINT(1), nullable = False)
 

class banner_image(db.Model):
    id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    banner_id  = Column(INTEGER(11),  nullable = False)
    language_id  = Column(INTEGER(11),  nullable = False)
    title  = Column(VARCHAR(64), nullable = False)
    link  = Column(VARCHAR(255), nullable = False)
    image  = Column(VARCHAR(255), nullable = False)
    sort_order  = Column(INTEGER(3), nullable = False, default= '0')

# class cart(db.Model):
            
#     id  = Column(INTEGER(11), nullable = False)
#     api_id  = Column(INTEGER(11),  nullable = False, primary_key=True)
#     customer_id  = Column(INTEGER(11),  nullable = False)
#     session_id  = Column(VARCHAR(32), nullable = False)
#     product_id  = Column(INTEGER(11),  nullable = False)
#     recurring_id  = Column(INTEGER(11),  nullable = False)
#     option  = Column(TEXT, nullable = False)
#     quantity  = Column(INTEGER(5), nullable = False)
#     date_added  = Column(DATETIME, nullable = False)


class category(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    image = Column(VARCHAR(255), nullable = True)
    parent_id  = Column(INTEGER(11),  nullable = False, default= '0')
    top  = Column(TINYINT(1), nullable = False)
    column  = Column(INTEGER(3), nullable = False)
    sort_order  = Column(INTEGER(3), nullable = False, default= '0')
    status  = Column(TINYINT(1), nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)
    date_modified  = Column(DATETIME, nullable = False, default=datetime.utcnow)

class category_description(db.Model):
    id  = Column(INTEGER(11),  nullable = False, primary_key=True)
    language_id  = Column(INTEGER(11),  nullable = False)
    name  = Column(VARCHAR(255), nullable = False)
    description  = Column(TEXT, nullable = False)
    meta_title  = Column(VARCHAR(255), nullable = False)
    meta_description  = Column(VARCHAR(255), nullable = False)
    meta_keyword  = Column(VARCHAR(255), nullable = False)


class category_filter(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable = False)
    filter_id = Column(INTEGER(11),  nullable = False)

class category_path(db.Model):
    id = Column(INTEGER(11), primary_key= True, nullable = False)
    path_id = Column(INTEGER(11),  nullable = False)
    level = Column(INTEGER(11),  nullable = False)

class category_to_google_product_category(db.Model):
    id = Column(INTEGER(11), nullable=True, primary_key=True)
    google_product_category = Column(VARCHAR(10), nullable = False)
    store_id = Column(INTEGER(11),  nullable = False, default= '0')
    category_id = Column(INTEGER(11),  nullable = False)

class category_to_layout(db.Model):
    id = Column(INTEGER(11),  nullable = False, primary_key=True)
    store_id = Column(INTEGER(11),  nullable = False)
    layout_id = Column(INTEGER(11),  nullable = False)

class category_to_store(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11), nullable = False)


class country(db.Model):
    id = Column(INTEGER(11), primary_key=True,  nullable = False)
    name = Column(VARCHAR(128), nullable = False)
    iso_code_2 = Column(VARCHAR(2), nullable = False)
    iso_code_3 = Column(VARCHAR(3), nullable = False)
    address_format = Column(TEXT, nullable = False)
    postcode_required = Column(TINYINT(1), nullable = False)
    status = Column(TINYINT(1), nullable = False, default= '1')


class coupon(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable = False)
    name = Column(VARCHAR(128), nullable = False)
    code = Column(VARCHAR(20), nullable = False)
    type = Column(CHAR(1), nullable = False)
    discount = Column(DECIMAL(15,4), nullable = False)
    logged = Column(TINYINT(1), nullable = False)
    shipping = Column(TINYINT(1), nullable = False)
    total = Column(DECIMAL(15,4), nullable = False)
    date_start = Column(DATETIME, nullable = False, default= '0000-00-00')
    date_end = Column(DATETIME, nullable = False, default= '0000-00-00')
    uses_total = Column(INTEGER(11),  nullable = False)
    uses_customer = Column(VARCHAR(11), nullable = False)
    status = Column(TINYINT(1), nullable = False)
    date_added = Column(DATETIME, nullable = False, default = datetime.utcnow)
   
    
class coupon_category(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    category_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class coupon_history(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    coupon_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    amount = Column(DECIMAL(15,4), nullable = False)
    date_added = Column(DATETIME, nullable = False)


class coupon_product(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    coupon_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)

class currency(db.Model):
    currency_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    title = Column(VARCHAR(32), nullable = False)
    code = Column(VARCHAR(3), nullable = False)
    symbol_left = Column(VARCHAR(12), nullable = False)
    symbol_right = Column(VARCHAR(12), nullable = False)
    decimal_place = Column(CHAR(1), nullable = False)
    value = Column(DOUBLE(15,8), nullable = False)
    status = Column(TINYINT(1), nullable = False)
    date_modified = Column(DATETIME, nullable=False)
  
class customer(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    firstname = Column(VARCHAR(32), nullable = False)
    lastname = Column(VARCHAR(32), nullable = False)
    email = Column(VARCHAR(96), nullable = False)
    telephone = Column(VARCHAR(32), nullable = False)
    fax = Column(VARCHAR(32), nullable = False)
    password = Column(VARCHAR(40), nullable = False)
    salt = Column(VARCHAR(9), nullable = False)
    cart = Column(TEXT)
    wishlist = Column(TEXT)
    newsletter = Column(TINYINT(1), nullable = False, default= '0')
    address_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    custom_field = Column(TEXT, nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    status = Column(TINYINT(1), nullable = False)
    safe = Column(TINYINT(1), nullable = False)
    token = Column(TEXT, nullable = False)
    code = Column(VARCHAR(40), nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)
    

class customer_activity(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    key = Column(VARCHAR(64), nullable = False)
    data = Column(TEXT, nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    date_added = Column(DATETIME, nullable=False, default = datetime.utcnow)

class customer_affiliate(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    company = Column(VARCHAR(40), nullable = False)
    website = Column(VARCHAR(255), nullable = False)
    tracking = Column(VARCHAR(64), nullable = False)
    commission = Column(DECIMAL(4,2), nullable = False, default= '0.00')
    tax = Column(VARCHAR(64), nullable = False)
    payment = Column(VARCHAR(6), nullable = False)
    cheque = Column(VARCHAR(100), nullable = False)
    paypal = Column(VARCHAR(64), nullable = False)
    bank_name = Column(VARCHAR(64), nullable = False)
    bank_branch_number = Column(VARCHAR(64), nullable = False)
    bank_swift_code = Column(VARCHAR(64), nullable = False)
    bank_account_name = Column(VARCHAR(64), nullable = False)
    bank_account_number = Column(VARCHAR(64), nullable = False)
    custom_field = Column(TEXT, nullable = False)
    status = Column(TINYINT(1), nullable = False)
    date_added = Column(DATETIME, nullable=False, default = datetime.utcnow)



class customer_approval(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    type = Column(VARCHAR(9), nullable = False)
    date_added = Column(DATETIME, nullable = False, default = datetime.utcnow)



class customer_group(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    approval = Column(INTEGER(1), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)



class customer_group_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)
    description = Column(TEXT, nullable = False)


class customer_history(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    comment = Column(TEXT, nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)


class customer_ip(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)


class customer_login(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    email = Column(VARCHAR(96), nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    total = Column(INTEGER(4), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)
    date_modified = Column(DATETIME, nullable = False, default = datetime.utcnow)


class customer_online(db.Model):
    ip = Column(VARCHAR(40), nullable = False)
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    url = Column(TEXT, nullable = False)
    referer = Column(TEXT, nullable = False)
    date_added = Column(DATETIME, nullable=False, default = datetime.utcnow)


class customer_reward(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    description = Column(TEXT, nullable = False)
    poINTEGERs = Column(INTEGER(8), nullable = False, default= '0')
    date_added = Column(DATETIME, nullable=False, default = datetime.utcnow)


class customer_search(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    keyword = Column(VARCHAR(255), nullable = False)
    category_id = Column(INTEGER(11), nullable = False)
    sub_category = Column(TINYINT(1), nullable = False)
    description = Column(TINYINT(1), nullable = False)
    products = Column(INTEGER(11),  nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)


class customer_transaction(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    description = Column(TEXT, nullable = False)
    amount = Column(DECIMAL(15,4), nullable = False)
    date_added = Column(DATETIME, nullable=False, default = datetime.utcnow)



class customer_wishlist(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable=False)


class custom_field(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    type = Column(VARCHAR(32), nullable = False)
    value = Column(TEXT, nullable = False)
    validation = Column(VARCHAR(255), nullable = False)
    location = Column(VARCHAR(10), nullable = False)
    status = Column(TINYINT(1), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)



class custom_field_customer_group(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    required = Column(TINYINT(1), nullable = False)


class custom_field_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(128), nullable = False)


class custom_field_value(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    custom_field_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)

class custom_field_value_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    custom_field_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(128), nullable = False)


class download(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    filename = Column(VARCHAR(160), nullable = False)
    mask = Column(VARCHAR(128), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable=False)


class download_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)


class event(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    code = Column(VARCHAR(64), nullable = False)
    trigger = Column(TEXT, nullable = False)
    action = Column(TEXT, nullable = False)
    status = Column(TINYINT(1), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)


class extension(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    type = Column(VARCHAR(32), nullable = False)
    code = Column(VARCHAR(32), nullable = False)


class extension_install(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    extension_download_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    filename = Column(VARCHAR(255), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable=False)


class extension_path(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    extension_install_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    path = Column(VARCHAR(255), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)


class filter(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    filter_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)


class filter_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    filter_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)


class filter_group(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)


class filter_group_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)


class geo_zone(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)
    description = Column(VARCHAR(255), nullable = False)
    date_added = Column(DATETIME, nullable = False, default = datetime.utcnow)
    date_modified = Column(DATETIME, default=datetime.utcnow, nullable=False)


class information(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    bottom = Column(INTEGER(1), nullable = False, default= '0')
    sort_order = Column(INTEGER(3), nullable = False, default= '0')
    status = Column(TINYINT(1), nullable = False, default= '1')



class information_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    title = Column(VARCHAR(64), nullable = False)
    description_medium= Column(TEXT, nullable = False)
    meta_title = Column(VARCHAR(255), nullable = False)
    meta_description = Column(VARCHAR(255), nullable = False)
    meta_keyword = Column(VARCHAR(255), nullable = False)

class information_to_layout(db.Model):
  id = Column(INTEGER(11),  primary_key = True, nullable = False)
  store_id = Column(INTEGER(11),  primary_key = True, nullable = False)
  layout_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class information_to_store(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class language(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)
    code = Column(VARCHAR(5), nullable = False)
    locale = Column(VARCHAR(255), nullable = False)
    image = Column(VARCHAR(64), nullable = False)
    directory = Column(VARCHAR(32), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False, default= '0')
    status = Column(TINYINT(1), nullable = False)



class layout(db.Model):
  id = Column(INTEGER(11),  primary_key = True, nullable = False)
  name = Column(VARCHAR(64), nullable = False)


class layout_module(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    layout_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    code = Column(VARCHAR(64), nullable = False)
    position = Column(VARCHAR(14), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)


class layout_route(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    layout_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    route = Column(VARCHAR(64), nullable = False)


class length_class(db.Model):
  id = Column(INTEGER(11),  primary_key = True, nullable = False)
  value = Column(DECIMAL(15,8), nullable = False)


class length_class_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    title = Column(VARCHAR(32), nullable = False)
    unit = Column(VARCHAR(4), nullable = False)


class location(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)
    address = Column(TEXT, nullable = False)
    telephone = Column(VARCHAR(32), nullable = False)
    fax = Column(VARCHAR(32), nullable = False)
    geocode = Column(VARCHAR(32), nullable = False)
    image = Column(VARCHAR(255), nullable=False)
    open = Column(TEXT, nullable = False)
    comment = Column(TEXT, nullable = False)


class lts_assigned_category(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    category_id = Column(TEXT, nullable = False)


class lts_attribute(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    attribute_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False) 


class lts_attribute_group(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class lts_attribute_mapping(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    attribute = Column(VARCHAR(256), nullable = False)
    category_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class lts_cart(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key=True)
    cart_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    api_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    session_id = Column(VARCHAR(32), nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    quantity = Column(INTEGER(5), nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)
    
    
    
class lts_category(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    category_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    assigned = Column(INTEGER(11),  nullable = False)
    status = Column(INTEGER(11),  nullable = False)
    approved = Column(INTEGER(11),  nullable = False)



class lts_commission(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    amount = Column(DECIMAL(15,4), nullable = False)
    type = Column(VARCHAR(30), nullable = False)
    status = Column(TINYINT(4), nullable = False)
    date_added = Column(DATETIME, nullable = False)
    date_modified = Column(DATETIME, nullable = False)
    default=_commission = Column(INTEGER(12), nullable = False, default = datetime.utcnow)


class lts_coupon(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    coupon_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    code = Column(VARCHAR(20), nullable = False)



class lts_download(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)



class lts_filter_group(db.Model):
    filter_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11), default= datetime.utcnow, nullable = False)



class lts_mail(db.Model):
    id = Column(INTEGER(10), nullable = False, primary_key=True)
    too_id = Column(INTEGER(2), nullable = False)
    subject = Column(VARCHAR(250), nullable = False)
    message = Column(TEXT, nullable = False)
    status = Column(INTEGER(1), nullable = False)
    date_added = Column(DATETIME, nullable=False, default= datetime.utcnow)
    date_modified = Column(DATETIME, nullable = False, default= datetime.utcnow) 


class lts_manufacturer(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False) 


class lts_option(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class lts_option_mapping(db.Model):
    option_mapping_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    category_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option = Column(VARCHAR(260), nullable = False)



class lts_order_history(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    notify = Column(TINYINT(1), nullable = False, default= '0')
    comment = Column(TEXT, nullable = False)
    date_added = Column(DATETIME, nullable = False, default = datetime.utcnow)



class lts_order_product(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    quantity = Column(INTEGER(11),  nullable = False)
    price = Column(DECIMAL(10,4), nullable = False)
    total = Column(DECIMAL(10,4), nullable = False)
    tax = Column(DECIMAL(15,4), nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)
    date_modified = Column(DATETIME, default=datetime.utcnow)


class lts_payment(db.Model):
    id = Column(INTEGER(13), nullable = False, primary_key=True)
    paypal = Column(VARCHAR(50), nullable = False)
    account_holder = Column(VARCHAR(100), nullable = False)
    bankname = Column(VARCHAR(100), nullable = False)
    accountno = Column(VARCHAR(20), nullable = False)
    ifsc = Column(VARCHAR(15), nullable = False)


class lts_pincode(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable=True)
    country_id = Column(INTEGER(11), default=datetime.utcnow, nullable=False)
    zone_id = Column(INTEGER(11), default= datetime.utcnow, nullable=False)
    status = Column(INTEGER(11),  nullable = False)


class lts_pincode_status(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    pincode_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    pincode = Column(INTEGER(11),  nullable = False)
    status = Column(INTEGER(11),  nullable = False)


class lts_plan(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    subscription_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    default=_plan = Column(INTEGER(11),  nullable = False)
    subscription_fee = Column(INTEGER(11),  nullable = False)
    subscription_commission = Column(INTEGER(11),  nullable = False)
    validity = Column(INTEGER(11),  nullable = False)
    date_added = Column(DATETIME,default = datetime.utcnow, nullable=False)
    date_expire = Column(DATETIME, default = datetime.utcnow, nullable=False)


class lts_product(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    price = Column(FLOAT, nullable=False)
    quantity = Column(INTEGER(11),  nullable = False)
    status = Column(INTEGER(11),  nullable = False)
    approved = Column(INTEGER(11),  nullable = False)
    exist = Column(INTEGER(11),  nullable = False, default= '0')


class lts_product_exist(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    price = Column(FLOAT, nullable=False)
    quantity = Column(INTEGER(11),  nullable = False)
    status = Column(INTEGER(11),  nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow)
    date_modified = Column(DATETIME, default=datetime.utcnow, nullable=False)


class lts_product_to_pincode(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    pincode_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class lts_review(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    review_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    vendor_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class lts_subscription(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    subscription_fee = Column(DECIMAL(10,0), nullable = False)
    status = Column(INTEGER(11),  nullable = False)
    subscription_commission = Column(INTEGER(11),  nullable = False)
    default=_plan = Column(INTEGER(11),  nullable = False)
    date_added = Column(DATETIME, nullable = False)
    date_modified = Column(DATETIME, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    plan_type = Column(INTEGER(2), nullable = False)


class lts_subscription_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    description = Column(TEXT, nullable = False)


class lts_too(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(250), nullable = False)


class lts_vendor(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    commission_rate = Column(INTEGER(11),  nullable = False)
    description = Column(VARCHAR(255), nullable = False)
    meta_title = Column(VARCHAR(65), nullable = False)
    meta_description = Column(VARCHAR(255), nullable = False)
    meta_keyword = Column(VARCHAR(255), nullable = False)
    store_owner = Column(VARCHAR(64), nullable = False)
    store_name = Column(VARCHAR(30), nullable = False)
    address = Column(TEXT, nullable = False)
    email = Column(VARCHAR(35), nullable = False)
    telephone = Column(VARCHAR(32), nullable = False)
    fax = Column(VARCHAR(32), nullable = False)
    country_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    zone_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    city = Column(VARCHAR(32), nullable = False)
    logo = Column(TEXT, nullable = False)
    banner = Column(TEXT, nullable = False)
    profile_image = Column(TEXT)
    facebook = Column(TEXT, nullable = False)
    instagram = Column(TEXT, nullable = False)
    youtube = Column(TEXT, nullable = False)
    twitter = Column(TEXT, nullable = False)
    pINTEGERerest = Column(TEXT, nullable = False)
    status = Column(INTEGER(2), nullable = False, default= '0')
    approved = Column(INTEGER(2), nullable = False, default= '0')
    date_added = Column(DATETIME, default = datetime.utcnow, nullable=False)



class lts_withdrawal(db.Model):
    id = Column(INTEGER(255), nullable = False, primary_key=True)
    vendor_id = Column(INTEGER(155), nullable = False)
    vendor_name = Column(VARCHAR(255), nullable = False)
    amount = Column(DECIMAL(15,3), nullable = False)
    payment_processed = Column(VARCHAR(10), nullable = False)
    withdrawal_initiate_date = Column(DATETIME, nullable = False)
    bank_name = Column(VARCHAR(155), nullable = False)
    payment_mode = Column(VARCHAR(155), nullable = False)
    transection_id = Column(VARCHAR(255), nullable = False)
    vendor_bank_account_no = Column(VARCHAR(255), nullable = False)
    payment_initiate_date = Column(DATE, nullable=False, default = datetime.utcnow)


class manufacturer(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)
    image = Column(VARCHAR(255), default= datetime.utcnow)
    sort_order = Column(INTEGER(3), nullable = False)


class manufacturer_to_store(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class marketing(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)
    description = Column(TEXT, nullable = False)
    code = Column(VARCHAR(64), nullable = False)
    clicks = Column(INTEGER(5), nullable = False, default= '0')
    date_added = Column(DATETIME, nullable=False, default=datetime.utcnow)


class modification(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    extension_install_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)
    code = Column(VARCHAR(64), nullable = False)
    author = Column(VARCHAR(64), nullable = False)
    version = Column(VARCHAR(32), nullable = False)
    link = Column(VARCHAR(255), nullable = False)
    xml_medium= Column(TEXT, nullable = False)
    status = Column(TINYINT(1), nullable = False)
    date_add = Column(DATETIME, nullable = False, default = datetime.utcnow)


class module(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)
    code = Column(VARCHAR(32), nullable = False)
    setting = Column(TEXT, nullable = False)


class option(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    type = Column(VARCHAR(32), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)



class option_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(128), nullable = False)


class option_value(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    image = Column(VARCHAR(255), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False)


class option_value_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(128), nullable = False)


class order(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    invoice_no = Column(INTEGER(11),  nullable = False, default= '0')
    invoice_prefix = Column(VARCHAR(26), nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    store_name = Column(VARCHAR(64), nullable = False)
    store_url = Column(VARCHAR(255), nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    firstname = Column(VARCHAR(32), nullable = False)
    lastname = Column(VARCHAR(32), nullable = False)
    email = Column(VARCHAR(96), nullable = False)
    telephone = Column(VARCHAR(32), nullable = False)
    fax = Column(VARCHAR(32), nullable = False)
    custom_field = Column(TEXT, nullable = False)
    payment_firstname = Column(VARCHAR(32), nullable = False)
    payment_lastname = Column(VARCHAR(32), nullable = False)
    payment_company = Column(VARCHAR(60), nullable = False)
    payment_address_1 = Column(VARCHAR(128), nullable = False)
    payment_address_2 = Column(VARCHAR(128), nullable = False)
    payment_city = Column(VARCHAR(128), nullable = False)
    payment_postcode = Column(VARCHAR(10), nullable = False)
    payment_country = Column(VARCHAR(128), nullable = False)
    payment_country_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    payment_zone = Column(VARCHAR(128), nullable = False)
    payment_zone_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    payment_address_format = Column(TEXT, nullable = False)
    payment_custom_field = Column(TEXT, nullable = False)
    payment_method = Column(VARCHAR(128), nullable = False)
    payment_code = Column(VARCHAR(128), nullable = False)
    shipping_firstname = Column(VARCHAR(32), nullable = False)
    shipping_lastname = Column(VARCHAR(32), nullable = False)
    shipping_company = Column(VARCHAR(40), nullable = False)
    shipping_address_1 = Column(VARCHAR(128), nullable = False)
    shipping_address_2 = Column(VARCHAR(128), nullable = False)
    shipping_city = Column(VARCHAR(128), nullable = False)
    shipping_postcode = Column(VARCHAR(10), nullable = False)
    shipping_country = Column(VARCHAR(128), nullable = False)
    shipping_country_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    shipping_zone = Column(VARCHAR(128), nullable = False)
    shipping_zone_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    shipping_address_format = Column(TEXT, nullable = False)
    shipping_custom_field = Column(TEXT, nullable = False)
    shipping_method = Column(VARCHAR(128), nullable = False)
    shipping_code = Column(VARCHAR(128), nullable = False)
    comment = Column(TEXT, nullable = False)
    total = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    order_status_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    affiliate_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    commission = Column(DECIMAL(15,4), nullable = False)
    marketing_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    tracking = Column(VARCHAR(64), nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    currency_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    currency_code = Column(VARCHAR(3), nullable = False)
    currency_value = Column(DECIMAL(15,8), nullable = False, default= '1.00000000')
    ip = Column(VARCHAR(40), nullable = False)
    forwarded_ip = Column(VARCHAR(40), nullable = False)
    user_agent = Column(VARCHAR(255), nullable = False)
    accept_language = Column(VARCHAR(255), nullable = False)
    date_added = Column(DATETIME, nullable = False)
    date_modified = Column(DATETIME, nullable=False, default=datetime.utcnow)


class order_history(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    notify = Column(TINYINT(1), nullable = False, default= '0')
    comment = Column(TEXT, nullable = False)
    date_added = Column(DATETIME, nullable=False, default=datetime.utcnow)


class order_option(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_option_value_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    name = Column(VARCHAR(255), nullable = False)
    value = Column(TEXT, nullable = False)
    type = Column(VARCHAR(32), nullable = False)


class order_product(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    model = Column(VARCHAR(64), nullable = False)
    quantity = Column(INTEGER(4), nullable = False)
    price = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    total = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    tax = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    reward = Column(INTEGER(8), nullable = False)


class order_recurring(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    reference = Column(VARCHAR(255), nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_name = Column(VARCHAR(255), nullable = False)
    product_quantity = Column(INTEGER(11),  nullable = False)
    recurring_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    recurring_name = Column(VARCHAR(255), nullable = False)
    recurring_description = Column(VARCHAR(255), nullable = False)
    recurring_frequency = Column(VARCHAR(25), nullable = False)
    recurring_cycle_small= Column(INTEGER(6), nullable = False)
    recurring_duration_small= Column(INTEGER(6), nullable = False)
    recurring_price = Column(DECIMAL(10,4), nullable = False)
    trial = Column(TINYINT(1), nullable = False)
    trial_frequency = Column(VARCHAR(25), nullable = False)
    trial_cycle_small = Column(INTEGER(6), nullable = False)
    trial_duration_small= Column(INTEGER(6), nullable = False)
    trial_price = Column(DECIMAL(10,4), nullable = False)
    status = Column(TINYINT(4), nullable = False)
    date_added = Column(DATETIME, nullable = False, default = datetime.utcnow)


class order_recurring_transaction(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_recurring_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    reference = Column(VARCHAR(255), nullable = False)
    type = Column(VARCHAR(255), nullable = False)
    amount = Column(DECIMAL(10,4), nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable=False)


class order_shipment(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)
    shipping_courier_id = Column(VARCHAR(255), nullable = False, default= '')
    tracking_number = Column(VARCHAR(255), nullable = False, default= '')


class order_status(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)

class order_total(db.Model):
    id = Column(INTEGER(10), nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    code = Column(VARCHAR(32), nullable = False)
    title = Column(VARCHAR(255), nullable = False)
    value = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    sort_order = Column(INTEGER(3), nullable = False)


class order_voucher(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    voucher_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    description = Column(VARCHAR(255), nullable = False)
    code = Column(VARCHAR(10), nullable = False)
    from_name = Column(VARCHAR(64), nullable = False)
    from_email = Column(VARCHAR(96), nullable = False)
    to_name = Column(VARCHAR(64), nullable = False)
    to_email = Column(VARCHAR(96), nullable = False)
    voucher_theme_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    message = Column(TEXT, nullable = False)
    amount = Column(DECIMAL(15,4), nullable = False)



class product(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    model = Column(VARCHAR(64), nullable = False)
    sku = Column(VARCHAR(64), nullable = False)
    upc = Column(VARCHAR(12), nullable = False)
    ean = Column(VARCHAR(14), nullable = False)
    jan = Column(VARCHAR(13), nullable = False)
    isbn = Column(VARCHAR(17), nullable = False)
    mpn = Column(VARCHAR(64), nullable = False)
    location = Column(VARCHAR(128), nullable = False)
    quantity = Column(INTEGER(4), nullable = False, default= '0')
    stock_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    image = Column(VARCHAR(255), default= datetime.utcnow)
    manufacturer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    shipping = Column(TINYINT(1), nullable = False, default= '1')
    price = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    poINTEGERs = Column(INTEGER(8), nullable = False, default= '0')
    tax_class_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    date_available = Column(DATETIME, default = datetime.utcnow)
    weight = Column(DECIMAL(15,8), nullable = False, default= '0.00000000')
    weight_class_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    length = Column(DECIMAL(15,8), nullable = False, default= '0.00000000')
    width = Column(DECIMAL(15,8), nullable = False, default= '0.00000000')
    height = Column(DECIMAL(15,8), nullable = False, default= '0.00000000')
    length_class_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    subtract = Column(TINYINT(1), nullable = False, default= '1')
    minimum = Column(INTEGER(11),  nullable = False, default= '1')
    sort_order = Column(INTEGER(11),  nullable = False, default= '0')
    status = Column(TINYINT(1), nullable = False, default= '0')
    viewed = Column(INTEGER(5), nullable = False, default= '0')
    date_added = Column(DATETIME, default = datetime.utcnow, nullable = False)
    date_modified = Column(DATETIME, default = datetime.utcnow, nullable=False)


class product_advertise_google(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key = True)
    product_id = Column(INTEGER(11), nullable=True)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    has_issues = Column(TINYINT(1), nullable=True)
    destination_status = Column(ENUM('pending','approved','disapproved'), nullable = False, default= 'pending')
    impressions = Column(INTEGER(11),  nullable = False, default= '0')
    clicks = Column(INTEGER(11),  nullable = False, default= '0')
    conversions = Column(INTEGER(11),  nullable = False, default= '0')
    cost = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    conversion_value = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    google_product_category = Column(VARCHAR(10), nullable=False)
    condition = Column(ENUM('new','refurbished','used'), nullable=True)
    adult = Column(TINYINT(1), nullable=True)
    multipack = Column(INTEGER(11), nullable=True)
    is_bundle = Column(TINYINT(1), nullable=True)
    age_group = Column(ENUM('newborn','infant','toddler','kids','adult'),  nullable=False)
    color = Column(INTEGER(11), nullable=True)
    gender = Column(ENUM('male','female','unisex'), nullable=True)
    size_type = Column(ENUM('regular','petite','plus','big and tall','maternity'), nullable = True)
    size_system = Column(ENUM('AU','BR','CN','DE','EU','FR','IT','JP','MEX','UK','US'), nullable = True)
    size = Column(INTEGER(11), nullable=True)
    is_modified = Column(TINYINT(1), nullable = False, default= '0')



class product_advertise_google_status(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    product_variation_id = Column(VARCHAR(64), nullable = False,  default= '')
    destination_statuses = Column(TEXT, nullable = False)
    data_quality_issues = Column(TEXT, nullable = False)
    item_level_issues = Column(TEXT, nullable = False)
    google_expiration_date = Column(INTEGER(11),  nullable = False, default= '0')



class product_advertise_google_target(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    advertise_google_target_id = Column(INTEGER(11), nullable = False)


class product_attribute(db.Model):
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    attribute_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    text = Column(TEXT , nullable = False)



class product_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    description = Column(TEXT, nullable = False)
    tag = Column(TEXT, nullable = False)
    meta_title = Column(VARCHAR(255), nullable = False)
    meta_description = Column(VARCHAR(255), nullable = False)
    meta_keyword = Column(VARCHAR(255), nullable = False)



class product_discount(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    quantity = Column(INTEGER(4), nullable = False, default= '0')
    priority = Column(INTEGER(5), nullable = False, default= '1')
    price = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    date_start = Column(DATETIME, nullable=False, default= datetime.utcnow)
    date_end = Column(DATETIME, nullable=False, default= datetime.utcnow)


class product_filter(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    filter_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class product_image(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    image = Column(VARCHAR(255), nullable=True)
    sort_order = Column(INTEGER(3), nullable = False, default= '0')


class product_option(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    value = Column(TEXT, nullable = False)
    required = Column(TINYINT(1), nullable = False)


class product_option_value(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    option_value_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    quantity = Column(INTEGER(3), nullable = False)
    subtract = Column(TINYINT(1), nullable = False)
    price = Column(DECIMAL(15,4), nullable = False)
    price_prefix = Column(VARCHAR(1), nullable = False)
    poINTEGERs = Column(INTEGER(8), nullable = False)
    poINTEGERs_prefix = Column(VARCHAR(1), nullable = False)
    weight = Column(DECIMAL(15,8), nullable = False)
    weight_prefix = Column(VARCHAR(1), nullable = False)


class product_recurring(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    recurring_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class product_related(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    related_id = Column(INTEGER(11),  primary_key = True, nullable = False)



class product_reward(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    poINTEGERs = Column(INTEGER(8), nullable = False, default= '0')


class product_special(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_group_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    priority = Column(INTEGER(5), nullable = False, default= 1)
    price = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    date_start = Column(DATETIME, nullable=False, default= datetime.utcnow)
    date_end = Column(DATETIME, nullable = False, default= datetime.utcnow)


class product_to_category(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    category_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class product_to_download(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    download_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class product_to_layout(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    layout_id = Column(INTEGER(11),  primary_key = True, nullable = False)


class product_to_store(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')


class recurring(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    price = Column(DECIMAL(10,4), nullable = False)
    frequency = Column(ENUM('day','week','semi_month','month','year'), nullable = False)
    duration = Column(INTEGER(10), nullable = False)
    cycle = Column(INTEGER(10), nullable = False)
    trial_status = Column(TINYINT(4), nullable = False)
    trial_price = Column(DECIMAL(10,4), nullable = False)
    trial_frequency =Column(ENUM('day','week','semi_month','month','year'), nullable = False)
    trial_duration = Column(INTEGER(10), nullable = False)
    trial_cycle = Column(INTEGER(10), nullable = False)
    status = Column(TINYINT(4), nullable = False)
    sort_order = Column(INTEGER(11),  nullable = False)


class recurring_description(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(255), nullable = False)


class py_return(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    order_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    firstname = Column(VARCHAR(32), nullable = False)
    lastname = Column(VARCHAR(32), nullable = False)
    email = Column(VARCHAR(96), nullable = False)
    telephone = Column(VARCHAR(32), nullable = False)
    product = Column(VARCHAR(255), nullable = False)
    model = Column(VARCHAR(64), nullable = False)
    quantity = Column(INTEGER(4), nullable = False)
    opened = Column(TINYINT(1), nullable = False)
    return_reason_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    return_action_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    return_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    comment = Column(TEXT)
    date_ordered = Column(DATETIME, nullable=False, default=datetime.utcnow)
    date_added = Column(DATETIME,default=datetime.utcnow, nullable = False)
    date_modified = Column(DATETIME, nullable=False, default=datetime.utcnow)



class return_action(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    name = Column(VARCHAR(64), nullable = False)


class return_history(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    return_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    return_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    notify = Column(TINYINT(1), nullable = False)
    comment = Column(TEXT, nullable = False)
    date_added = Column(DATETIME, nullable = False, default=datetime.utcnow)

class return_reason(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    name = Column(VARCHAR(128), nullable = False)


class return_status(db.Model):
    return_status_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    name = Column(VARCHAR(32), nullable = False)


class review(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    product_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    customer_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    author = Column(VARCHAR(64), nullable = False)
    text = Column(TEXT, nullable = False)
    rating = Column(INTEGER(1), nullable = False)
    status = Column(TINYINT(1), nullable = False, default= '0')
    date_added = Column(DATETIME, nullable = False)
    date_modified = Column(DATETIME, default = datetime.utcnow, nullable=False) 


class seo_url(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    query = Column(VARCHAR(255), nullable = False)
    keyword = Column(VARCHAR(255), nullable = False)


class session(db.Model):
    id = Column(VARCHAR(32), nullable = False, primary_key=True)
    data = Column(TEXT, nullable = False)
    expire = Column(DATETIME, default = datetime.utcnow, nullable=False)


class setting(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    store_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    code = Column(VARCHAR(128), nullable = False)
    key = Column(VARCHAR(128), nullable = False)
    value = Column(TEXT, nullable = False)
    serialized = Column(TINYINT(1), nullable = False)


class shipping_courier(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    shipping_courier_code = Column(VARCHAR(255), nullable = False, default= '')
    shipping_courier_name = Column(VARCHAR(255), nullable = False, default= '')


class statistics(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    code = Column(VARCHAR(64), nullable = False)
    value = Column(DECIMAL(15,4), nullable = False)


class stock_status(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    language_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(32), nullable = False)


class store(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    name = Column(VARCHAR(64), nullable = False)
    url = Column(VARCHAR(255), nullable = False)
    ssl = Column(VARCHAR(255), nullable = False)


class tax_class(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    title = Column(VARCHAR(32), nullable = False)
    description = Column(VARCHAR(255), nullable = False)
    date_added = Column(DATETIME, nullable = False)
    date_modified = Column(DATETIME, default=datetime.utcnow, nullable=False)


class tax_rate(db.Model):
    id = Column(INTEGER(11),  primary_key = True, nullable = False)
    geo_zone_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    name = Column(VARCHAR(32), nullable = False)
    rate = Column(DECIMAL(15,4), nullable = False, default= '0.0000')
    type = Column(CHAR(1), nullable = False)
    date_added = Column(DATETIME, default=datetime.utcnow, nullable = False)
    date_modified = Column(DATETIME, default=datetime.utcnow, nullable=False)


class zone_to_geo_zone(db.Model):
    zone_to_geo_zone_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    country_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    zone_id = Column(INTEGER(11),  primary_key = True, nullable = False, default= '0')
    geo_zone_id = Column(INTEGER(11),  primary_key = True, nullable = False)
    date_added = Column(DATETIME,default = datetime.utcnow, nullable = False)
    date_modified = Column(DATETIME, default=False, nullable=False)
