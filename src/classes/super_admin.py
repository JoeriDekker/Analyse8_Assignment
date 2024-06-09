# Super administrator is simply the owner or the manager of the association. 
# The manager needs a super admin password through which can define a system administrator. 
# Although the main function of the super admin is to define system admin(s), and leave the system to them; however, 
# they should be able to perform all possible functionalities of the lower-level users (i.e., system admin and consultant).

# In this assignment, to make it easier for your teacher to test and assess your work, 
# a super admin must be hard coded with username: super_admin, password: Admin_123?

# § Note that we know this is not a good development practice in terms of the quality and security of the system, 
# but this is only to enable your teacher to easily test your system using this predefined hardcoded username and password.

# The minimum required functions of a super administrator are listed below:

# FUNCTIONS TO DO:

# (inherited from consultant)

    # ● To add a new member to the system.

    # ● To modify or update the information of a member in the system.

    # ● To search and retrieve the information of a member.

# (inherited from admin)

    # ● To check the list of users and their roles.

    # ● To define and add a new consultant to the system.

    # ● To modify or update an existing consultant’s account and profile.

    # ● To delete an existing consultant account.

    # ● To reset an existing consultant password (a temporary password).

    # ● To make a backup of the system and restore a backup (members information and users’ data).

    # ● To see the logs file of the system.

    # ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).

from classes.menu import Menu
from classes.admin import Admin

from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.hash_functions import HashFunctions
from functions.login import get_masked_password 

from db.db_connection import ConnectToDB
import sqlite3

class SuperAdmin(Admin):
    def __init__(self, username, level):
        super().__init__(username, level)
        super_admin_options = [
            "Add admin", "Update admin", "Delete admin",
            "Reset admin password"
        ]
        super_admin_functions = [
            self.add_admin, self.update_admin, self.delete_admin,
            self.reset_admin_password
        ]
        self.menu_options += super_admin_options + ["Logout"]
        self.menu_functions += super_admin_functions + [self.logout]
        self.menu = Menu(options=self.menu_options, functions=self.menu_functions)

    # ● To define and add a new admin to the system.
    def add_admin(self):

        print("\n------ Add Admin ------\n")
        member_id = IdFunc.generate_membership_id()

        first_name = input("First name: ")
        last_name = input("Last name: ")
        username = input("Username: ")
        password = get_masked_password()

        if not Checks.username_check(username):
            print("Invalid username")
            return
        
        if not Checks.password_check(password):
            print("Invalid password")
            return
        
        if not Checks.name_check(first_name):
            print("Invalid first name")
            return
        
        if not Checks.name_check(last_name):
            print("Invalid last name")
            return
        
        password = HashFunctions.hash_password(password)


        c = ConnectToDB()
        c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
          (member_id, first_name, last_name, username, password, "2"))
        c.commit()
        c.close()
        
    # ● To modify or update an existing admin’s account and profile.
    def update_admin(self):
        pass

    # ● To delete an existing admin’s account.
    def delete_admin(self):
        
        # TODO make genaric function for this if we have time
        if int(self.level) < 3:
            print("You do not have permission to delete an admin.")
            return
        
        print("\n------ Delete Admin ------\n")

        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE level=?", ("2",))
        users = c.fetchall()
        c.close()

        if len(users) == 0:
            print("0 admin's found in db \n")
            return
        
        print("Admin's in db:")
        for user in users:
            print(f"- {user[0]}")

        username = input("Username: ")
        if not Checks.username_check(username) :
            print("Invalid username")
            return

        # Check if the user is deleted
        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        deleted_user = c.fetchone()
        c.close()

        if deleted_user is None:
            print(f"Admin '{username}' has been deleted successfully.")
        else:
            print(f"Failed to delete admin '{username}'. Please try again.")



    # ● To reset an existing admin’s password (a temporary password).
    def reset_admin_password(self):
        pass