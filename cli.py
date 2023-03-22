import click
from flask.cli import AppGroup
from kesandu import app

user_cli = AppGroup('user')

# @app.cli.command("create-user")
@user_cli.command('create')
@click.argument("name")
def create_user(name):
    print("Hello world cli")
    

app.cli.add_command(user_cli)