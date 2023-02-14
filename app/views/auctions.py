from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.app import cur
from app.forms import BiddingForm, NewAuctionForm
from app.models import Auction, History

import datetime

bp = Blueprint('bp_auctions', __name__)


@bp.route('/auctions')
@login_required
def user_auctions_get():
    cur.execute(
        'SELECT ai.*, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items ai '
        'JOIN users u ON u.uid = ai.uid '
        'LEFT JOIN bidding_history b ON ai.aid = b.aid '
        'WHERE ai.uid = (%s)'
        'GROUP BY ai.aid, u.username;', (str(current_user.get_id()),)
    )
    auctions = []
    for auction in cur.fetchall():
        auctions.append(Auction(*auction))
    return render_template('gallery.html', auctions=auctions, user=current_user)


@bp.route('/bids')
@login_required
def user_bids_get():
    cur.execute(
        'SELECT bi.*, NULL, ai.name '
        'FROM bidding_history bi '
        'LEFT JOIN (SELECT aid, name FROM auction_items) ai on ai.aid = bi.aid '
        'WHERE bi.bid = (%s);', (str(current_user.get_id()),)
    )
    bids = []
    for bid in cur.fetchall():
        bids.append(History(*bid))

    return render_template('bids.html', user=current_user, bids=bids)


@bp.route('/auction/<int:auction_id>', methods=['POST', 'GET'])
def auction_details(auction_id):
    cur.execute('SELECT * FROM auction_items WHERE aid=(%s);', (auction_id,))
    if not cur.fetchall():
        return render_template('404.html'), 404
    form = BiddingForm()
    if form.validate_on_submit():
        cur.execute('SELECT price FROM auction_items WHERE aid=(%s);', (auction_id,))
        starting_price = cur.fetchone()[0]

        cur.execute('SELECT MAX(b.price) FROM bidding_history b WHERE b.aid=(%s);', (auction_id,))
        current_price = cur.fetchone()[0]

        proposed_bid = form.price.data

        if current_price is None:
            if starting_price < proposed_bid:
                new_bid = History(aid=auction_id, bid=current_user.uid, price=proposed_bid)
                new_bid.add()
            else:
                flash('eee co tak mało?')
        else:
            if current_price < proposed_bid:
                new_bid = History(aid=auction_id, bid=current_user.uid, price=proposed_bid)
                new_bid.add()
            else:
                flash('eee co tak mało?')

        return redirect(url_for('bp_auctions.auction_details', auction_id=auction_id))

    cur.execute(
        'SELECT ai.*, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items ai '
        'JOIN users u ON u.uid = ai.uid '
        'LEFT JOIN bidding_history b ON ai.aid = b.aid '
        'WHERE ai.aid=(%s) '
        'GROUP BY ai.aid, u.username;', (auction_id,)
    )
    auction = Auction(*cur.fetchone())

    cur.execute('SELECT b.*, u.username '
                'FROM bidding_history b, users u '
                'WHERE b.aid=(%s) AND b.bid=u.uid '
                'ORDER BY b.date DESC;', (auction_id,))
    bids = []
    for bid in cur.fetchall():
        bids.append(History(*bid))

    return render_template('auction_details.html', auction=auction, bids=bids, form=form, user=current_user,
                           is_expired=auction.auction_end < datetime.datetime.now())


@bp.route('/won')
@login_required
def won_auctions_get():
    cur.execute(
        'SELECT ai.*, u.username, bidding_history.price '
        'FROM bidding_history '
        'INNER JOIN auction_items ai on ai.aid = bidding_history.aid '
        'JOIN users u on u.uid = ai.uid '
        'WHERE bhid '
        'IN ('
        'SELECT max(bhid) '
        'FROM bidding_history bi '
        'GROUP BY aid'
        ') '
        'AND bidding_history.bid = (%s) '
        'AND ai.auction_end < now();', (current_user.get_id(),)
    )
    auctions = []
    for auction in cur.fetchall():
        auctions.append(Auction(*auction))
    return render_template('gallery.html', auctions=auctions, user=current_user)


@bp.route('/new', methods=['POST', 'GET'])
@login_required
def new_auction():
    form = NewAuctionForm()
    if form.validate_on_submit():
        auction_end = datetime.datetime.combine(form.auction_end.data, form.auction_end_time.data)
        auction = Auction(uid=current_user.get_id(),
                          bid=current_user.get_id(),
                          auction_start=datetime.datetime.now(),
                          auction_end=auction_end,
                          price=form.price.data,
                          name=form.name.data,
                          desc=form.description.data,
                          link=form.img_link.data
                          )
        auction.add()

        return redirect(url_for('bp_home.home_get'))

    return render_template('newAuction.html', form=form, user=current_user)
