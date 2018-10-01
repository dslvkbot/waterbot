class Order:
    def __init__(self, room=None, time=None, count=None, type_of_payment=None):
        self.room = room
        self.time = time
        self.count = count
        self.type_of_payment = type_of_payment

    def change_room(self, room):
        self.room = room

    def change_time(self, time):
        self.time = time

    def change_count(self, count):
        self.count = count

    def change_type(self, type_of_payment):
        self.type_of_payment = type_of_payment
