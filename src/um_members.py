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
import sys

from db.db_connection import ConnectToDB
from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin
from classes.menu import Menu


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
            user = Admin(username, level)
            user.display_menu()
        elif level == "2":
            user = SuperAdmin(username, level)
            user.display_menu()
    else:
        print("Invalid credentials")

# get single character from input
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