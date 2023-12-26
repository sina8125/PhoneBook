import datetime
import sqlite3

import pytz

from Contact import Contact

database_file = "contacts.db"


class ContactDataBase:
    def __init__(self):
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            create_table_query = '''CREATE TABLE IF NOT EXISTS CONTACTDATA (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NULL,
            phone_number CHARACTER(11) NOT NULL UNIQUE,
            created_time TIMESTAMP NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime'))
            );'''
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
            cursor.close()

    def insert_contact(self, contact: Contact):
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            if contact.first_name:
                contact.first_name = contact.first_name.replace("'", "\'")
            if contact.last_name:
                contact.last_name = contact.last_name.replace("'", "\'")

            insert_query = f'''INSERT INTO CONTACTDATA (first_name, last_name, phone_number)
             VALUES ('{contact.first_name}','{contact.last_name}', '{contact.phone_number}')'''
            cursor.execute(insert_query)
            connection.commit()
            cursor.close()

    def read_contacts(self) -> list[Contact] or None:
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            select_query = f'''SELECT * FROM CONTACTDATA;'''
            result = cursor.execute(select_query).fetchall()
            connection.commit()
            cursor.close()
        contact_list = []
        for row in result:
            contact_list.append(Contact(database_id=row[0],
                                        first_name=row[1],
                                        last_name=row[2],
                                        phone_number=row[3],
                                        created_time=row[4]))
        return contact_list if len(contact_list) > 0 else None
