from flask import Blueprint

bp = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')

from kesandu.frontend import routes
