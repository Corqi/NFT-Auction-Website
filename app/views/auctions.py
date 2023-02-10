import datetime

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from app.app import cur
from app.forms import BiddingForm
from app.models import Auction, History

bp = Blueprint('bp_auctions', __name__)


@bp.route('/auctions')
def user_auctions_get():
    cur.execute(
        'SELECT a.aid, a.uid, a.bid, a.auction_start, a.auction_end, a.price, a.name, a.desc, a.link, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items a '
        'JOIN users u ON u.uid = a.uid '
        'LEFT JOIN bidding_history b ON a.aid = b.aid '
        'WHERE a.uid = (%s)'
        'GROUP BY a.aid, u.username;', (str(current_user.get_id()))
    )
    auctions = []
    for auction in cur.fetchall():
        auctions.append(Auction(*auction))
    return render_template('gallery.html', auctions=auctions, user=current_user)


@bp.route('/auction/<int:auction_id>', methods=['POST', 'GET'])
def auction_details(auction_id):
    form = BiddingForm()
    if form.validate_on_submit():
        cur.execute('SELECT price FROM auction_items WHERE aid=(%s);', (auction_id,))
        starting_price = cur.fetchall()[0][0]
        price = form.price.data
        cur.execute('SELECT MAX(b.price) FROM bidding_history b WHERE b.aid=(%s);', (auction_id,))
        current_price = cur.fetchall()

        if current_price[0][0] is None and starting_price < price:
            new_bid = History(aid=auction_id, bid=current_user.uid, price=price)
            new_bid.add()
        elif current_price[0][0] is None and starting_price >= price:
            flash('eee co tak mało?')
        else:
            if current_price[0][0] < price:
                new_bid = History(aid=auction_id, bid=current_user.uid, price=price)
                new_bid.add()
            else:
                flash('eee co tak mało?')
        return redirect(url_for('bp_auctions.auction_details', auction_id=auction_id))

    cur.execute(
        'SELECT a.aid, a.uid, a.bid, a.auction_start, a.auction_end, a.price, a.name, a.desc, a.link, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items a '
        'JOIN users u ON u.uid = a.uid '
        'LEFT JOIN bidding_history b ON a.aid = b.aid '
        'WHERE a.aid=(%s) '
        'GROUP BY a.aid, u.username;', (auction_id,)
    )

    auction = Auction(*cur.fetchone())

    cur.execute('SELECT b.bhid, b.aid, b.bid, b.date, b.price, u.username '
                'FROM bidding_history b, users u '
                'WHERE b.aid=(%s) AND b.bid=u.uid '
                'ORDER BY b.date DESC;', (auction_id,))

    bids = []
    for bid in cur.fetchall():
        bids.append(History(*bid))

    # TODO do not display the form if the user is the owner of the auction
    return render_template('auction_details.html', auction=auction, bids=bids, form=form, user=current_user,
                           is_expired=auction.auction_end < datetime.datetime.now())
