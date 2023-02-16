from flask import Blueprint

bp = Blueprint('frontend',
               __name__, 
               template_folder='templates', 
               static_folder='static',
               static_url_path='/frontend/static')

from kesandu.frontend import routes
