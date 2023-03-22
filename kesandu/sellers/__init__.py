from flask import Blueprint
import click 

bp = Blueprint('sellers',
               __name__, 
               template_folder='templates', 
               static_folder='static',
               static_url_path='/sellers/static')

@bp.cli.command('create_demo_user')
@click.argument('name')
def create_demo_seller(name):
    # Make demo_seller is_active = 0
    print("Working")
    
    
from kesandu.sellers import routes