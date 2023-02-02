# these functions translate sql select into dictionary
# IMPORTANT use only when selecting ALL columns

def sql2user(rows) -> list[dict]:
    result = []

    for row in rows:
        dictionary = {
            'uid': row[0],
            'username': row[1],
            'password': row[2],
            'email': row[3],
            'name': row[4],
            'surname': row[5]
        }
        result.append(dictionary)

    return result


def sql2auction(rows) -> list[dict]:
    result = []

    for row in rows:
        dictionary = {
            'aid': row[0],
            'uid': row[1],
            'bid': row[2],
            'auction_start': row[3],
            'auction_end': row[4],
            'price': row[5],
            'name': row[3],
            'desc': row[4],
            'link': row[5]
        }
        result.append(dictionary)

    return result


def sql2history(rows) -> list[dict]:
    result = []

    for row in rows:
        dictionary = {
            'bhid': row[0],
            'aid': row[1],
            'bid': row[2],
            'date': row[3],
            'price': row[4]
        }
        result.append(dictionary)

    return result
