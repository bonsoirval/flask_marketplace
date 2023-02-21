from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session,logging, jsonify, current_app
from flask_login import current_user, login_required
from kesandu import db
from kesandu.frontend.forms import OrderForm 
from kesandu.frontend import bp
from kesandu.frontend.models import Product, Cart
from sqlalchemy.sql.expression import func # for random selection of items


# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
    # g.locale = str(get_locale())

@bp.route('/ajax')
def fe_ajax():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@bp.route('/ajax_index')
def ajax_index():
    return render_template('dummy/ajax_index.html')


@bp.route('/add_to_cart/')
def fe_cart():
    seller_id = request.args.get('seller_id', 0, type=int)
    product_id = request.args.get('product_id', 0, type=int)
    quantity = request.args.get('quantity', 0, type=int)
    user_id = request.args.get('user_id', 0, type=int)
    # return seller_id + product_id + quantity
    
    # confirm there is enough product available to be added to cart
    cart = Product.query.filter_by(id = prodcut_id).filter_by(available >= quantity).first()
    # if enough product, add to cart
    
	# api_id	
	# user_id
	# session_id
	# product_id	
	# recurring_id
	# option	text
	# quantity
	# date_added	
 
    cart = Cart(user_id=user_id, seller_id=seller_id, product_id=product_id, quantity=quantity)
    db.session.add(cart)
    db.session.commit()
    
    return jsonify(result= 'your cart add')
    
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

@bp.route('/tshirt', methods=['GET', 'POST'])
def tshirt():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        return render_template('tshirt.html', tshirt=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        # print('Execution time: ' + str(execution_time) + ' usec')
        if 'uid' in session:
            uid = session['uid']
            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM product_view WHERE user_id=%s AND product_id=%s", (uid, product_id))
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                            (now_time, uid, product_id))
            else:
                cur.execute("INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)", (uid, product_id))
                mysql.connection.commit()
        return render_template('view_product.html', x=x, tshirts=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('tshirt.html', tshirt=products, form=form)


@bp.route('/product/<category>/<int:product_id>', methods=['GET', 'POST'])
def fe_product(category, product_id):
    form = OrderForm(request.form)
    product = Product.query.filter_by(id=product_id).all()
    x = '' # x is empty just to get going for now
    
    item = [item.product_name for item in product]
    title = f"{item} from Kesandu"
    
    # this is a mock keywords
    keywords = product[0].description.split(' ')
    
    description = product[0].description
    return render_template('frontend/view_product.html',description = description, keywords = keywords, title=title, products=product, x=x)
    
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def fe_index():
    form = OrderForm(request.form)
    product = Product.query.all()
    agro = Product.query.filter_by(category='agro').order_by(func.rand()).limit(4).all()
    organic_skin_care = Product.query.filter_by(category='organic_skin_care').order_by(func.rand()).limit(4).all()
    organic_hair_care = Product.query.filter_by(category='organic_hair_care').order_by(func.rand()).limit(4).all()
    seedlings = Product.query.filter_by(category='seedling').order_by(func.rand()).limit(4).all()
    
    # return render_template('dummy/test.html', product=organic_skin_care)
    return render_template(
        'frontend/home.html', 
        agro=agro, 
        organic_skin_care=organic_skin_care,
        organic_hair_care=organic_hair_care,
        seedlings=seedlings)


