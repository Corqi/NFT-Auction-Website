from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from ..init_db import init_db
from ..app import db, cur
from ..db_handler import sql2user

from app.models import Auction
from app.forms import NewAuctionForm

import datetime

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    # init_db()
    # cur.execute('SELECT * FROM users;')
    # dictionary = sql2user(cur.fetchall())
    # print(dictionary[1]['name'])

    # Creating some auction for test
    # import datetime
    # list_of_auctions = [Auction(i, 1, i, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1), 100*i, f"Example {i}", "desc", "link") for i in range(50)]

    list_of_auctions = []
    cur.execute('SELECT * FROM auction_items WHERE auction_end > (%s);', (datetime.datetime.now(),))
    for auction in cur.fetchall():
        list_of_auctions.append(Auction(*auction))

    return render_template('gallery.html', auctions=list_of_auctions, user=current_user)


@bp.route('/new', methods=['POST', 'GET'])
def new_item_get():
    form = NewAuctionForm()
    if form.validate_on_submit():
        # TODO protect from sql injection
        auction_end = datetime.datetime.combine(form.auction_end.data, form.auction_end_time.data)
        new_auction = Auction(uid=current_user.get_id(), bid=current_user.get_id(), auction_start=datetime.datetime.now(), auction_end=auction_end, price=form.price.data, name=form.name.data, desc=form.description.data, link=form.img_link.data)
        new_auction.add()
        return redirect(url_for('bp_home.home_get'))

    return render_template('newAuction.html', form=form, user=current_user)