import datetime
import sqlite3

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
        if not self.check_repeated_number(contact.phone_number):
            raise ValueError("Phone number already exists")
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            if contact.first_name:
                contact.first_name = contact.first_name.replace("'", "\'")
            if contact.last_name:
                contact.last_name = contact.last_name.replace("'", "\'")

            insert_query = f'''INSERT INTO CONTACTDATA (first_name, last_name, phone_number)
                         VALUES (?,?,?)'''
            cursor.execute(insert_query, (contact.first_name, contact.last_name, contact.phone_number))
            connection.commit()
            cursor.close()

    def read_contacts(self) -> list[Contact] or None:
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            select_query = f'''SELECT * FROM CONTACTDATA ORDER BY first_name ASC, last_name ASC;'''
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
        return contact_list

    def check_repeated_number(self, phone_number: str) -> bool:
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            select_query = f'''select count(*) from CONTACTDATA where phone_number = '{phone_number}';'''
            result = cursor.execute(select_query).fetchall()
            connection.commit()
            cursor.close()
        if result[0][0] == 0:
            return True
        return False

    def search(self, search_input: str) -> list[Contact] or None:
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            if search_input.isnumeric():
                select_query = f'''SELECT * FROM CONTACTDATA WHERE phone_number like '%{search_input}%';'''
                result = cursor.execute(select_query).fetchall()
            else:
                select_query = f'''SELECT * FROM CONTACTDATA WHERE (first_name || COALESCE((' ' || last_name),'')) like '%{search_input.lower()}%';'''
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
        return contact_list

    def edit(self, contact: Contact):
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            try:
                cursor = connection.cursor()
                query = f'''UPDATE CONTACTDATA
                                   SET first_name = ?, last_name = ?,
                                    phone_number = ? 
                                    WHERE id = ? ;'''
                cursor.execute(query, (contact.first_name, contact.last_name, contact.phone_number, contact.database_id))
                connection.commit()
                cursor.close()
            except sqlite3.IntegrityError as e:
                if any('UNIQUE constraint failed' in arg for arg in e.args):
                    raise ValueError("Phone number already exists")

    def delete_contacts(self, contacts: list[Contact]) -> None:
        with sqlite3.connect(database_file,
                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as connection:
            cursor = connection.cursor()
            contacts_id = str([contact.database_id for contact in contacts])[1:-1]
            delete_query = f'''DELETE FROM CONTACTDATA WHERE id IN ({contacts_id});'''
            cursor.execute(delete_query)
            connection.commit()
            cursor.close()
