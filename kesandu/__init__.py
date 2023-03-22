import logging
import os
from jinja2 import StrictUndefined
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
# from flask_authorize import Authorize
from flask_session import Session


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
# authorize = Authorize()
# Session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    # Use config class as config object
    app.config.from_object(config_class)
    # app.jinja_env.undefined = StrictUndefined
        
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    # authorize.init_app(app)
    # Session.init_app(app)

    # Errors
    # from kesandu.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)
    
    # frontend
    from kesandu.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp)
    
    # Auth 
    from kesandu.auth import bp as authbp
    app.register_blueprint(authbp, url_prefix='/auth')
    
    # sellers
    from kesandu.sellers import bp as sellers_bp
    app.register_blueprint(sellers_bp, url_prefi='/sellers')

    # Admin
    from kesandu.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefi='/admin')
    
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=app.config['APP_NAME'] + ' Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # if not os.path.exists('logs'):
        #     os.system('mkdir logs')
        # file_handler = RotatingFileHandler('logs/' + app.config['APP_NAME'] + '.log',
        #                                    maxBytes=10240, backupCount=10)
        # file_handler.setFormatter(logging.Formatter(
        #     '%(asctime)s %(levelname)s: %(message)s '
        #     '[in %(pathname)s:%(lineno)d]'))
        # file_handler.setLevel(logging.INFO)
        # app.logger.addHandler(file_handler)

        # app.logger.setLevel(logging.INFO)
        # app.logger.info(app.config['APP_NAME'] + ' startup')
    
 
    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from kesandu.frontend import models
