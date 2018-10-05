from sqlite3 import OperationalError

import Database.Table as Table
import datetime


def parse_date(string):
    fields = string.split('.')
    assert len(fields) == 3, "Unright format date, need: dd.mm.yy"
    return datetime.datetime(int(fields[2]), int(fields[1]), int(fields[0]))


def current_date():
    now = datetime.datetime.today()
    return datetime.datetime(now.year, now.month, now.day)


def current_time():
    date = datetime.datetime.now()
    return [int(date.hour), int(date.minute), int(date.second)]


def time_in_seconds(timer):
    assert len(timer) >= 3, "Wrong format time " + str(timer)
    return int(timer[0]) * 3600 + int(timer[1]) * 60 + int(timer[2])


def need_delete_order(date):
    date_order = parse_date(date)
    if (current_date() - date_order).days > 3:
        return True
    return False


def reset():
    table_orders = Table.Table('orders')
    records = table_orders.select(['user_id', 'date'])
    for record in records:
        if need_delete_order(record[1]):
            table_orders.delete_info_by_user_id(record[0])


class ReseterClass:

    def __init__(self, radius=30):
        if radius < 30:
            radius = 30
        self.radius = radius
        self.need_reset = True

    def reset(self):
        if not self.need_reset:
            pass
        current_seconds = time_in_seconds(current_time())
        if abs(current_seconds - time_in_seconds([1, 0, 0])) < self.radius:
            self.need_reset = False
            reset()
