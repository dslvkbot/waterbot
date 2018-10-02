import Database.Table as Table
import datetime


def current_time():
    date = datetime.datetime.now()
    return [int(date.hour), int(date.minute), int(date.second)]


def time_in_seconds(timer):
    assert len(timer) >= 3, "Unright format time " + str(timer)
    return int(timer[0]) * 3600 + int(timer[1]) * 60 + int(timer[2])


class ReseteDatabase:

    def __init__(self, reset_time, radius=None):
        self.reset_time = time_in_seconds(reset_time)
        if radius is None:
            radius = 0
        self.radius = max(radius, 20)
        self.need_reset = True

    def reset(self):
        if self.need_reset is False:
            pass
        current_seconds = time_in_seconds(current_time())
        if abs(current_seconds - self.reset_time) < self.radius:
            orders = Table.Table('orders')
            clients = Table.Table('clients')
            orders.clear_table()
            try:
                orders.create_table({
                    'user_id': 'text',
                    'count': 'text',
                    'room': 'text',
                    'time': 'text',
                    'type': 'text',
                })
            except:
                pass
            try:
                clients.create_table({
                    'user_id': 'text',
                    'room': 'text',
                })
            except:
                pass
            self.need_reset = False
        else:
            self.need_reset = True
        if current_seconds > self.reset_time:
            self.need_reset = False
