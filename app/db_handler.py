from app.models import User, Auction, History


# these functions translate sql select into list of objects
# IMPORTANT use only when selecting ALL columns

def sql2user(rows) -> list[User]:
    result = []

    for row in rows:
        user = User(
            uid=row[0],
            username=row[1],
            password=row[2],
            email=row[3],
            name=row[4],
            surname=row[5]
        )

        result.append(user)

    return result


def sql2auction(rows) -> list[Auction]:
    result = []

    for row in rows:
        auction = Auction(
            aid=row[0],
            uid=row[1],
            bid=row[2],
            auction_start=row[3],
            auction_end=row[4],
            price=row[5],
            name=row[6],
            desc=row[7],
            link=row[8]
        )
        result.append(auction)

    return result


def sql2history(rows) -> list[History]:
    result = []

    for row in rows:
        history = History(
            bhid=row[0],
            aid=row[1],
            bid=row[2],
            date=row[3],
            price=row[4]
        )
        result.append(history)

    return result
