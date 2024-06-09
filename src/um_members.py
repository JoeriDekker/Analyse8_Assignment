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
import setup

from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin

from classes.menu import Menu
from functions.login import Login


def authenticate():
    user = Login()

    if user == None:
        return

    if str(user['level']) == "1":
        user = Consultant(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    elif str(user['level']) == "2":
        user = Admin(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    elif str(user['level']) == "3":
        user = SuperAdmin(user['unsername'], user['level'])
        while user.logged_in:
            user.display_menu()
    else:
        print("Something went wrong, please try again.")
        input("Press Enter to Continue")
  

def exit():
    print("Goodbye!")
    quit()

def main():
    Menu.clear_screen(Menu)

    print("""
        ░█████╗░███╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗░██████╗███████╗  ░█████╗░
        ██╔══██╗████╗░██║██╔══██╗██║░░░░░╚██╗░██╔╝██╔════╝██╔════╝  ██╔══██╗
        ███████║██╔██╗██║███████║██║░░░░░░╚████╔╝░╚█████╗░█████╗░░  ╚█████╔╝
        ██╔══██║██║╚████║██╔══██║██║░░░░░░░╚██╔╝░░░╚═══██╗██╔══╝░░  ██╔══██╗
        ██║░░██║██║░╚███║██║░░██║███████╗░░░██║░░░██████╔╝███████╗  ╚█████╔╝
        ╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═════╝░╚══════╝  ░╚════╝░

        ░█████╗░░██████╗░██████╗██╗░██████╗░███╗░░██╗███╗░░░███╗███████╗███╗░░██╗████████╗
        ██╔══██╗██╔════╝██╔════╝██║██╔════╝░████╗░██║████╗░████║██╔════╝████╗░██║╚══██╔══╝
        ███████║╚█████╗░╚█████╗░██║██║░░██╗░██╔██╗██║██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░
        ██╔══██║░╚═══██╗░╚═══██╗██║██║░░╚██╗██║╚████║██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░
        ██║░░██║██████╔╝██████╔╝██║╚██████╔╝██║░╚███║██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░
        ╚═╝░░╚═╝╚═════╝░╚═════╝░╚═╝░╚═════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░
        ===================================================================
          
          """)
    while True:
        menu = Menu(["Login", "Exit"], [authenticate, exit])
        menu.display()
        menu.execute_choice()

if __name__ == "__main__":
    conn = CreateDB()


    main()