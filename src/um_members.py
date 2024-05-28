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
from db.db_connection import CreateDB, ConnectToDB
import sys

from db.db_connection import ConnectToDB
from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin

from classes.menu import Menu
from functions.login import Login


def authenticate():
    # Login()
    # This function will authenticate the user
    username = input("Enter your username: ")

    password = input("Enter your password: ")
    
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



def exit():
    print("Goodbye!")
    quit()

def main():
    while True:
        menu = Menu(["Login", "Exit"], [authenticate, exit])
        menu.display()
        menu.execute_choice()

if __name__ == "__main__":
    
    conn = CreateDB()

    print("This is a very epic python project biatches")

    main()