# Consultants are employees of the Unique Meal who are in direct contact with the members. 
# They process the requests of the members. Hence, they need to be able to manage the member’s information and data. 
# For this purpose, when a new client requests for membership, a consultant needs to register the client's information in the system. 
# So, the minimum required functions of a consultant in the system are summarized as below:

# FUNCTIONS TO DO:

import uuid
from classes.menu import Menu
from functions.input_checks import Checks
from functions.id_functions import IdFunc


from db.db_connection import ConnectToDB

class Consultant:
    def __init__(self, username, level):
        self.username = username
        self.level = level
        self.logged_in = True
        self.menu_options = ["Update password", "Add member", "Update member", "Search member"]
        self.menu_functions = [self.update_password, self.add_member, self.update_member, self.search_member]
        self.menu = Menu(
            options=self.menu_options + ["Logout"],
            functions=self.menu_functions + [self.logout]
        )

    # ● To update their own password
    def update_password(self):
        print("Updating password...")

    # ● To add a new member to the system
    def add_member(self):
        print("Enter the info of the new Member:")

        # TODO: checks for the string inputs? they cant inject, so is there reason to?

        member_id = IdFunc.generate_membership_id()
        first_name = input("First name: ")
        last_name = input("Last name: ")

        age = input("Age: ")
        if not Checks.number_check(age):
            print("not a number, try again.")
            return
        gender = input("Gender: ")
        weight = input("Weight: ")
        if not Checks.number_check(weight):
            print("not a number, try again.")
            return

        street = input("Street name: ")
        house_number = input("House number: ")
        if not Checks.number_check(house_number):
            print("not a number, try again.")
            return
        zip_code = input("Zip code: ")
        if not Checks.zip_code_check(zip_code):
            print("zip code in wrong format, try again.")
            return
        
        # TODO: can only choose between 10 predecided cities
        city = input("City: ")

        email = input("Email: ")
        if not Checks.email_check(email):
            print("email in wrong format, try again.")
            return
        phone_number = input("Phone number: ")
        if not Checks.phone_number_check(phone_number):
            print("phone number in wrong format, try again.")
            return

        print("Now adding Member...")

        c = ConnectToDB()
        c.execute("INSERT INTO members (id, first_name, last_name, age, gender, weight, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(member_id), first_name, last_name, age, gender, weight, email, phone_number))
        c.execute("INSERT INTO address (id, member_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), member_id, street, house_number, zip_code, city))
        c.commit()
        c.close()

        print("Adding Member successful!")
        input("Press Enter to Continue")

    # ● To modify or update the information of a member in the system
    def update_member(self):
        print("Updating member info...")

    # ● To search and retrieve the information of a member.
    def search_member(self):
        print("Searching member...")

    def display_menu(self):
        self.menu.display()
        self.menu.execute_choice()

    def logout(self):
        print("Logging out...")
        self.logged_in = False
