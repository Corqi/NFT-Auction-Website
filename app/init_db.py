from app.app import db


def init_db():
	cur = db.cursor()
	# table users
	cur.execute('DROP TABLE IF EXISTS users CASCADE;')
	cur.execute('''create table users (
				uid SERIAL PRIMARY KEY,
				username VARCHAR(32) UNIQUE not NULL,
				"password" VARCHAR(256) NOT NULL,
				email VARCHAR(32) UNIQUE NOT NULL,
				"name" VARCHAR(32),
				surname VARCHAR(32));''')

	# table auction_items
	cur.execute('DROP TABLE IF EXISTS auction_items CASCADE;')
	cur.execute('''create table auction_items (
				aid SERIAL PRIMARY KEY,
				uid INTEGER NOT NULL,
				bid INTEGER not NULL,
				auction_start TIMESTAMP DEFAULT now() not NULL,
				auction_end TIMESTAMP not NULL,
				price FLOAT not NULL,
				"name" VARCHAR(256) not NULL,
				"desc" VARCHAR(1024),
				"link" VARCHAR(2048) not NULL,
				FOREIGN KEY(uid) REFERENCES users(uid),
				FOREIGN KEY(bid) REFERENCES users(uid),
				CHECK(auction_end > auction_start),
				CHECK(price >= 0));''')

	# table bidding_history
	cur.execute('DROP TABLE IF EXISTS bidding_history CASCADE;')
	cur.execute('''create table bidding_history (
				bhid SERIAL PRIMARY KEY,
				aid INTEGER not NULL,
				bid INTEGER NOT NULL,
				date TIMESTAMP DEFAULT now() not NULL,
				price FLOAT not NULL,
				FOREIGN KEY(aid) REFERENCES auction_items(aid),
				FOREIGN KEY(bid) REFERENCES users(uid),
				CHECK(price >= 0)
				);''')

	# create function to check if bid is higher than others
	cur.execute('''CREATE OR REPLACE FUNCTION isHigher (FLOAT, INTEGER) RETURNS BOOL as '
					DECLARE 
						row bidding_history%rowtype;
					BEGIN
	    				FOR row in SELECT * FROM bidding_history WHERE aid=$2 LOOP
	    					if row.price >= $1 then
	    						return true;
	    				END if;
	    				END LOOP;
	    				return false;
	    			end;
	    			' language 'plpgsql';
		''')

	# alter bidding_history to use this above function as check
	cur.execute('''ALTER TABLE bidding_history
				ADD CONSTRAINT priceCheck
				CHECK (isHigher(price, aid) = false);''')
	db.commit()
