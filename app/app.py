from flask import Flask, flash, render_template, redirect, url_for, session
from werkzeug.debug import DebuggedApplication
from flask_login import LoginManager

from app.database import db
from app.test_data import insert_test_data
from app.init_db import init_db

cur = db.cursor()


def create_app():
    init_db()
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )

    # Load config from file config.py
    app.config.from_pyfile('config.py')

    insert_test_data()

    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    login_manager = LoginManager()
    login_manager.login_view = 'bp_auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (user_id,))
        result = cur.fetchone()
        try:
            user = User(*result)
        except IndexError:
            user = None
        return user

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page!')
        return redirect(url_for('bp_auth.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 500

    # Register blueprints (views)
    from .views.example import bp as bp_example
    app.register_blueprint(bp_example)

    from .views.home import bp as bp_home
    app.register_blueprint(bp_home)

    from .views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from .views.auctions import bp as bp_auctions
    app.register_blueprint(bp_auctions)

    # for localhost only
    app.run()
