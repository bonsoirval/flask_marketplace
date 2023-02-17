from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from kesandu import db
from kesandu.frontend.forms import OrderForm 
from kesandu.frontend import bp
from kesandu.frontend.models import Product
from sqlalchemy.sql.expression import func # for random selection of items


# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
    # g.locale = str(get_locale())

@bp.route('/register', methods=['GET', 'POST'])
def fe_register():
    return 'register'

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


