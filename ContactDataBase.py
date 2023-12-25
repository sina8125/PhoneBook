import datetime
import sqlite3


class ContactDataBase:
    def __init__(self):
        with sqlite3.connect('contacts.db') as connection:
            create_table_query = '''CREATE TABLE IF NOT EXISTS CONTACTDATA (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NULL,
            phone_number CHARACTER(11) NOT NULL,
            created_time DATETIME NOT NULL);'''
            cursor = connection.cursor()
            cursor.execute(create_table_query)
