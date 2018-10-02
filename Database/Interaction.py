import sqlite3 as sql

connect = sql.connect("database.sqlite")
cursor = connect.cursor()


def execute(query):
    cursor.execute(query)
    connect.commit()
    return cursor.fetchall()
