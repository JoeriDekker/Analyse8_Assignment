import sqlite3
from classes.menu import Menu
from classes.consultant import Consultant
from functions.backup_functions import BackupFunc
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.log_functions import LogFunc
from functions.hash_functions import HashFunctions
from functions.encrypt_functions import EncryptFunc
from db.db_connection import ConnectToDB
import functions.login as Login


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
# (admin)
    # ● To check the list of users and their roles.
    # ● To define and add a new consultant to the system. (complete)
    # ● To modify or update an existing consultant’s account and profile. (complete)
    # ● To delete an existing consultant’s account. (complete)
    # ● To reset an existing consultant’s password (a temporary password).
    # ● To make a backup of the system... 
    # ...and restore a backup (members information and users’ data).
    # ● To see the logs file(s) of the system.
    # ● To delete a member's record from the database.


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
    

    def add_consultant(self):

        # asks consultant info
        print("Enter the info of the new Consultant:")

        user_id = IdFunc.generate_membership_id()

        first_name = input("First name: ")
        if not Checks.string_check(first_name):
            print("first name too long or empty, try again.")
            return
        
        last_name = input("Last name: ")
        if not Checks.string_check(last_name):
            print("last name too long or empty, try again.")
            return
        
        print("- between 8 and 10 characters\n- only letters, numbers and underscores")
        username = input("Username: ")
        if not Checks.username_check(username):
            print("invalid username, try again.")
            return
        if not Checks.username_available_check(username):
            print("username already in use, try again")
            return
        
        print("- must have a length of at least 12 characters\n- must be no longer than 30 characters\n- must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character")
        print("Enter password: ")
        password = Login.get_masked_password()
        if not Checks.password_check(password):
            print("Invalid password")


        print("Now adding Consultant...")

        # encrypts all given data and adds to database
        encrypted_first_name = EncryptFunc.encrypt_value(first_name)
        encrypted_last_name = EncryptFunc.encrypt_value(last_name)
        encrypted_username = EncryptFunc.encrypt_int_value(username)
        hashed_password = HashFunctions.hash_value(password)
        
        c = ConnectToDB()
        c.execute("INSERT INTO users (id, first_name, last_name, username, level, password) VALUES (?, ?, ?, ?, ?, ?)",
            (str(user_id), encrypted_first_name, encrypted_last_name, encrypted_username, "1", hashed_password))
        c.commit()
        c.close()

        print("Adding Consultant successful!")
        LogFunc.append_to_file(f"{self.username}", "Consultant added", f"{self.username} added Consultant named: {first_name} {last_name}", "no")
        input("Press Enter to Continue")


    def update_consultant(self):

        # asks consultant username  
        username_input = input("Enter the username of the consultant you want to update: ")
        if not Checks.username_check(username_input):
            print("invalid input username, try again.")
            return

        # gets all users
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        c.close()

        consult_info = None
        
        # searches consultant by username
        if not users:
            print("user not found in the database.")
            return
        else:
            for user in users:
                if EncryptFunc.decrypt_value(user[3]) == username_input:
                    if user[4] == 1:
                        consult_info = user
                        break
                    else:
                        print("user is not an consultant, try again")
                        return

        if consult_info == None:
            print("user not found between users")
            return

        # displays consultant info
        print("Current Consultant Information:")
        print("ID:", consult_info[0])
        print("First Name:", EncryptFunc.decrypt_value(consult_info[1]))
        print("Last Name:", EncryptFunc.decrypt_value(consult_info[2]))
        print("Username:", EncryptFunc.decrypt_value(consult_info[3]))
        print("Registration Date:", consult_info[6])

        # asks for updated information
        print("\nEnter the updated information (leave blank if not updating):")

        updated_first_name = input("First name: ").strip()
        if updated_first_name:
            if not Checks.string_check(updated_first_name):
                print("name too long or empty, try again.")
                return
            
        updated_last_name = input("Last name: ").strip()
        if updated_last_name:
            if not Checks.string_check(updated_last_name):
                print("name too long or empty, try again.")
                return
            
        print("- between 8 and 10 characters\n- only letters, numbers and underscores")
        updated_username = input("Username: ").strip()
        if updated_username:
            if not Checks.username_check(updated_username):
                print("invalid username, try again.")
                return
            if not Checks.username_available_check(updated_username):
                print("username already in use, try again")
                return

        print("Updating consultant info...")

        # updates consultant info in database
        c = ConnectToDB()
        if updated_first_name:
            encrypted_first_name = EncryptFunc.encrypt_value(updated_first_name)
            c.execute("UPDATE users SET first_name=? WHERE id=?", (encrypted_first_name, consult_info[0]))
        if updated_last_name:
            encrypted_last_name = EncryptFunc.encrypt_value(updated_last_name)
            c.execute("UPDATE users SET last_name=? WHERE id=?", (encrypted_last_name, consult_info[0]))
        if updated_username:
            encrypted_username = EncryptFunc.encrypt_int_value(updated_username)
            c.execute("UPDATE users SET username=? WHERE id=?", (encrypted_username, consult_info[0]))

        c.commit()
        c.close()

        print("Consultant information updated successfully!")
        LogFunc.append_to_file(f"{self.username}", "Consultant updated", f"{self.username} updated consultant with Id: {consult_info[0]}", "no")
        input("Press Enter to Continue")


    def delete_consultant(self):

        # asks consultant username  
        username_input = input("Enter the username of the consultant you want to delete: ")
        if not Checks.username_check(username_input):
            print("invalid input username, try again.")
            return

        # gets all users
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        c.close()

        consult_to_delete = None
        
        # searches consultant by username
        if not users:
            print("user not found in the database.")
            return
        else:
            for user in users:
                if EncryptFunc.decrypt_value(user[3]) == username_input:
                    if user[4] == 1:
                        consult_to_delete = user
                        break
                    else:
                        print("user is not an consultant, try again")
                        return

        if consult_to_delete == None:
            print("user not found between users")
            return
        
        # deletes the consultant
        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (consult_to_delete[0],))
        conn.commit()
        c.close()

        # checks if the user is deleted
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE id=?", (consult_to_delete[0],))
        deleted_user = c.fetchone()
        c.close()

        if deleted_user:
            print(f"Failed to delete consultant '{username_input}'. Please try again.")
            return
        
        print(f"Consultant '{username_input}' has been deleted successfully.")
        LogFunc.append_to_file(f"{self.username}", "Consultant deleted", f"{self.username} deleted consultant: {username_input}", "no")
        input("Press Enter to Continue")

    def reset_consultant_password(self):
        pass

    def backup_system(self):
        print("\n--- Backup System ---\n")
        BackupFunc.CreateBackup()
        LogFunc.append_to_file(self.username, "Backup system", f"{self.username} has created an backup of the system", "no")
        input("Press Enter to Continue")

    def restore_backup(self):
        pass

    def see_logs(self):
        LogFunc.read_log()

    def delete_member(self):
        pass