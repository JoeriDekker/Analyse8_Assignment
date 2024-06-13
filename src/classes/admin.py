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
# import functions.input_checks as input_check
# import db.db_connection as id
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.log_functions import LogFunc
from functions.hash_functions import HashFunctions
from functions.encrypt_functions import EncryptFunc


from db.db_connection import ConnectToDB
import sqlite3


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
        self.menu_options += admin_options 
        self.menu_functions += admin_functions 
        self.menu = Menu(options=self.menu_options + ["Logout"], functions=self.menu_functions + [self.logout])
        
    @staticmethod
    def connect_to_db():
        return sqlite3.connect('assignment.db')

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
        if self.level < 2:
            print("You do not have permission to add a consultant.")
            return

        print("------ Add Consultant ------\n")

        print("Enter username: ")
        username = input("")
        print("Enter password: ")
        password = input("")
        
        # TODO: Add check if username does not already exist in db
        if (Checks.username_check(username) & Checks.password_check(password)):
            print("Enter first name: ")
            firstName = input("")
            print("Enter last name: ")
            lastName = input("")
            conID = IdFunc.generate_membership_id()
            password = HashFunctions.hash_password(password)

            if conID is not None:
                conn = self.connect_to_db()
                c = conn.cursor()
                c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
                        (str(conID), EncryptFunc.encrypt_value(firstName), EncryptFunc.encrypt_value(lastName), EncryptFunc.encrypt_value(username), password, 1))
                conn.commit()

            else:
                print("Failed to generate a valid membership ID.")
                return   
        else:
            print("failed adding a consultant")
            return

    # ● To modify or update an existing consultant’s account and profile.
    def update_consultant(self):
        print("------ Update Consultant ------\n")

        print("Enter username: ")
        username = input("")

        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute("UPDATE members SET first_name=? WHERE last_name=?", (updated_first_name, last_name_input))
        conn.commit()


    # ● To delete an existing consultant’s account.
    def delete_consultant(self):
        # TODO make genaric function for this if we have time
        print(self.level)
        if self.level < 2:
            print("You do not have permission to delete a consultant.")
            return
        
        print("\n------ Delete Consultant ------\n")

        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE level=?", ("1",))
        users = c.fetchall()
        c.close()

        if len(users) == 0:
            print("0 Consultant's found in db \n")
            return
        
        print("Consultant's in db:")
        for user in users:
            print(f"- {EncryptFunc.decrypt_value(user[1])}")

        username = input("Username: ")
        if not Checks.username_check(username) :
            print("Invalid username")
            return
        
        user_to_delete = None

        for user in users:
            if EncryptFunc.decrypt_value(user[1]) == username:
                user_to_delete = user[1]
                break
        # Check if the user is deleted
        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (user_to_delete,))
        conn.commit()  # Commit the changes
        c.close()

        # Check if the user is deleted
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=?", (user_to_delete,))
        deleted_user = c.fetchone()
        c.close()


        if deleted_user is None:
            print(f"Consultant '{username}' has been deleted successfully.")
        else:
            print(f"Failed to delete Consultant '{username}'. Please try again.")

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
        LogFunc.read_log()

    # ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).
    def delete_member(self):
        pass