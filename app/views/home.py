from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.app import cur

from app.models import Auction
from app.forms import NewAuctionForm

import datetime

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    list_of_auctions = []
    cur.execute(
        'SELECT a.aid, a.uid, a.bid, a.auction_start, a.auction_end, a.price, a.name, a.desc, a.link, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items a '
        'JOIN users u ON u.uid = a.uid '
        'LEFT JOIN bidding_history b ON a.aid = b.aid '
        'WHERE auction_end > (%s)'
        'GROUP BY a.aid, u.username;', (datetime.datetime.now(),)
    )
    for auction in cur.fetchall():
        list_of_auctions.append(Auction(*auction))

    return render_template('gallery.html', auctions=list_of_auctions, user=current_user)


@bp.route('/new', methods=['POST', 'GET'])
def new_auction():
    form = NewAuctionForm()
    if form.validate_on_submit():
        # TODO protect from sql injection
        auction_end = datetime.datetime.combine(form.auction_end.data, form.auction_end_time.data)
        new_auction = Auction(uid=current_user.get_id(), bid=current_user.get_id(), auction_start=datetime.datetime.now(), auction_end=auction_end, price=form.price.data, name=form.name.data, desc=form.description.data, link=form.img_link.data)
        new_auction.add()
        return redirect(url_for('bp_home.home_get'))

    return render_template('newAuction.html', form=form, user=current_user)