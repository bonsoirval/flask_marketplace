from kesandu.frontend.models import User
from flask import Blueprint
from kesandu import db
import click


bp = Blueprint('frontend',
               __name__, 
               template_folder='templates', 
               static_folder='static',
               static_url_path='/frontend/static')

@bp.cli.command('create_demo_user')
@click.argument('name')
def create_demo_user(name):
    # Make demo_seller is_active = 0
    username = "user@example.com"
    password = 'user@example.com'
    user = User(username=username, name = name)
    user.set_password(password) 
    db.session.add(user)
    db.session.commit()
    print("Default user created successfully")
    print(f"Username: {username} \nPassword: {password}")

@bp.cli.command('test_code')
@click.argument('value')
def test_code(value = 'nothing really'):
    import os
    from flask import current_app as app, send_from_directory
    basedir = os.path.abspath(os.path.dirname(app.config['SELLERS_PRODUCT']))
    product = 'catalog/demo/htc_touch_hd_1.jpg'.split('/')[-1]
    # image = basedir + "/" + product
    
    print(f"Basedir : {basedir}")
    print(f"Product : {product}")
    # print(f"Image : {image}")
        
from kesandu.frontend import routes
