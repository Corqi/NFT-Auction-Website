from flask import Blueprint, render_template, redirect, url_for, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from app.forms import LoginForm, RegistrationForm

bp = Blueprint('bp_auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # TODO check if there is a user with such an email in the database
        user = None     # get user from db
        if user:
            flash(Markup(f'Email address already exists. Go to <a class="danger-link" href="{url_for("bp_auth.login")}">login page</a>.'),
                  'error')
            return redirect(url_for('bp_auth.register'))

        # TODO create new user
        # new_user = Usear(email=email,
        #                 pw_hash=generate_password_hash(password, method='sha256', salt_length=8)
        #                 )
        new_user = None

        # TODO add new_user to db
        flash('Your account has been created you can now log in')
        return redirect(url_for('bp_auth.login'))

    return render_template('register.html', form=form, user=current_user)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp_home.home_get'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = None     # TODO get user from db

        if not user:    # or not check_password_hash(user.pw_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('bp_auth.login'))

        login_user(user)
        return redirect(url_for('bp_home.home_get'))

    return render_template('login.html', form=form, user=current_user)


@login_required
@bp.route('/logout')
def logout_get():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('bp_auth.login'))