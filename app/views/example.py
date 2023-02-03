import datetime

from flask import Blueprint, render_template, redirect, url_for
from ..app import db, cur
from ..db_handler import sql2user
from app.models import User, Auction, History
from ..init_db import init_db

bp = Blueprint('bp_example', __name__)


@bp.route('/example')
def example_get():
    # init_db()
    # cur.execute('SELECT * FROM users WHERE uid=(%s);', (1,))
    # users = sql2user(cur.fetchall())
    # users[0].update()
    # new_user = User(username='basia123', password='pass', email='basia@gmail.com', name='basia')
    # new_user.add()
    # new_auction = Auction(uid=1, bid=1, auction_start=datetime.datetime.now(),
    #                       auction_end=datetime.datetime(2024, 11, 6, 14, 36, 56),
    #                       price=134, name='monke9', desc='monke4',
    #                       link='https://play-lh.googleusercontent.com/T_vA5l9W1-XYTmgr3gCB2MBd7QmA-iG0wcm09_IFWNB-4gOpnS-tYNEmcalwdixSyw')
    # new_auction.add()
    # new_bid = History(aid=1, bid=1, price=700)
    # new_bid.add()
    return render_template('gallery.html')
