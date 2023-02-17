from kesandu import create_app, db, cli
from kesandu.frontend.models import User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User} # , 'Post': Post}
