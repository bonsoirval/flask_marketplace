from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session,logging, jsonify,\
    current_app as app, send_from_directory, Response
from flask_login import current_user, login_required
from kesandu import db
from kesandu.frontend.forms import OrderForm 
from kesandu.frontend import bp
from kesandu.frontend.models import Product, Cart, Category, ProductDescription
from sqlalchemy.sql.expression import func # for random selection of items
from sqlalchemy import text, select, or_, and_, not_, join
from datetime import datetime
import pandas as pd 
import os
from config import Config

session = db.session

# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
    # g.locale = str(get_locale())

@bp.route('/load_image/<image>')
def fe_load_image(image):
    return send_from_directory(app.config['SELLER_PRODUCT_PATH'], image)
    
@bp.route('/ajax')
def fe_ajax():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

# @bp.route('/ajax_index')
# def ajax_index():
#     return render_template('dummy/ajax_index.html')

@bp.route("/my_cart", methods = ["GET", "POST"])
def fe_my_cart():
    # Show current user cart
    stmt = text("SELECT c.customer_id, c.product_id, c.seller_id, c.quantity,\
        p.price, p.image, pdesc.name \
            FROM cart AS c \
                JOIN products p  ON p.id = c.product_id \
                    JOIN product_description pdesc ON p.id = pdesc.product_id \
                        WHERE c.customer_id = :customer_id")
    stmt = stmt.bindparams(customer_id = current_user.id) # , pdesc_id = product_id)
    cart = db.engine.execute(stmt).all()
    
    price = text("SELECT SUM(p.price * c.quantity) as total FROM products AS p \
                JOIN cart AS c  ON p.id = c.product_id \
                        WHERE c.customer_id = :customer_id")
    price = price.bindparams(customer_id = current_user.id) # , pdesc_id = product_id)
    total_price = db.engine.execute(price).all()
    
    data = {
        'title' : 'Page title',
        'cart': cart,
        'total' : total_price
    }
    return render_template('frontend/cart.html', data = data) 

@bp.route('/add_to_cart/', methods=['GET', 'POST'])
def fe_cart():
    seller_id = request.args.get('seller_id', 0, type=int)
    product_id = request.args.get('product_id', 0, type=int)
    quantity = request.args.get('quantity', 1, type=int)
    user_id = request.args.get('user_id', 0, type=int)
    
    cart = Cart(customer_id = user_id, seller_id = seller_id, quantity = quantity, product_id = product_id, date_added = datetime.utcnow())
    db.session.add(cart)
    db.session.commit()
    
    return jsonify(result= True) # f"{result}") # : {product_id} : {quantity} : {user_id}'  )

# method to handle all insert operations
def insert(table, columns, values):
    result = db.engine.execute( "INSERT INTO {table} ( {columns} ) VALUES ( {values} )".format(table,columns, values))
    return result

@bp.route('/category/<category>', methods=['GET'])
def fe_category(category):
    products = Product.query.filter_by(category=category).order_by(func.rand()).limit(3).all()
    x = ''
    if category == 'agro':
        category = 'Agro Produce'
    elif category == 'organic_skin_care':
        category = "Organic Skin Care"
    elif category == 'organic_hair_care':
        category = 'Organic Hair Care'
    
    title = f"Kesandu {category} products"
    return render_template('frontend/category.html', x=x,title=title, products=products, category=category)

@bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def fe_product(product_id):
    stmt = text("SELECT p.id, p.seller_id, p.model, p.sku, p.upc, p.ean, p.jan, p.isbn, p.mpn,\
        p.location, p.quantity, p.stock_status_id, p.image, p.manufacturer_id, p.shipping, \
            p.price, p.points, p.tax_class_id,  p.date_available, p.weight, p.weight_class_id, \
                p.length, p.width, p.height, p.length_class_id, p.subtract,p.minimum, \
                    p.sort_order, p.status, p.viewed, p.date_added, p.date_modified, \
                        pdesc.language_id, pdesc.name, pdesc.description, pdesc.tag, \
                            pdesc.meta_title, pdesc.meta_description, pdesc.meta_keyword \
                                FROM products AS p, product_description AS pdesc\
                                    WHERE p.id = :p_id AND pdesc.product_id = :pdesc_id")
    stmt = stmt.bindparams(p_id = product_id, pdesc_id = product_id)
    product = db.engine.execute(stmt).first()
    data = {
        'description':"description", 
        'keywords' : "keywords",
        'product' : product,
        'title' : "Kesandu Organic Shop"
    }
    
    
    category_nav = text("SELECT c.id, c.parent_id, c.sort_order, cd.id, cd.name \
        FROM category AS c \
        JOIN category_description AS cd \
            ON cd.category_id = c.id \
            GROUP BY cd.name \
                ORDER BY cd.id")
    # \
    #         ON category.parent_id = category_description.id")
    # categories_nav = db.engine.execute(category_nav)
    cat_df = pd.read_sql(con = db.engine , sql = category_nav)
    categories_nav = [{'category_id': i[0:][0], 'parent_name':i[0:][4] } for i in cat_df[cat_df['parent_id'] == 0].values]
    
    return render_template('frontend/view_product.html', data = data, categories_nav = categories_nav) # description =  product.description, keywords = product.meta_title, title = product.meta_title, product=product, x= ' x ')
    
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def fe_index():
    # Working scripts
    # stmt = text("SELECT * FROM products \
    #     JOIN product_description \
    #         ON products.id = product_description.product_id ORDER BY products.price ASC") #  WHERE id = :x") 
    # # stmt = stmt.bindparams(x = 48)
    # product = db.engine.execute(stmt)
    product = Product.query.all()
    title = "Kesandu Organics" #app.config['APP_NAME']
    data = {
        'description':"description", 
        'keywords' : "keywords",
        'products' : product,
        'title' : "Kesandu Organic Shop"
    }
    # return render_template('dummy/mock.html', data = data)
    return render_template('frontend/home.html', data = data) #products=product, title = title, description = "description", keywords = "keywords")
     
# Run raw sql from flask_sqlalchemy
@bp.route('/test_sql')
def run_sql():
    db.engine.execute(
        '''        
        INSERT INTO `layout` (`id`, `name`) VALUES
        (1, 'Home'),
        (2, 'Product'),
        (3, 'Category'),
        (4, 'Default'),
        (5, 'Manufacturer'),
        (6, 'Account'),
        (7, 'Checkout'),
        (8, 'Contact'),
        (9, 'Sitemap'),
        (10, 'Affiliate'),
        (11, 'Information'),
        (12, 'Compare'),
        (13, 'Search');
        '''
    )
    
@bp.app_template_filter()
def cageory_nav(value, locaton = 'left'):
    print("Hello")
    return 'left_cageory_nav'

@bp.app_template_filter()
def add_total(item_1, item_2):
    return item_1 + item_2

@bp.app_template_filter()
def nav_bar(name):
    # {# /////////// Navigations //////////// #}
    """{% for i in parents %}
        Parent : {{i}}<br/>
        {% for j in children %}
            {% if i.category_id == j.parent_id%}
                Child : {{j | lower }}<br/>
            {% endif %}
        {% endfor %}
        <br/>
    {% endfor %}
    <br/>
    """
    return f"Hello {name}"

# get categories
@bp.route('/cats')
def fe_cats():
    query = text("SELECT c.id, c.parent_id, c.sort_order, cd.id, cd.name \
        FROM category AS c \
        JOIN category_description AS cd \
            ON cd.category_id = c.id \
            GROUP BY cd.name \
                ORDER BY cd.id")
    # \
    #         ON category.parent_id = category_description.id")
    categories = db.engine.execute(query)
    cat_df = pd.read_sql(con = db.engine , sql = query)
    parents = [{'category_id': i[0:][0], 'parent_name':i[0:][4] } for i in cat_df[cat_df['parent_id'] == 0].values]
    children = [{'category_id':i[0:][0],'parent_id':i[0:][1], 'child_name':i[0:][4] } for i in cat_df[cat_df['parent_id'] > 0].values] # cat_df[cat_df['parent_id'] > 0]['id']
    
                
    # return f"{categories}"
    return render_template("frontend/mock.html", stmt = categories, \
        parents = parents, children = children, cat_df = cat_df,\
            df = dict(cat_df))
       
@bp.route('/search')    
def fe_search():
    q = request.args.get('q', 'nothing')
    # Working scripts
    # '%' attention to spaces
    # query_sql = """SELECT * FROM product_description WHERE name CONTAIN :name"""

    # # db is sqlalchemy session object
    # tags_res_list = db.engine.execute(text(query_sql), {"name": q}).fetchall()
    search = "%{}%".format(q)
    
    product = ProductDescription.query.filter(or_(
            ProductDescription.name.like(search),
            ProductDescription.description.like(search)
        )
    ).all()
    data = {
        'description':"description", 
        'keywords' : "keywords",
        'products' : product,
        'title' : "Organic Shop"
    }
    
    # return render_template('dummy/mock.html', result = tags_res_list)
    return render_template('frontend/home.html', data = data)

    