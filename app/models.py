from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, uid, username, password, email, name, surname):
        self.uid = uid
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname


class Auction:
    def __init__(self, aid, uid, bid, auction_start, auction_end, price, name, desc, lin):
        self.aid = aid
        self.uid = uid
        self.bid = bid
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.price = price
        self.name = name
        self.desc = desc
        self.lin = lin