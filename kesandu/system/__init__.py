from flask import Blueprint

bp = Blueprint('system',
               __name__, 
               template_folder='templates', 
               static_folder='static',
               static_url_path='/frontend/static')

from kesandu.system import routes
