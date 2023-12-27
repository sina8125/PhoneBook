import re
from textwrap import dedent
from Contact import Contact
from ContactDataBase import ContactDataBase
from rich.console import Console
from rich.table import Table


class Menu:
    def __init__(self, database: ContactDataBase):
        self.database = database
        self.console = Console()
        self.main_menu()

    def main_menu(self):
        while True:
            command = input(dedent('''
            What do you want to do with you contacts?
            1- Add a new one
            2- See all of them
            3- Find, edit or delete
            4- Exit
            '''))
            match command:
                case '1':
                    self.insert_contact_menu()
                case '2':
                    self.get_all_contacts()
                case '3':
                    self.search()
                case '4':
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
            sort = input(dedent('''
            sort by:
            1- first name
            2- last name
            3- phone number
            4- created time
            5- exit
            '''))
            match sort:
                case '1':
                    contacts.sort(key=lambda x: x.first_name, reverse=last_sort[sort - 1])
                case '2':
                    contacts.sort(key=lambda x: x.last_name or '', reverse=last_sort[sort - 1])
                case '3':
                    contacts.sort(key=lambda x: x.phone_number, reverse=last_sort[sort - 1])
                case '4':
                    contacts.sort(key=lambda x: x.created_time, reverse=last_sort[sort - 1])
                case '5':
                    return
                case _:
                    print('Undefined command, try again!')

            last_sort[sort - 1] = not last_sort[sort - 1]

    def search(self):
        while True:
            search_input = input(
                'Enter part of name or phone number of the contact you want to find (or type \"return\" to get back): ')
            if search_input == 'return':
                break
            res = self.database.search(search_input)
            table = Table("Number", "First name", 'Last name', "Phone Number", "Date Added", title="Found Contacts: ")
            if res is not None:
                res = list(enumerate(res, start=1))
                for contact in res:
                    table.add_row(str(contact[0]),
                                  contact[1].first_name,
                                  contact[1].last_name if contact[1].last_name != 'None' else '',
                                  contact[1].phone_number,
                                  str(contact[1].created_time))
                self.console.print(table)
                break_outer_loop = False
                while True:
                    after_search_command = input(dedent('''
                            What do you want to do with these found contacts?
                            1- Edit one of them
                            2- Delete
                            3- Search again
                            4- Do nothing and return
                            '''))
                    match after_search_command:
                        case '1':
                            while True:
                                selected_contact_number = int(input('Enter number of the contact you want to edit: '))
                                if 1 <= selected_contact_number <= len(res):
                                    break
                                else:
                                    print('Enter a number that exists on the result table!')
                            self.edit(res[selected_contact_number - 1][1])
                        case '2':
                            while True:
                                delete_command = input(dedent('''
                                                    Enter number of each contact you wish to delete:
                                                    (if you want to delete all found contacts type and enter "*")
                                                    (if you intend to delete multiple contacts, separate the numbers with space)
                                                    '''))
                                selected_contacts = []
                                if re.match(r'^\d+( \d+)*$', delete_command):
                                    selected_contacts_number = list(int(i) for i in delete_command.split())
                                    for enumeratedRow in res:
                                        if enumeratedRow[0] in selected_contacts_number:
                                            selected_contacts.append(enumeratedRow[1])
                                    self.delete(selected_contacts)
                                    break_outer_loop = True
                                    break
                                elif delete_command == '*':
                                    for enumeratedRow in res:
                                        selected_contacts.append(enumeratedRow[1])
                                    self.delete(selected_contacts)
                                    break_outer_loop = True
                                    break
                                else:
                                    print('Undefined command, try again!')
                            if break_outer_loop:
                                break
                        case '3':
                            break
                        case '4':
                            break_outer_loop = True
                            break
                        case _:
                            print('Undefined command, try again!')
                if break_outer_loop:
                    break
            else:
                print("Nothing found!")
                continue

    def delete(self, contacts: list[Contact]):
        self.database.delete_contacts(contacts)
        print('Successfully deleted!')

    def edit(self, contact: Contact):
        while True:
            edit_command = input(dedent('''
                Which one of the fields do you wish to edit?:
                1- First Name
                2- Last Name
                3- Phone Number
                4- Save and get back
                5- Discard the changes and get back
                '''))
            match edit_command:
                case '1':
                    while True:
                        try:
                            contact.first_name = input("Enter your contact's new first name : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case '2':
                    while True:
                        try:
                            contact.last_name = input("Enter your contact's new last name : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case '3':
                    while True:
                        try:
                            contact.phone_number = input("Enter your contact's new phone number : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case '4':
                    self.database.edit(contact)
                    break
                case '5':
                    break
                case _:
                    print('Undefined command, try again!')
