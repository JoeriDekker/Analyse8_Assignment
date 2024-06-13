from classes.menu import Menu
from classes.admin import Admin
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.hash_functions import HashFunctions
import functions.login as Login
from functions.log_functions import LogFunc
from functions.encrypt_functions import EncryptFunc
from db.db_connection import ConnectToDB
import sqlite3

# Super administrator is simply the owner or the manager of the association. 
# The manager needs a super admin password through which can define a system administrator. 
# Although the main function of the super admin is to define system admin(s), and leave the system to them; however, 
# they should be able to perform all possible functionalities of the lower-level users (i.e., system admin and consultant).

# a super admin must be hard coded with username: super_admin, password: Admin_123?

# SUPERADMIN DOES NOT HAVE:
    # ● To update their own password (consultant)

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
    # ● To make a backup of the system and...
    # ● ...restore a backup (members information and users’ data).
    # ● To see the logs file of the system.
    # ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).
# (super admin)
    # ● To define and add a new admin to the system. (complete)
    # ● To modify or update an existing admin’s account and profile. (complete)



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
        self.menu_options += super_admin_options 
        self.menu_functions += super_admin_functions 
        self.menu = Menu(options=self.menu_options[1:] + ["Logout"], functions=self.menu_functions[1:] + [self.logout])


    def add_admin(self):
        
        # asks admin info
        print("Enter the info of the new Admin:")

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


        print("Now adding Admin...")

        # encrypts all given data and adds to database
        encrypted_first_name = EncryptFunc.encrypt_value(first_name)
        encrypted_last_name = EncryptFunc.encrypt_value(last_name)
        encrypted_username = EncryptFunc.encrypt_int_value(username)
        hashed_password = HashFunctions.hash_value(password)
        
        c = ConnectToDB()
        c.execute("INSERT INTO users (id, first_name, last_name, username, level, password) VALUES (?, ?, ?, ?, ?, ?)",
            (str(user_id), encrypted_first_name, encrypted_last_name, encrypted_username, "2", hashed_password))
        c.commit()
        c.close()

        print("Adding Admin successful!")
        LogFunc.append_to_file(f"{self.username}", "Admin added", f"{self.username} added Admin named: {first_name} {last_name}", "no")
        input("Press Enter to Continue")

        
    def update_admin(self):   

        # asks admin username  
        username_input = input("Enter the username of the admin you want to update: ")
        if not Checks.username_check(username_input):
            print("invalid input username, try again.")
            return

        # gets all users
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        c.close()

        admin_info = None
        
        # searches admin by username
        if not users:
            print("user not found in the database.")
            return
        else:
            for user in users:
                if EncryptFunc.decrypt_value(user[3]) == username_input:
                    if user[4] == 2:
                        admin_info = user
                        break
                    else:
                        print("user is not an admin, try again")
                        return

        if admin_info == None:
            print("user not found between users")
            return

        # displays admin info
        print("Current Admin Information:")
        print("ID:", admin_info[0])
        print("First Name:", EncryptFunc.decrypt_value(admin_info[1]))
        print("Last Name:", EncryptFunc.decrypt_value(admin_info[2]))
        print("Username:", EncryptFunc.decrypt_value(admin_info[3]))
        print("Registration Date:", admin_info[6])

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

        print("Updating admin info...")

        # updates admin info in database
        c = ConnectToDB()
        if updated_first_name:
            encrypted_first_name = EncryptFunc.encrypt_value(updated_first_name)
            c.execute("UPDATE users SET first_name=? WHERE id=?", (encrypted_first_name, admin_info[0]))
        if updated_last_name:
            encrypted_last_name = EncryptFunc.encrypt_value(updated_last_name)
            c.execute("UPDATE members SET last_name=? WHERE id=?", (encrypted_last_name, admin_info[0]))
        if updated_username:
            encrypted_username = EncryptFunc.encrypt_int_value(updated_username)
            c.execute("UPDATE members SET username=? WHERE id=?", (encrypted_username, admin_info[0]))

        c.commit()
        c.close()

        print("Admin information updated successfully!")
        LogFunc.append_to_file(f"{self.username}", "Admin updated", f"{self.username} updated admin with Id: {admin_info[0]}", "no")
        input("Press Enter to Continue")
        

    # ● To delete an existing admin’s account.
    def delete_admin(self):
        
        # TODO make genaric function for this if we have time
        if self.level < 3:
            print("You do not have permission to delete an admin.")
            return
        
        print("\n------ Delete Admin ------\n")

        conn = ConnectToDB()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE level=?", ("2",))
        users = c.fetchall()
        c.close()

        if len(users) == 0:
            print("0 admin's found in db \n")
            return
        
        print("Admin's in db:")
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
            print(f"Admin '{username}' has been deleted successfully.")
            LogFunc.append_to_file(f"{self.username}", "Admin deleted", f"{self.username} deleted admin: {username}", "no")
        else:
            print(f"Failed to delete admin '{username}'. Please try again.")



    # ● To reset an existing admin’s password (a temporary password).
    def reset_admin_password(self):
        pass