import copy
import os
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
            0- Exit
            1- Add a new one
            2- See all of them
            3- Find, edit or delete
            --------------------------------------
            ''')).strip()
            match command:
                case '1':
                    if not self.insert_contact_menu():
                        os.system('cls' if os.name == 'nt' else 'clear')
                case '2':
                    self.get_all_contacts()
                    os.system('cls' if os.name == 'nt' else 'clear')
                case '3':
                    self.search()
                    os.system('cls' if os.name == 'nt' else 'clear')
                case '0':
                    break
                case _:
                    print('Undefined command, try again!')

    def insert_contact_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            contact = Contact(-1, 'temp', '09123456789')
            while True:
                try:
                    phone_number = input("Enter your contact's number (type # to back): ").strip()
                    if phone_number == '#':
                        return False
                    contact.phone_number = phone_number
                    break
                except ValueError as e:
                    print(str(e))
            while True:
                try:
                    first_name = input("Enter your contact's firstname (type # to back): ").strip()
                    if phone_number == '#':
                        return False
                    contact.first_name = first_name
                    break
                except ValueError as e:
                    print(str(e))
            while True:
                try:
                    contact.last_name = input(
                        "Enter your contact's lastname (This is optional, if you don't want to add this field just press enter) : ").strip()
                    break
                except ValueError as e:
                    print(str(e))
            try:
                self.database.insert_contact(contact)
                print('Successfully added!')
                return True
            except ValueError as e:
                print(str(e))
                print('Try again!')

    def get_all_contacts(self):
        last_sort = [True, False, False, False]
        contacts = self.database.read_contacts()
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            table = Table()
            table.add_column(header='First Name', justify='center')
            table.add_column(header='Last Name', justify='center')
            table.add_column(header='Phone Number', justify='center')
            table.add_column(header='created time', justify='center')
            for i, contact in enumerate(contacts):
                if i > 0 and contacts[i - 1].first_name[0] != contact.first_name[0]:
                    table.add_section()
                style = '#33ccff' if i % 3 == 0 else ('#00ff40' if i % 3 == 1 else '#fe3939')
                table.add_row(contact.first_name,
                              contact.last_name or '',
                              contact.phone_number,
                              contact.created_time.strftime('%Y-%m-%d %H:%M:%S'), style=style)

            console = Console()
            console.print(table)
            sort = input(dedent('''
            sort by:
            0 - Exit
            1- first name
            2- last name
            3- phone number
            4- created time
            --------------------------------------
            ''')).strip()
            match sort:
                case '1':
                    contacts.sort(key=lambda x: x.first_name, reverse=last_sort[int(sort) - 1])
                case '2':
                    contacts.sort(key=lambda x: x.last_name or '', reverse=last_sort[int(sort) - 1])
                case '3':
                    contacts.sort(key=lambda x: x.phone_number, reverse=last_sort[int(sort) - 1])
                case '4':
                    contacts.sort(key=lambda x: x.created_time, reverse=last_sort[int(sort) - 1])
                case '0':
                    return
                case _:
                    print('Undefined command, try again!')
                    continue

            last_sort[int(sort) - 1] = not last_sort[int(sort) - 1]

    def search(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            search_input = input(
                'Enter part of name or phone number of the contact you want to find (or type \"#\" to get back): ').strip()
            if search_input == '#':
                break
            res = self.database.search(search_input)
            if self.search_menu(res):
                return

    def search_menu(self, res: list[Contact]):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            if res:
                table = Table(title="Found Contacts: ", caption_justify='center', title_justify='center')
                table.add_column("Number", justify='center')
                table.add_column("First name", justify='center')
                table.add_column("Last name", justify='center')
                table.add_column("Phone Number", justify='center')
                table.add_column("Date Added", justify='center')
                for i, contact in enumerate(res, start=1):
                    style = '#33ccff' if (i - 1) % 3 == 0 else ('#00ff40' if (i - 1) % 3 == 1 else '#fe3939')
                    table.add_row(str(i),
                                  contact.first_name,
                                  contact.last_name or '',
                                  contact.phone_number,
                                  contact.created_time.strftime('%Y-%m-%d %H:%M:%S'), style=style)
                self.console.print(table)
            else:
                print('Nothing found!')
                return False
            after_search_command = input(dedent('''
                    What do you want to do with these found contacts?
                    0- Do nothing and return
                    1- Edit one of them
                    2- Delete
                    3- Search again
                    --------------------------------------
                    ''')).strip()
            match after_search_command:
                case '1':
                    while True:
                        if len(res) == 1:
                            selected_contact_number = '1'
                        else:
                            selected_contact_number = input(
                                'Enter number of the contact you want to edit: (type # to back)\n').strip()
                            if selected_contact_number == '#':
                                break
                        if selected_contact_number.isdecimal() and 1 <= int(selected_contact_number) <= len(res):
                            self.edit(res[int(selected_contact_number) - 1])
                            break
                        else:
                            print('Enter a number that exists on the result table!')
                    os.system('cls' if os.name == 'nt' else 'clear')
                case '2':
                    self.delete_menu(res)
                case '3':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return False
                case '0':
                    return True
                case _:
                    print('Undefined command, try again!')

    def delete_menu(self, res: list[Contact]):
        while True:
            delete_command = input(dedent('''
                                Enter number of each contact you wish to delete:
                                (if you want to delete all found contacts type and enter "*")
                                (if you intend to delete multiple contacts, separate the numbers with space)
                                (type 0 to get back)
                                --------------------------------------
                                ''')).strip()
            selected_contacts = []
            if delete_command == '0':
                return
            elif re.match(r'^\d+( \d+)*$', delete_command):
                selected_contacts_number = [int(i) for i in delete_command.split()]
                if any(not (1 <= i <= len(res)) for i in selected_contacts_number):
                    print('Enter a number that exists on the result table!')
                    continue
                for i, contact in enumerate(res, start=1):
                    if i in selected_contacts_number:
                        selected_contacts.append(contact)
                for contact in selected_contacts:
                    res.remove(contact)
                self.delete(selected_contacts)
                return
            elif delete_command == '*':
                self.delete(res)
                res.clear()
                return
            else:
                print('Undefined command, try again!')

    def delete(self, contacts: list[Contact]):
        self.database.delete_contacts(contacts)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Successfully deleted!')

    def edit(self, contact: Contact):
        temp_contact = copy.deepcopy(contact)
        while True:
            edit_command = input(dedent('''
                Which one of the fields do you wish to edit?:
                1- First Name
                2- Last Name
                3- Phone Number
                4- Save and get back
                5- Discard the changes and get back
                ----------------------------------------
                ''')).strip()
            match edit_command:
                case '1':
                    while True:
                        try:
                            first_name = input("Enter your contact's new first name (type # to back): ").strip()
                            if '#' not in first_name:
                                temp_contact.first_name = first_name
                            break
                        except ValueError as e:
                            print(str(e))
                case '2':
                    while True:
                        try:
                            last_name = input("Enter your contact's new last name (type # to back): ").strip()
                            if '#' not in last_name:
                                if not last_name:
                                    temp_contact.last_name = None
                                else:
                                    temp_contact.last_name = last_name
                            break
                        except ValueError as e:
                            print(str(e))
                case '3':
                    while True:
                        try:
                            phone_number = input("Enter your contact's new phone number (type # to back): ").strip()
                            if not self.database.check_repeated_number(phone_number):
                                print('Phone number already exists')
                                print('Try again!')
                                continue
                            if '#' not in phone_number:
                                temp_contact.phone_number = phone_number
                            break
                        except ValueError as e:
                            print(str(e))
                case '4':
                    self.database.edit(temp_contact)
                    contact.__dict__.update(temp_contact.__dict__)
                    break
                case '5':
                    break
                case _:
                    print('Undefined command, try again!')
