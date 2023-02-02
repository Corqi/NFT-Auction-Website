from flask import Flask, flash, redirect, url_for, session
from werkzeug.debug import DebuggedApplication
from flask_login import LoginManager
import psycopg2
import app.config

db = psycopg2.connect(
    host=app.config.DB_HOST,
    database=app.config.DB_NAME,
    user=app.config.DB_USER,
    password=app.config.DB_PASSWORD
)
cur = db.cursor()


def create_app():
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )

    # Load config from file config.py
    app.config.from_pyfile('config.py')

    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    # todo ustawienie połączenie z bazą danych / mailem
    # # Setup database connection using standard pattern mysql://user:password@host/dbname
    # app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
    #                                          f"@{app.config['DB_HOST']}/{app.config['DB_NAME']}")
    # db.init_app(app)
    # mail.init_app(app)
    #
    # login_manager = LoginManager()
    # login_manager.login_view = 'bp_auth.login_get'
    # login_manager.init_app(app)
    #
    # from .models import User
    #
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))
    #
    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     session.pop('_flashes', None)
    #     flash('Please log in to access this page!')
    #     print(login_manager.blueprint_login_views)
    #     return redirect(url_for('bp_auth.login_get'))
    #
    # with app.app_context():
    #     db.create_all()
    #     db.session.commit()
    # todo koniec bloku

    # Register blueprints (views)
    from .views.example import bp as bp_example
    app.register_blueprint(bp_example)

    # todo strona 404
    # Register errors
    # from .views.errors import page_not_found
    # app.register_error_handler(404, page_not_found)
    # todo koniec bloku

    # for localhost only
    app.run()
