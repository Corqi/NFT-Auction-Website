class HistoryDto:
    def __init__(self, username, date, price):
        self.username = username
        self.date = date
        self.price = price


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
