import logging
from flask_login import UserMixin
from app.app import db, cur


class User(UserMixin):
    def __init__(self, uid=None, username=None, password=None, email=None, name=None, surname=None):
        self.uid = uid
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname

    def get_id(self):
        """ For login manager"""
        return str(self.uid)

    # update user in db
    def update(self):
        # check if user exists
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.uid,))
        if len(cur.fetchall()) == 0:
            logging.error('User not found!')
            return
        # check for not nullable variables
        if self.username is None or self.password is None or self.password is None:
            logging.error('Not nullable variables found!')
            return

        # update db
        cur.execute('''UPDATE users SET username=(%s), password=(%s), email=(%s), name=(%s), surname=(%s)
                    WHERE uid=(%s);''',
                    (self.username, self.password, self.email, self.name, self.surname, self.uid))
        db.commit()
        return

    # add user to db
    def add(self):
        # check if username already exists
        cur.execute('SELECT * FROM users WHERE username=(%s);', (self.username,))
        if len(cur.fetchall()) != 0:
            logging.error('Username already taken!')
            return
        # check if email already exists
        cur.execute('SELECT * FROM users WHERE email=(%s);', (self.email,))
        if len(cur.fetchall()) != 0:
            logging.error('Email already taken!')
            return
        # check for not nullable variables
        if self.username is None or self.password is None or self.password is None:
            logging.error('Not nullable variables found!')
            return

        # add to db
        cur.execute('''INSERT INTO users (username, password, email, name, surname) VALUES (%s, %s, %s, %s, %s);''',
                    (self.username, self.password, self.email, self.name, self.surname))
        db.commit()
        return


class Auction:
    def __init__(self, aid=None, uid=None, bid=None, auction_start=None, auction_end=None, price=None, name=None,
                 desc=None, link=None, owner_username=None, highest_bid=None):
        self.aid = aid
        self.uid = uid
        self.bid = bid
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.price = price
        self.name = name
        self.desc = desc
        self.link = link

        self.owner_username = owner_username
        self.highest_bid = highest_bid

    # update auction in db
    def update(self):
        # check if auction exists
        cur.execute('SELECT * FROM auction_items WHERE aid=(%s);', (self.aid,))
        if len(cur.fetchall()) == 0:
            logging.error('Auction not found!')
            return
        # check if seller and bidder exists
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.uid,))
        if len(cur.fetchall()) == 0:
            logging.error('Seller not found!')
            return
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.bid,))
        if len(cur.fetchall()) == 0:
            logging.error('Bidder not found!')
            return
        # check for not nullable variables
        if self.auction_start is None or self.auction_end is None or self.price is None or self.name is None \
                or self.link is None:
            logging.error('Not nullable variables found!')
            return
        # check if price >= 0
        if self.price < 0:
            logging.error('Price must be a positive number!')
            return
        # check if auction_end > auction_start
        if self.auction_end < self.auction_start:
            logging.error('Auction_end must be later than Auction_start!')
            return

        # update db
        cur.execute('''UPDATE auction_items SET bid=(%s), auction_start=(%s), auction_end=(%s), price=(%s), name=(%s), 
                    "desc"=(%s), link=(%s)
                    WHERE aid=(%s);''',
                    (self.bid, self.auction_start, self.auction_end, self.price, self.name, self.desc, self.link,
                     self.aid))
        db.commit()
        return

    # add auction to db
    def add(self):
        cur.execute('BEGIN TRANSACTION;')
        # check if seller and bidder exists
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.uid,))
        if len(cur.fetchall()) == 0:
            logging.error('Seller not found!')
            return
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.bid,))
        if len(cur.fetchall()) == 0:
            logging.error('Bidder not found!')
            return
        # check for not nullable variables
        if self.auction_start is None or self.auction_end is None or self.price is None or self.name is None \
                or self.link is None:
            logging.error('Not nullable variables found!')
            return
        # check if price >= 0
        if self.price < 0:
            logging.error('Price must be a positive number!')
            return
        # check if auction_end > auction_start
        if self.auction_end < self.auction_start:
            logging.error('Auction_end must be later than Auction_start!')
            return

        # add to db
        cur.execute('''INSERT INTO auction_items (uid, bid, auction_start, auction_end, price, name, "desc", link) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''',
                    (self.uid, self.bid, self.auction_start, self.auction_end, self.price, self.name, self.desc,
                     self.link))
        db.commit()
        return


class History:
    def __init__(self, bhid=None, aid=None, bid=None, date=None, price=None, bidder_username=None, auction_name=None):
        self.bhid = bhid
        self.aid = aid
        self.bid = bid
        self.date = date
        self.price = price

        self.bidder_username = bidder_username
        self.auction_name = auction_name

    # update history in db
    def update(self):
        # check if history exists
        cur.execute('SELECT * FROM bidding_history WHERE bhid=(%s);', (self.bhid,))
        if len(cur.fetchall()) == 0:
            logging.error('History not found!')
            return
        # check if auction and bidder exists
        cur.execute('SELECT * FROM auction_items WHERE aid=(%s);', (self.aid,))
        if len(cur.fetchall()) == 0:
            logging.error('Auction not found!')
            return
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.bid,))
        if len(cur.fetchall()) == 0:
            logging.error('Bidder not found!')
            return
        # check for not nullable variables
        if self.date is None or self.price is None:
            logging.error('Not nullable variables found!')
            return
        # check if price >= 0
        if self.price < 0:
            logging.error('Price must be a positive number!')
            return

        # update db
        cur.execute('''UPDATE bidding_history SET aid=(%s), bid=(%s), date=(%s), price=(%s)
                    WHERE bhid=(%s);''',
                    (self.aid, self.bid, self.date, self.price))
        db.commit()
        return

    # add user to db
    def add(self):
        # check if history exists
        cur = db.cursor()
        cur.execute('SELECT * FROM bidding_history WHERE bhid=(%s);', (self.bhid,))
        if len(cur.fetchall()) != 0:
            logging.error('History not found!')
            return
        # check if auction and bidder exists
        cur.execute('SELECT * FROM auction_items WHERE aid=(%s);', (self.aid,))
        if len(cur.fetchall()) == 0:
            logging.error('Auction not found!')
            return
        cur.execute('SELECT * FROM users WHERE uid=(%s);', (self.bid,))
        if len(cur.fetchall()) == 0:
            logging.error('Bidder not found!')
            return
        # check if price >= 0
        if self.price < 0:
            logging.error('Price must be a positive number!')
            return

        # add to db
        cur.execute('''INSERT INTO bidding_history (aid, bid, price) VALUES (%s, %s, %s);''',
                    (self.aid, self.bid, self.price))
        db.commit()
        return
