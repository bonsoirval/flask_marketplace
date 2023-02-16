#!/var/www/webenv/bin/python3
# usr/bin/python3
import sys 
import logging 

activate_this = '/var/webenv/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, '/var/www/kesandu/')

from kesandu import create_app, db #, cli
from kesandu.models import User #, Post

application = create_app()
# cli.register(application )

@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}  # , 'Post': Post}


application.secret_key = "kesandu_4&)lk^o!d5#rw4k$hnzk-4r(sv!%7h6@+%(w51@)!83+1!sb8"

logging.basicConfig(stream=sys.stderr) 
