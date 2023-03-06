# for class based views
from flask.views import View

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import current_user, login_required, logout_user, login_user
from kesandu.sellers.models import Seller
from kesandu import db
from kesandu.sellers import bp

    
    
@bp.route('/sellers', methods=['GET', 'POST'])
@bp.route('/sellers/index', methods=['GET', 'POST'])
def sellers_index():
    return "Worked"

@bp.route('/sellers/create', methods=['GET', 'POST'])
def sellers_create():
    return 'wanna register'