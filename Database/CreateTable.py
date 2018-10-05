from sqlite3 import OperationalError

import Database.Table as Table


def create():
    orders = Table.Table('orders')
    clients = Table.Table('clients')
    archive = Table.Table('archive')
    try:
        archive.create_table({
            'user_id': 'text',
            'count': 'text',
            'date': 'text',
        })
    except OperationalError:
        print('WARNING: Operational error while creating ArchiveTable')
    try:
        orders.create_table({
            'user_id': 'text',
            'count': 'text',
            'room': 'text',
            'time': 'text',
            'type': 'text',
            'date': 'text',
        })
    except OperationalError:
        print('WARNING: Operational error while creating OrderTable')
    try:
        clients.create_table({
            'user_id': 'text',
            'room': 'text',
        })
    except OperationalError:
        print('WARNING: Operational error while creating ClientsTable')
