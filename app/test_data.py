import datetime

from werkzeug.security import generate_password_hash
from app.database import db
from app.models import User, Auction

users = ['admintest1', 'admintest2', 'admintest3', 'admintest4', 'admintest5']


def insert_test_data():
    for user in users:
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM users WHERE username=(%s);', (user,))
        if cur.fetchone()[0] == 0:
            userdb = User(
                username=user,
                password=generate_password_hash(user, method='sha256', salt_length=8),
                email=user,
                name=user,
                surname=user
            )
            userdb.add()

    cur = db.cursor()
    cur.execute('SELECT count(*) FROM auction_items WHERE name=(%s);', ("space monke",))
    if cur.fetchone()[0] == 0:
        cur.execute('SELECT uid FROM users WHERE username=(%s);', ("admintest5",))
        user_id = cur.fetchone()[0]
        auction = Auction(
            uid=user_id,
            bid=user_id,
            auction_start=datetime.datetime.now(),
            auction_end=datetime.datetime.now() + datetime.timedelta(days=1000),
            price=100,
            name="space monke",
            desc="monke from space",
            link="https://i1.sndcdn.com/artworks-A4J7FVMfa1D0yI7i-hxGIUg-t500x500.jpg",
            owner_username="admintest5",
            highest_bid=0
        )
        auction.add()
