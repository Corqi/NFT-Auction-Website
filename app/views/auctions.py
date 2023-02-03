import datetime

from flask import Blueprint, render_template, redirect, url_for

from app.app import cur
from app.db_handler import sql2auction, sql2history
from app.dtos import map_history_dto
from app.forms import BiddingForm

bp = Blueprint('bp_auctions', __name__)


@bp.route('/auctions')
def get_all_auctions():
    cur.execute('SELECT * FROM auction_items;')
    auctions = sql2auction(cur.fetchall())
    return render_template('gallery.html', auctions=auctions)


@bp.route('/auction/<int:auction_id>')
def get_auction(auction_id):
    form = BiddingForm()
    if form.validate_on_submit():
        price = form.price.data
    cur.execute('SELECT * FROM auction_items WHERE aid=(%s);', (auction_id,))
    auction = sql2auction(cur.fetchall())
    cur.execute('SELECT u.username, b.date, b.price FROM bidding_history b, users u WHERE b.aid=(%s) ORDER BY b.date DESC;', (auction_id,))
    bids = map_history_dto(cur.fetchall())
    if auction.__len__() == 0:
        return render_template('404.html')
    return render_template('auction_details.html', auction=auction[0], bids=bids)


