from flask import Blueprint, render_template, redirect, url_for
from ..app import db, cur
from ..db_handler import sql2user
from app.models import User, Auction, History

bp = Blueprint('bp_example', __name__)


@bp.route('/example')
def example_get():
    # init_db()
    # cur.execute('SELECT * FROM users WHERE uid=(%s);', (1,))
    # users = sql2user(cur.fetchall())
    # users[0].update()
    # new_user = User(username='basia123', password='pass', email='basia@gmail.com', name='basia')
    # new_user.add()


    return render_template('gallery.html')

