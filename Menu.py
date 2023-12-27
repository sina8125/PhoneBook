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
            command = int(input(dedent('''
            What do you want to do with you contacts?
            1- Add a new one
            2- See all of them
            3- Find, edit or delete
            4- Exit
            ''')))
            match command:
                case 1:
                    self.insert_contact_menu()
                case 2:
                    self.get_all_contacts()
                case 3:
                    self.search()
                case 4:
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
        pass

    def search(self):
        while True:
            search_input = input(
                'Enter part of name or phone number of the contact you want to find (or type \"return\" to get back): ')
            if search_input == 'return':
                break
            res = self.database.search(search_input)
            table = Table("number", "Name", "Phone Number", "Date Added", title="Found Contacts: ")
            if res is not None:
                res = list(enumerate(res, start=1))
                for contact in res:
                    table.add_row(str(contact[0]),
                                  contact[1].first_name,
                                  contact[1].phone_number,
                                  str(contact[1].created_time))
                self.console.print(table)
                break_outer_loop = False
                while True:
                    after_search_command = int(input(dedent('''
                            What do you want to do with these found contacts?
                            1- Edit one of them
                            2- Delete some of them
                            3- Delete all of them
                            4- Search again
                            5- Do nothing and return
                            ''')))
                    match after_search_command:
                        case 1:
                            while True:
                                selected_contact_number = int(input('Enter number of the contact you want to edit: '))
                                if 1 <= selected_contact_number <= len(res):
                                    break
                                else:
                                    print('Enter a number that exists on the result table!')
                            self.edit(res[selected_contact_number - 1][1])
                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            break
                        case 5:
                            break_outer_loop = True
                            break
                        case _:
                            print('Undefined command, try again!')
                if break_outer_loop:
                    break
            else:
                print("Nothing found!")
                continue

    def delete(self):
        pass

    def edit(self, contact: Contact):
        while True:
            edit_command = int(input(dedent('''
                Which one of the fields do you wish to edit?:
                1- First Name
                2- Last Name
                3- Phone Number
                4- Save and get back
                5- Discard the changes and get back
                ''')))
            match edit_command:
                case 1:
                    while True:
                        try:
                            contact.first_name = input("Enter your contact's new first name : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case 2:
                    while True:
                        try:
                            contact.last_name = input("Enter your contact's new last name : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case 3:
                    while True:
                        try:
                            contact.phone_number = input("Enter your contact's new phone number : ")
                            break
                        except ValueError as e:
                            print(str(e))
                case 4:
                    self.database.edit(contact)
                    break
                case 5:
                    break
                case _:
                    print('Undefined command, try again!')
