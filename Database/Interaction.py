import sqlite3 as sql

connect = sql.connect("database.sqlite")
cursor = connect.cursor()


def execute(query):
#    try:
    cursor.execute(query)
    connect.commit()
    return cursor.fetchall()
 #   except:
 #       print("Impossible make query {query}".format(query=query))
