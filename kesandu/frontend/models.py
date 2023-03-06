from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from kesandu import db, login
from sqlalchemy import Column, ForeignKey
from flask_authorize import RestrictionsMixin, AllowancesMixin
from sqlalchemy.dialects.mysql import DATE,DECIMAL, SMALLINT, FLOAT, TEXT,INTEGER, VARCHAR, FLOAT, DECIMAL, CHAR, DOUBLE, ENUM,   DATETIME


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
    # product_id = Column(INTEGER(11), db.ForeignKey('products.id'), nullable=True)
    # product = db.relationship('Product', backref='products', lazy=True)
    
    
    def __repr__(self):
        return '<Seller {}>'.format(self.username)    
    
    
class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Customer(db.Model):
    id  = Column(INTEGER(11), primary_key=True, nullable=False)
    customer_group_id = Column(INTEGER(11), nullable=False)
    store_id = Column(INTEGER(11), nullable=False, default = 0)
    language_id  = Column(INTEGER(11), nullable=False)
    firstname  = Column(VARCHAR(32), nullable = False)
    lastname  = Column(VARCHAR(32), nullable = False)
    email  = Column(VARCHAR(96), nullable = False)
    telephone  = Column(VARCHAR(32), nullable = False)
    fax  = Column(VARCHAR(32), nullable = False)
    password  = Column(VARCHAR(40), nullable = False)
    salt  = Column(VARCHAR(9), nullable = False)
    cart  = Column(TEXT)
    wishlist  = Column(TEXT)
    newsletter  = Column(INTEGER(1), nullable = False, default = 0)
    address_id  = Column(INTEGER(11), nullable = False, default = 0)
    custom_field  = Column(TEXT, nullable=False)
    ip  = Column(VARCHAR(40), nullable = False)
    status  = Column(INTEGER(1), nullable = False)
    safe  = Column(INTEGER(1), nullable = False)
    token  = Column(TEXT, nullable= False)
    code  = Column(VARCHAR(40), nullable = False)
    date_added = Column(db.DateTime, nullable=False)
   

class CustomerActivity(db.Model):
    id = Column(INTEGER(11), primary_key=True, nullable=False)
    customer_id = Column(INTEGER(11), nullable=False)
    key = Column(VARCHAR(64), nullable=False)
    data = Column(TEXT, nullable= False)
    ip = Column(VARCHAR(40), nullable=False)
    date_added = Column(db.DateTime, nullable=False)


class CustomerAffiliate(db.Model):
    id = Column(INTEGER(11), primary_key=True, nullable=False)
    company = Column(VARCHAR(40), nullable=False)
    website = Column(VARCHAR(255), nullable= False)
    tracking = Column(VARCHAR(64), nullable= False)
    commission = Column(DECIMAL(4,2), nullable = False, default = 0.0)
    tax = Column(VARCHAR(64), nullable= False)
    payment = Column(VARCHAR(6), nullable= False)
    cheque = Column(VARCHAR(100), nullable= False)
    paypal = Column(VARCHAR(64), nullable= False)
    bank_name = Column(VARCHAR(64), nullable= False)
    bank_branch_number = Column(VARCHAR(64), nullable= False)
    bank_swift_code = Column(VARCHAR(64), nullable= False)
    bank_account_name = Column(VARCHAR(64), nullable= False)
    bank_account_number = Column(VARCHAR(64), nullable= False)
    custom_field  = Column(TEXT, nullable = False)
    status = Column(INTEGER(1), nullable= False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerApproval(db.Model):
    id  = Column(INTEGER(11),nullable = False, primary_key=True)
    customer_id  = Column(INTEGER(11), nullable= False)
    type = Column(VARCHAR(9), nullable= False)
    date_added  = Column(db.DateTime, nullable = False, default = datetime.utcnow)


class CustomerGroup(db.Model):
    id  = Column(INTEGER(11), nullable=False, primary_key=True)
    approval  = Column(INTEGER(1), nullable= False)
    sort_order  = Column(INTEGER(3), nullable= False)


class CustomerGroupDescription(db.Model):
    id  = Column(INTEGER(11), primary_key=True, nullable= False)
    language_id  = Column(INTEGER(11), nullable= False)
    name = Column(VARCHAR(32), nullable= False)
    description  = Column(TEXT, nullable = False)


class CustomerHistory(db.Model):
    id  = Column(INTEGER(11), primary_key = True, nullable = False)
    customer_id  = Column(INTEGER(11), nullable= False)
    comment  = Column(TEXT, nullable = False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerLogin(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key = True)
    email = Column(VARCHAR(96), nullable = False)
    ip = Column(VARCHAR(40), nullable = False)
    total = Column(INTEGER(4), nullable = False)
    date_added = Column(db.DateTime, nullable = False)
    date_modified = Column(db.DateTime, nullable = False)


class CustomerIp(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key = True)
    customer_id  = Column(INTEGER(11), nullable= False)
    ip = Column(VARCHAR(40), nullable= False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerOnline(db.Model):
    ip = Column(VARCHAR(40),primary_key=True, nullable= False)
    customer_id  = Column(INTEGER(11), nullable= False)
    url  = Column(TEXT, nullable = False)
    referer  = Column(TEXT, nullable = False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerReward(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key = True)
    customer_id  = Column(INTEGER(11), nullable = False, default = 0)
    order_id  = Column(INTEGER(11), nullable = False, default = 0)
    description  = Column(TEXT, nullable = False)
    points  = Column(INTEGER(8), nullable = False, default = 0)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerTransaction(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key=True)
    customer_id  = Column(INTEGER(11), nullable= False)
    order_id  = Column(INTEGER(11), nullable= False)
    description  = Column(TEXT, nullable = False)
    amount = Column(DECIMAL(15,4), nullable= False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerSearch(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key =True, unique =True)
    store_id  = Column(INTEGER(11), nullable= False)
    language_id  = Column(INTEGER(11), nullable= False)
    customer_id  = Column(INTEGER(11), nullable= False)
    keyword = Column(VARCHAR(255), nullable= False)
    category_id  = Column(INTEGER(11), nullable= False)
    sub_category = Column(INTEGER(1), nullable= False)
    description = Column(INTEGER(1), nullable= False)
    products  = Column(INTEGER(11), nullable= False)
    ip = Column(VARCHAR(40), nullable= False)
    date_added  = Column(db.DateTime, nullable = False)


class CustomerWishlist(db.Model):
    iid = Column(INTEGER(11), nullable=False, primary_key=True)
    product_id = Column(INTEGER(11), nullable=False, primary_key=True)
    date_added = Column(db.DateTime, nullable=False, default=datetime.utcnow)


# class CategoryDescription(db.Model):
#     id = Column(INTEGER(11), primary_key= True, nullable = False)
#     language_id = Column(INTEGER(11), nullable = False, primary_key= True)
#     name = Column(VARCHAR(255), nullable = False, key=True)
#     description = Column(TEXT, nullable = False)
#     meta_title = Column(VARCHAR(255), nullable = False)
#     meta_description = Column(VARCHAR(255), nullable = False)
#     meta_keyword = Column(VARCHAR(255), nullable = False)
#

class CategoryFilter(db.Model):
    category_id = Column(INTEGER(11), nullable = False, primary_key=True)
    filter_id = Column(INTEGER(11), nullable = False, primary_key=True)


class CategoryPath(db.Model):
    category_id = Column(INTEGER(11), nullable = False, primary_key=True)
    path_id = Column(INTEGER(11), nullable = False, primary_key=True)
    level = Column(INTEGER(11), nullable = False)


class CategoryToGoogleProductCategory(db.Model):
    id = Column(INTEGER(11), primary_key = True, nullable=False)
    google_product_category  = Column(VARCHAR(10), nullable = False)
    store_id = Column(INTEGER(11), nullable = False, default = 0, primary_key = True)
    category_id = Column(INTEGER(11), nullable = False, primary_key = True)


class CategoryToLayout(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key = True)
    store_id = Column(INTEGER(11), nullable = False, primary_key = True)
    layout_id = Column(INTEGER(11), nullable = False)


class CategoryToStore(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key=True)
    store_id = Column(INTEGER(11), nullable = False, primary_key=True)


class Order (db.Model):
  id  = Column(INTEGER(11), nullable = False, primary_key = True)
  invoice_no  = Column(INTEGER(11), nullable = False, default = 0)
  invoice_prefix  = Column(VARCHAR(26), nullable = False)
  store_id  = Column(INTEGER(11), nullable = False, default = 0)
  store_name  = Column(VARCHAR(64), nullable = False)
  store_url  = Column(VARCHAR(255), nullable = False)
  customer_id  = Column(INTEGER(11), nullable = False, default = 0)
  customer_group_id  = Column(INTEGER(11), nullable = False, default = 0)
  firstname  = Column(VARCHAR(32), nullable = False)
  lastname  = Column(VARCHAR(32), nullable = False)
  email  = Column(VARCHAR(96), nullable = False)
  telephone  = Column(VARCHAR(32), nullable = False)
  fax  = Column(VARCHAR(32), nullable = False)
  custom_field = Column(TEXT, nullable = False)
  payment_firstname  = Column(VARCHAR(32), nullable = False)
  payment_lastname  = Column(VARCHAR(32), nullable = False)
  payment_company  = Column(VARCHAR(60), nullable = False)
  payment_address_1  = Column(VARCHAR(128), nullable = False)
  payment_address_2  = Column(VARCHAR(128), nullable = False)
  payment_city  = Column(VARCHAR(128), nullable = False)
  payment_postcode  = Column(VARCHAR(10), nullable = False)
  payment_country  = Column(VARCHAR(128), nullable = False)
  payment_country_id  = Column(INTEGER(11), nullable = False)
  payment_zone  = Column(VARCHAR(128), nullable = False)
  payment_zone_id  = Column(INTEGER(11), nullable = False)
  payment_address_format = Column(TEXT, nullable = False)
  payment_custom_field = Column(TEXT, nullable = False)
  payment_method  = Column(VARCHAR(128), nullable = False)
  payment_code  = Column(VARCHAR(128), nullable = False)
  shipping_firstname  = Column(VARCHAR(32), nullable = False)
  shipping_lastname  = Column(VARCHAR(32), nullable = False)
  shipping_company  = Column(VARCHAR(40), nullable = False)
  shipping_address_1  = Column(VARCHAR(128), nullable = False)
  shipping_address_2  = Column(VARCHAR(128), nullable = False)
  shipping_city  = Column(VARCHAR(128), nullable = False)
  shipping_postcode  = Column(VARCHAR(10), nullable = False)
  shipping_country  = Column(VARCHAR(128), nullable = False)
  shipping_country_id  = Column(INTEGER(11), nullable = False)
  shipping_zone  = Column(VARCHAR(128), nullable = False)
  shipping_zone_id  = Column(INTEGER(11), nullable = False)
  shipping_address_format = Column(TEXT, nullable = False)
  shipping_custom_field = Column(TEXT, nullable = False)
  shipping_method  = Column(VARCHAR(128), nullable = False)
  shipping_code  = Column(VARCHAR(128), nullable = False)
  comment = Column(TEXT, nullable = False)
  total  = Column(DECIMAL(15,4), nullable = False, default = 0.0000)
  order_status_id  = Column(INTEGER(11), nullable = False, default = 0)
  affiliate_id  = Column(INTEGER(11), nullable = False)
  commission  = Column(DECIMAL(15,4), nullable = False)
  marketing_id  = Column(INTEGER(11), nullable = False)
  tracking  = Column(VARCHAR(64), nullable = False)
  language_id  = Column(INTEGER(11), nullable = False)
  currency_id  = Column(INTEGER(11), nullable = False)
  currency_code  = Column(VARCHAR(3), nullable = False)
  currency_value  = Column(DECIMAL(15,8), nullable = False, default = 1.00000000)
  ip  = Column(VARCHAR(40), nullable = False)
  forwarded_ip  = Column(VARCHAR(40), nullable = False)
  user_agent  = Column(VARCHAR(255), nullable = False)
  accept_language  = Column(VARCHAR(255), nullable = False)
  date_added = Column(db.DateTime, nullable = True, default= datetime.utcnow)
  date_modified = Column(db.DateTime, nullable = False, default= datetime.utcnow)


class OrderHistory(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key=True)
    order_id  = Column(INTEGER(11), nullable = False)
    order_status_id  = Column(INTEGER(11), nullable = False)
    notify = Column(INTEGER(1), nullable = False, default = 0)
    comment = Column(TEXT, nullable = False)
    date_added = Column(db.DateTime, nullable = False, default = datetime.utcnow)


class OrderOption(db.Model):
    id  = Column(INTEGER(11), nullable=True,primary_key=True)
    order_id  = Column(INTEGER(11), nullable = False)
    order_product_id  = Column(INTEGER(11), nullable = False)
    product_option_id  = Column(INTEGER(11), nullable = False)
    product_option_value_id  = Column(INTEGER(11), nullable = False, default = 0)
    name  = Column(VARCHAR(255), nullable = False)
    value = Column(TEXT, nullable = False)
    type  = Column(VARCHAR(32), nullable = False)


class OrderProduct(db.Model):
    id  = Column(INTEGER(11), primary_key = True, nullable = True)
    order_id = Column(INTEGER(11), nullable = False, primary_key=True)
    product_id = Column(INTEGER(11), nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    model = Column(VARCHAR(64), nullable = False)
    quantity  = Column(INTEGER(4), nullable = False)
    price  = Column(DECIMAL(15,4), nullable = False, default = 0.0000)
    total  = Column(DECIMAL(15,4), nullable = False, default = 0.0000)
    tax  = Column(DECIMAL(15,4), nullable = False, default = 0.0000)
    reward  = Column(INTEGER(8), nullable = False)


class OrderRecurring (db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key = True)
    order_id  = Column(INTEGER(11), nullable = False)
    reference  = Column(VARCHAR(255), nullable = False)
    product_id  = Column(INTEGER(11), nullable = False)
    product_name  = Column(VARCHAR(255), nullable = False)
    product_quantity  = Column(INTEGER(11), nullable = False)
    recurring_id  = Column(INTEGER(11), nullable = False)
    recurring_name  = Column(VARCHAR(255), nullable = False)
    recurring_description  = Column(VARCHAR(255), nullable = False)
    recurring_frequency  = Column(VARCHAR(25), nullable = False)
    recurring_cycle = Column(SMALLINT(6), nullable = False)
    recurring_duration = Column(SMALLINT(6), nullable = False)
    recurring_price = Column(DECIMAL(10,4), nullable = False)
    trial = Column(INTEGER(1), nullable = False)
    trial_frequency  = Column(VARCHAR(25), nullable = False)
    trial_cycle = Column(SMALLINT(6), nullable = False)
    trial_duration = Column(SMALLINT(6), nullable = False)
    trial_price = Column(DECIMAL(4,4), nullable = False)
    status = Column(INTEGER(4), nullable = False)
    date_added = Column(db.DateTime,default=datetime.utcnow, nullable = False)


class OrderRecurringTransaction(db.Model):
    id  = Column(INTEGER(11), nullable = False, primary_key = True)
    order_recurring_id  = Column(INTEGER(11), nullable = False)
    reference  = Column(VARCHAR(255), nullable = False)
    type  = Column(VARCHAR(255), nullable = False)
    amount = Column(DECIMAL(10,4), nullable = False)
    date_added = Column(db.DateTime, nullable = False, default = datetime.utcnow)


class OrderShipment(db.Model):
    id  = Column(INTEGER(11), primary_key= True, nullable=False)
    order_id  = Column(INTEGER(11), nullable = False)
    date_added = Column(db.DateTime, nullable = False,default = datetime.utcnow)
    shipping_courier_id  = Column(VARCHAR(255), nullable = False, default = 0)
    tracking_number  = Column(VARCHAR(255), nullable = False, default = 0)


class Cart(db.Model):
    id = Column(INTEGER(11), nullable=True, primary_key = True)
    api_id = Column(INTEGER(11), nullable = True)
    customer_id = Column(INTEGER(11), nullable = False)
    session_id  = Column(VARCHAR(32), nullable = True)
    product_id = Column(INTEGER(11), nullable = False)
    seller_id = Column(INTEGER(11), ForeignKey('sellers.id'), nullable = False)
    recurring_id = Column(INTEGER(11), nullable = True)
    option = Column(TEXT, nullable = True)
    quantity = Column(INTEGER(5), nullable = False)
    date_added = Column(db.DateTime, nullable=False, default = datetime.utcnow)


class Category(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key = True)
    image  = Column(VARCHAR(255), nullable = True)
    parent_id = Column(INTEGER(11), nullable = False, default = 0)
    top  = Column(INTEGER(1), nullable = False)
    column = Column(INTEGER(3), nullable = False)
    sort_order = Column(INTEGER(3), nullable = False, default = 0)
    status  = Column(INTEGER(1), nullable = False)
    date_added  = Column(db.DateTime, nullable=False)
    date_modified  = Column(db.DateTime, nullable=False)


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(INTEGER(11), primary_key=True, nullable = False)
    seller_id = Column(INTEGER(11), db.ForeignKey('sellers.id'), nullable=False)
    # describe= db.relationship('ProductDescription', backref='describe', lazy=True)
    model = Column(VARCHAR(64), nullable = False)
    sku = Column(VARCHAR(64), nullable = False)
    upc = Column(VARCHAR(12), nullable = False)
    ean = Column(VARCHAR(14), nullable = False)
    jan = Column(VARCHAR(13), nullable = False)
    isbn = Column(VARCHAR(17), nullable = False)
    mpn = Column(VARCHAR(64), nullable = False)
    location = Column(VARCHAR(128), nullable = False)
    quantity  = Column(INTEGER(4), nullable = False, default = 0)
    stock_status_id  = Column(INTEGER(11), nullable = False)
    image = Column(VARCHAR(255), nullable= True)
    manufacturer_id  = Column(INTEGER(11), nullable = False)
    shipping  = Column(INTEGER(1), nullable = False, default = 1)
    price  = Column(DECIMAL(15,4), nullable = False, default = 0.0000)
    points  = Column(INTEGER(8), nullable = False, default = 0)
    tax_class_id  = Column(INTEGER(11), nullable = False)
    date_available = Column(DATE, nullable = False, default = 0000-00-00)
    weight  = Column(DECIMAL(15,8), nullable = False, default = 0.00000000)
    weight_class_id  = Column(INTEGER(11), nullable = False, default = 0)
    length  = Column(DECIMAL(15,8), nullable = False, default = 0.00000000)
    width  = Column(DECIMAL(15,8), nullable = False, default = 0.00000000)
    height  = Column(DECIMAL(15,8), nullable = False, default = 0.00000000)
    length_class_id  = Column(INTEGER(11), nullable = False, default = 0)
    subtract  = Column(INTEGER(1), nullable = False, default = 1)
    minimum  = Column(INTEGER(11), nullable = False, default = 1)
    sort_order = Column(INTEGER(11), nullable = False, default = 0)
    status  = Column(INTEGER(1), nullable = False, default = 0)
    viewed = Column(INTEGER(5), nullable = False, default = 0)
    date_added = Column(db.DateTime, nullable = False)
    date_modified = Column(db.DateTime, nullable = False)
    #   PRIMARY KEY (product_id)
    # ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


class ProductDescription(db.Model): 
    id = Column(INTEGER(11), nullable=False, primary_key = True)
    language_id = Column(INTEGER(11), ForeignKey("language.id"), nullable=False)
    product_id = Column(INTEGER(11), ForeignKey("products.id"), nullable=False, unique = True)
    name = Column(VARCHAR(250), nullable=False)
    description = Column(TEXT, nullable=False)
    tag = Column(TEXT, nullable=False)
    meta_title = Column(VARCHAR(255), nullable=False)
    meta_description = Column(VARCHAR(255), nullable=False)
    meta_keyword = Column(VARCHAR(255), nullable=False)
    
    def __repr__(self):
        data = {
            'name':self.name,
            'description': self.description
        }
        return f'{data}'

    
class language(db.Model):
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(32), nullable=False)
    code = Column(VARCHAR(5), nullable=False)
    locale = Column(VARCHAR(255), nullable=False)
    image = Column(VARCHAR(64), nullable=False)
    directory = Column(VARCHAR(32), nullable=False)
    sort_order = Column(INTEGER, nullable=False, default=0)
    status = Column(INTEGER(1), nullable=False)


# class Category(db.Model):
#     id = Column(INTEGER(11), primary_key=True, nullable=False)
#     image = Column(VARCHAR(255), nullable = True, default = "NULL")
#     parent_id = Column(INTEGER(11), nullable=True, default='0')
#     top = Column(INTEGER(1), nullable = True)
#     column = Column(INTEGER(3), nullable = False)
#     sort_order = Column(INTEGER(3), nullable = True, default='0')
#     status = Column(INTEGER(1), nullable=True)
#     date_added = Column(db.DateTime, nullable=False, default= datetime.utcnow)
#     date_modified = Column(db.DateTime, nullable = False, default = '00-00-0000')
    
    
class CategoryDescription(db.Model):
    id = Column(INTEGER(11), nullable = False, primary_key = True)
    category_id = Column(INTEGER(11), ForeignKey('category.id'), nullable = False)
    language_id = Column(INTEGER(11), nullable = False)
    name = Column(VARCHAR(255), nullable = False)
    description = Column(TEXT, nullable = False)
    meta_title = Column(VARCHAR(255), nullable = True)
    meta_description = Column(VARCHAR(255), nullable = False)
    meta_keyword = Column(VARCHAR(255), nullable = False)

    
      