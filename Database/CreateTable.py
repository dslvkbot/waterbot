import Database.Table as Table

def create():
    orders = Table.Table('orders')
    clients = Table.Table('clients')
    archive = Table.Table('archive')
    try:
        archive.create_table({
            'used_id': 'text',
            'count': 'text',
            'date': 'text',
        })
    except:
        pass
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
