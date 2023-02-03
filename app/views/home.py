from flask import Blueprint, render_template, redirect, url_for

from ..init_db import init_db
from ..app import db, cur
from ..db_handler import sql2user

from ..models import Auction

bp = Blueprint('bp_home', __name__)

@bp.route('/')
def home_get():
    # init_db()
    # cur.execute('SELECT * FROM users;')
    # dictionary = sql2user(cur.fetchall())
    # print(dictionary[1]['name'])

    import datetime
    list_of_auctions = [Auction(i, 1, i, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1), 100*i, f"Example {i}", "desc", "link") for i in range(50)]

    return render_template('gallery.html', auctions=list_of_auctions)