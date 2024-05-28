# Consultants are employees of the Unique Meal who are in direct contact with the members. 
# They process the requests of the members. Hence, they need to be able to manage the member’s information and data. 
# For this purpose, when a new client requests for membership, a consultant needs to register the client's information in the system. 
# So, the minimum required functions of a consultant in the system are summarized as below:

# FUNCTIONS TO DO:

import uuid
from classes.menu import Menu
from db.db_connection import ConnectToDB

class Consultant:
    def __init__(self, username, level):
        self.username = username
        self.level = level
        self.menu_options = ["Update password", "Add member", "Update member", "Search member"]
        self.menu_functions = [self.update_password, self.add_member, self.update_member, self.search_member]
        self.menu = Menu(
            options=self.menu_options,
            functions=self.menu_functions
        )

    # ● To update their own password
    def update_password(self):
        print("Updating password...")

    # ● To add a new member to the system
    def add_member(self):
        print("Enter the info of the new Member:")
        id = uuid.uuid4()
        name = input("Name: ")
        password = input("Password: ")
        level = 0
        gender = input("Gender: ")
        weight = input("Weight: ")
        email = input("Email: ")

        # TODO: Mobile Phone (+31-6-DDDDDDDD) – only DDDDDDDD to be entered by the user.
        mobile = input("Mobile: ")

        # wat is het nut van eerst dit maken en daarna in de execute te zetten als het ook direct kan??
        Member = {"id": id, "name": name, "password": password, "level": level, "gender": gender, "weight": weight, "email": email, "mobile": mobile}

        print("Now adding Member...")

        # TODO: also ask and add address
        c = ConnectToDB()
        c.execute("INSERT INTO users (id, name, password, level, gender, weight, email, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(Member['id']), Member['name'], Member['password'], Member['level'], Member['gender'], Member['weight'], Member['email'], Member['mobile']))
        c.commit()
        c.close()

        print("Adding Member successful!")
        input("Press Enter to Continue")

    # ● To modify or update the information of a member in the system
    def update_member(self):
        print("Updating member info...")

    # ● To search and retrieve the information of a member (check note 2 below).
    def search_member(self):
        print("Searching member...")

    def display_menu(self):
        self.menu.display()
        self.menu.execute_choice()