from flask import Blueprint

bp = Blueprint('sellers',
               __name__, 
               template_folder='templates', 
               static_folder='static')

from kesandu.sellers import routes
