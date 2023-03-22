from kesandu.sellers import bp
from flask import render_template, request, flash, redirect, url_for, session
from kesandu.sellers.forms import SellersLoginForm, RegistrationForm
from werkzeug.urls import url_parse
from kesandu.sellers.models import Seller
from kesandu import db 
from kesandu.sellers import catalog
from flask_login import login_user, login_required, logout_user, current_user


# @bp.route('/sellers/categories', methods=['GET', 'POST'])
# # @seller_required
# def categories():
#     return 'categories'

@bp.route("/sellers")
@bp.route("/sellers/")
@bp.route("/sellers/index")
# overwrite this function for sellers so that it will send sellers to sellers' 
# login page
@login_required 
def s_home():
    data = {
        'title': 'Sellers Home',
    }
    return render_template('sellers/s_home.html', data=data)

@bp.route("/sellers/login", methods =['POST', 'GET'])
def s_login():
    if current_user.is_authenticated:
        return redirect(url_for("sellers.s_home"))
    
    # login form object   
    login_form = SellersLoginForm()
    if login_form.validate_on_submit():
        seller = Seller.query.filter_by(username=login_form.username.data).first()
        if seller is None or not seller.check_password(login_form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('sellers.s_login'))
        login_user(seller, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('sellers.s_home')
        return redirect(next_page)
    data = {
        'title' : "Sellers Home",
        'form' : login_form
    }
    return render_template('sellers/s_login.html',data=data)

@bp.route('/sellers/logout')
def s_logout():
    logout_user()
    return redirect(url_for('sellers.s_login')) 
   
@bp.route('/sellers/register', methods=['GET', 'POST'])
def s_register():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        seller = Seller(firstName=form.username.data,mobile=0,type='nothing', confirmCode="none for now", address='address to be filled', lastName=form.username.data, username=form.username.data, email=form.email.data)
        seller.set_password(form.password.data)
        db.session.add(seller)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('sellers.s_login'))
    page_data = {
            'title':'Register'
        }
    return render_template('sellers/auth/s_register.html', data = page_data, form = form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('frontend.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

