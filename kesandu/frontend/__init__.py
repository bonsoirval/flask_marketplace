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
        
from kesandu.frontend import routes
