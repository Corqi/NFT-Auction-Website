from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.app import cur
from app.models import Auction

import datetime

bp = Blueprint('bp_home', __name__)


@bp.route('/')
def home_get():
    list_of_auctions = []
    cur.execute(
        'SELECT ai.*, u.username, COALESCE(MAX(b.price), 0) as max_price '
        'FROM auction_items ai '
        'JOIN users u ON u.uid = ai.uid '
        'LEFT JOIN bidding_history b ON ai.aid = b.aid '
        'WHERE auction_end > (%s)'
        'GROUP BY ai.aid, u.username;', (datetime.datetime.now(),)
    )
    for auction in cur.fetchall():
        list_of_auctions.append(Auction(*auction))

    return render_template('gallery.html', auctions=list_of_auctions, user=current_user)
