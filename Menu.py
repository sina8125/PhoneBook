from textwrap import dedent

from rich.console import Console
from rich.table import Table, Column

from Contact import Contact
from ContactDataBase import ContactDataBase


class Menu:
    def __init__(self, database: ContactDataBase):
        self.database = database
        self.main_menu()

    def main_menu(self):
        while True:
            command = int(input(dedent('''
            What do you want to do with you contacts?
            1- Add a new one
            2- See all of them
            3- Search in all of them
            4- Delete
            5- Edit
            6- Exit
            ''')))
            match command:
                case 1:
                    self.insert_contact_menu()
                case 2:
                    self.get_all_contacts()
                case 3:
                    self.search()
                case 4:
                    self.delete()
                case 5:
                    self.edit()
                case 6:
                    break
                case _:
                    print('Undefined command, try again!')

    def insert_contact_menu(self):
        while True:
            contact = Contact(-1, 'temp', '09123456789')
            while True:
                try:
                    contact.phone_number = input("Enter your contact's number : ")
                    break
                except ValueError as e:
                    print(str(e))
            while True:
                try:
                    contact.first_name = input("Enter your contact's firstname : ")
                    break
                except ValueError as e:
                    print(str(e))
            while True:
                try:
                    contact.last_name = input(
                        "Enter your contact's lastname (This is optional, if you don't want to add this field just press enter) : ")
                    break
                except ValueError as e:
                    print(str(e))
            try:
                self.database.insert_contact(contact)
                print('Successfully added!')
                break
            except ValueError as e:
                print(str(e))
                print('Try again!')

    def get_all_contacts(self):
        last_sort = [True, False, False, False]
        contacts = self.database.read_contacts()
        while True:
            table = Table()
            table.add_column(header='First Name', justify='center', style='green')
            table.add_column(header='Last Name', justify='center', style='green')
            table.add_column(header='Phone Number', justify='center', style='green')
            table.add_column(header='created time', justify='center', style='green')
            for i, contact in enumerate(contacts):
                table.add_row(contact.first_name,
                              contact.last_name or '',
                              contact.phone_number,
                              contact.created_time.strftime('%Y-%m-%d %H:%M:%S'))
                if contacts[i - 1].first_name[0] != contact.first_name[0]:
                    table.add_section()
            console = Console()
            console.print(table)
            sort = int(input(dedent('''
            sort by:
            1- first name
            2- last name
            3- phone number
            4- created time
            5- exit
            ''')))
            match sort:
                case 1:
                    contacts.sort(key=lambda x: x.first_name, reverse=last_sort[sort - 1])
                case 2:
                    contacts.sort(key=lambda x: x.last_name or '', reverse=last_sort[sort - 1])
                case 3:
                    contacts.sort(key=lambda x: x.phone_number, reverse=last_sort[sort - 1])
                case 4:
                    contacts.sort(key=lambda x: x.created_time, reverse=last_sort[sort - 1])
                case 5:
                    return
                case _:
                    print('Undefined command, try again!')

            last_sort[sort - 1] = not last_sort[sort - 1]

    def search(self):
        pass

    def delete(self):
        pass

    def edit(self):
        pass
