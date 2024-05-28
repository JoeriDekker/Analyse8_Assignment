# ==========[CREATED BY]============
# STUDENT 1
# NAME: Joeri Dekker
# STUDENT NUMBER:

# STUDENT 2
# NAME: Alysha van Etten
# STUDENT NUMBER: 

# STUDENT 3
# NAME: Kim leeters
# STUDENT NUMBER:
# ===================================

import os
from db.db_connection import ConnectToDB
from classes.consultant import Consultant
from classes.menu import Menu
import sys

def authenticate():
    # This function will authenticate the user
    username = input("Enter your username: ")
    print("Enter your password: ", end='', flush=True)
    password = get_masked_password()
    level = input("Enter your level: ")

    if username == "Jo" and password == "123":
        if level == "0":
            user = Consultant(username, level)
            user.display_menu()
        elif level == "1":
            user = Consultant(username, level)
            user.display_menu()
        elif level == "2":
            user = Consultant(username, level)
            user.display_menu()
    else:
        print("Invalid credentials")

def getch():
    """Gets a single character from standard input. Works on Windows and Unix-like systems."""
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode('utf-8')
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
    
def get_masked_password():
    """Prompts for password input while masking the input characters with asterisks."""
    password = ''
    while True:
        ch = getch()
        if ch == '\n' or ch == '\r':
            break
        elif ch == '\x08' or ch == '\x7f':
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        elif 32 <= ord(ch) <= 126:
            password += ch
            print('*', end='', flush=True)
    print()
    return password

def exit():
    print("Goodbye!")
    quit()

def main():
    while True:
        menu = Menu(["Login", "Exit"], [authenticate, exit])
        menu.display()
        menu.execute_choice()

if __name__ == "__main__":
    
    conn = ConnectToDB()

    print("This is a very epic python project biatches")

    main()