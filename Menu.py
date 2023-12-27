from textwrap import dedent
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
                    contact.last_name = input("Enter your contact's lastname (This is optional, if you don't want to add this field just press enter) : ")
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
        pass

    def delete(self):
        pass

    def edit(self):
        pass

