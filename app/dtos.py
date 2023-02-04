class HistoryDto:
    def __init__(self, username, date, price):
        self.username = username
        self.date = date
        self.price = price


class AuctionDto:
    def __init__(self, aid, auction_start, auction_end, price, name, desc, link, auctioneer, highest_bid):
        self.aid = aid
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.price = price
        self.name = name
        self.desc = desc
        self.link = link
        self.auctioneer = auctioneer
        self.highest_bid = highest_bid


def map_history_dto(rows) -> list[HistoryDto]:
    result = []
    for row in rows:
        history_dto = HistoryDto(
            username=row[0],
            date=row[1],
            price=row[2]
        )
        result.append(history_dto)

    return result


def map_auction_dto(rows) -> list[AuctionDto]:
    result = []
    for row in rows:
        auction_dto = AuctionDto(
            aid=row[0],
            auction_start=row[1],
            auction_end=row[2],
            price=row[3],
            name=row[4],
            desc=row[5],
            link=row[6],
            auctioneer=row[7],
            highest_bid=row[8]
        )
        result.append(auction_dto)

    return result
