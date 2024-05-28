# Consultants are employees of the Unique Meal who are in direct contact with the members. 
# They process the requests of the members. Hence, they need to be able to manage the member’s information and data. 
# For this purpose, when a new client requests for membership, a consultant needs to register the client's information in the system. 
# So, the minimum required functions of a consultant in the system are summarized as below:

# FUNCTIONS TO DO:

# ● To update their own password

# ● To add a new member to the system

# ● To modify or update the information of a member in the system

# ● To search and retrieve the information of a member (check note 2 below).


from classes.menu import Menu

class Consultant:
    def __init__(self, username, level):
        self.username = username
        self.level = level
        self.menu = Menu(
            options=["Update password", "Add member", "Update member info", "Search member"],
            functions=[self.update_password, self.add_member, self.update_member_info, self.search_member]
        )

    def update_password(self):
        print("Updating password...")

    def add_member(self):
        print("Adding member...")

    def update_member_info(self):
        print("Updating member info...")

    def search_member(self):
        print("Searching member...")

    def display_menu(self):
        self.menu.display()
        self.menu.execute_choice()