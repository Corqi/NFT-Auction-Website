from app.app import db, cur


def init_db():
	# table users
	cur.execute('DROP TABLE IF EXISTS users;')
	cur.execute('create table users ('
				'uid SERIAL PRIMARY KEY,'
				'username VARCHAR(32) UNIQUE not NULL,'
				'"password" VARCHAR(256) NOT NULL,'
				'email VARCHAR(32) UNIQUE NOT NULL,'
				'"name" VARCHAR(32),'
				'surname VARCHAR(32));')

	# table auction_items
	cur.execute('DROP TABLE IF EXISTS auction_items;')
	cur.execute('create table auction_items ('
				'aid SERIAL PRIMARY KEY,'
				'uid INTEGER NOT NULL,'
				'bid INTEGER not NULL,'
				'auction_start TIMESTAMP DEFAULT now() not NULL,'
				'auction_end TIMESTAMP not NULL,'
				'price FLOAT not NULL,'
				'"name" VARCHAR(256) not NULL,'
				'"desc" VARCHAR(1024),'
				'"link" VARCHAR(2048) not NULL,'
				'FOREIGN KEY(uid) REFERENCES users(uid),'
				'FOREIGN KEY(bid) REFERENCES users(uid),'
				'CHECK(auction_end > auction_start),'
				'CHECK(auction_start >= now()),'
				'CHECK(price >= 0))')

	# table bidding_history
	cur.execute('DROP TABLE IF EXISTS bidding_history;')
	cur.execute('create table bidding_history ('
				'bhid SERIAL PRIMARY KEY,'
				'aid INTEGER not NULL,'
				'bid INTEGER NOT NULL,'
				'date TIMESTAMP not NULL,'
				'price FLOAT not NULL,'
				'FOREIGN KEY(aid) REFERENCES auction_items(aid),'
				'FOREIGN KEY(bid) REFERENCES users(uid),'
				'CHECK(price >= 0));')
	db.commit()
