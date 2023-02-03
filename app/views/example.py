from flask import Blueprint, render_template, redirect, url_for
from ..init_db import init_db
from ..app import db, cur
from ..db_handler import sql2user

bp = Blueprint('bp_example', __name__)


@bp.route('/example')
def example_get():
    # init_db()
    cur.execute('SELECT * FROM users;')
    dictionary = sql2user(cur.fetchall())
    print(dictionary[1]['name'])

    return render_template('gallery.html')

