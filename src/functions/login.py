import sqlite3

from functions.input_checks import Checks
from functions.hash_functions import HashFunctions
from functions.mask_functions import MaskFunc

from logger.log import append_to_file

def Login():
    attempt_count = 0
    while attempt_count < 3:
        print("Enter username: ")
        username = input("")

        print("Enter password: ")
        password = MaskFunc.get_masked_password()

        if not Checks.username_check(username) or not Checks.password_check(password) :
            print("Invalid username or password")
        if Checks.username_check(username) and Checks.password_check(password) or username == "super_admin" and Checks.password_check(password):
            conn = sqlite3.connect('src/assignment.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            users = c.fetchall()
            conn.close()

            if len(users) > 0:
                if HashFunctions.check_password(password, users[0]['password']):
                    print("Login successful!")
                    # Show nice user and role
                    print(f"""
                        ████████████████████████████████████████
                        ██                                    ██                                   
                                User: {users[0]['username']}         
                                                            
                                Role: {users[0]['level']}   
                        ██                                    ██    
                        ████████████████████████████████████████
                        """)
                    append_to_file(f"{username}", "Succesful login", "", "no")
                    return users[0]

        
        attempt_count += 1
        if attempt_count == 3:
            print("----------\nToo many failed login attempts. going back.\n----------")
            append_to_file("...", "Unsuccesful login", f"username: '{username}' is used for a login attempt with a wrong password ", "no")
            return None
        else:
            append_to_file("...", "Unsuccesful login", f"multiple login fails from single user", "yes")
        
        print("1. Try again")
        print("2. Return to menu")
        option = input("Enter your option: ")
        if option == '1':
            continue
        elif option == '2':
            return None
        else:
            print("Invalid option. Please enter 1 or 2.")
                
        
    