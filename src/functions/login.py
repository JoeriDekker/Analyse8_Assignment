import sqlite3
import os

from functions.input_checks import Checks
from functions.hash_functions import HashFunctions
from functions.encrypt_functions import EncryptFunc

from functions.log_functions import LogFunc

def getch():
        # if windows system
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8')
        # if unix based system
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

# masks password while asking for input with asterisks
def get_masked_password():
    # TODO: if else statement with second part for unix based
    password = ''
    while True:
        ch = getch()
        # if enter is pressed, break
        if ch == '\n' or ch == '\r':
            break
        # if backspace is pressed
        elif ch == '\x08' or ch == '\x7f':
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        # if pressed char is printable, add asterisks, else dont
        elif 32 <= ord(ch) <= 126:
            password += ch
            print('*', end='', flush=True)
    print()
    return str(password)

def Login():
    attempt_count = 0
    while attempt_count < 3:
        print("Enter username: ")
        username = input("")

        print("Enter password: ")
        password = get_masked_password()

        if Checks.username_check(username) and Checks.password_check(password) or username == "super_admin" and password == "Admin_123?":
            conn = sqlite3.connect('assignment.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            users = c.fetchall()
            conn.close()

            found_user = None

            for user in users:
                user_dict = dict(user)
                user_dict['username'] = EncryptFunc.decrypt_value(user_dict['username'])
                if user_dict['username'] == username:
                    found_user = user_dict

            if not found_user is None:
                if HashFunctions.check_password(password, found_user['password']):
                    print("Login successful!")
                    # Show nice user and role
                    print(f"""
████████████████████████████████████████
██                                    ██                                   
        User: {found_user['username']}         
                                    
        Role: {found_user['level']}   
██                                    ██    
████████████████████████████████████████
                        """)
                    LogFunc.append_to_file(f"{username}", "Succesful login", "", "no")
                    return found_user
        else:
            print("Invalid username or password")

        
        attempt_count += 1
        if attempt_count == 3:
            print("----------\nToo many failed login attempts. going back.\n----------")
            LogFunc.append_to_file("...", "Unsuccesful login", f"multiple login fails from single user", "yes")
            return None
        else:
            LogFunc.append_to_file("...", "Unsuccesful login", f"username: '{username}' is used for a login attempt with a wrong password ", "no")
        
        print("1. Try again")
        print("2. Return to menu")
        option = input("Enter your option: ")
        if option == '1':
            continue
        elif option == '2':
            return None
        else:
            print("Invalid option. Please enter 1 or 2.")
                
        
    