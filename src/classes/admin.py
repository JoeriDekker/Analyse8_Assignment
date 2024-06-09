# A system administrator is a person who can maintain the system and perform some administration tasks on the application. 
# They are IT technical people and not intended to work with the members. 
# However, for security reasons, they should be able to perform all the functions of consultants, if needed. 
# The minimum required functions of an administrator are listed below:

# FUNCTIONS TO DO:

# (inherited from consultant)

    # ● To update their own password.

    # ● To add a new member to the system.

    # ● To modify or update the information of a member in the system.

    # ● To search and retrieve the information of a member.
import sqlite3
import uuid
from classes.menu import Menu
from classes.consultant import Consultant
import functions.input_checks as input_check
# import db.db_connection as id
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from logger.log import read_log


class Admin(Consultant):
    def __init__(self, username, level):
        super().__init__(username, level)
        admin_options = [
            "Check users", "Add consultant", "Update consultant", "Delete consultant",
            "Reset consultant password", "Backup system", "Restore backup",
            "See logs", "Delete member"
        ]
        admin_functions = [
            self.check_users, self.add_consultant, self.update_consultant, self.delete_consultant,
            self.reset_consultant_password, self.backup_system, self.restore_backup,
            self.see_logs, self.delete_member
        ]
        self.menu_options += admin_options + ["Logout"]
        self.menu_functions += admin_functions + [self.logout]
        self.menu = Menu(options=self.menu_options, functions=self.menu_functions)
        
    @staticmethod
    def connect_to_db():
        return sqlite3.connect('src/assignment.db')

    # ● To check the list of users and their roles. (member to admin??)
    def check_users(self):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT id, username, level FROM users")
        users = c.fetchall()
        conn.close()
        
        print("List of users:")
        for user in users:
            if user[2] == 0:
                print(f"Name: {user[1]}, Role: Member")
            elif user[2] == 1:
                print(f"Name: {user[1]}, Role: Consultant")
            
            elif user[2] == 2:
                print(f"Name: {user[1]}, Role: Admin")
            else:
                print(f"Name: {user[1]}, Role: Super Admin")
    
    # ● To define and add a new consultant to the system.
    def add_consultant(self):
        print("=== ADD CONSULTANT ===\n")

        print("Enter username: ")
        username = input("")
        print("Enter password: ")
        password = input("")
        
        if (input_check.username_check(username) & input_check.password_check(password)):
            print("Enter first name: ")
            firstName = input("")
            print("Enter last name: ")
            lastName = input("")
            conID = generate_membership_id()

            if conID is not None:
            # conn = self.connect_to_db()
            # c = conn.cursor()
            # c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
            #           (str(id.generate_membership_id), firstName, lastName, username, password, 1))
            # conn.commit()

                print(str(conID), firstName, lastName, username, password, 1)
            else:
                print("Failed to generate a valid membership ID.")
                return   
        else:
            return

    # ● To modify or update an existing consultant’s account and profile.
    def update_consultant(self):
        pass

    # ● To delete an existing consultant’s account.
    def delete_consultant(self):
        pass

    # ● To reset an existing consultant’s password (a temporary password).
    def reset_consultant_password(self):
        pass

    # ● To make a backup of the system... 
    def backup_system(self):
        pass

    # ...and restore a backup (members information and users’ data).
    def restore_backup(self):
        pass

    # ● To see the logs file(s) of the system.
    def see_logs(self):
        read_log()

    # ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).
    def delete_member(self):
        pass