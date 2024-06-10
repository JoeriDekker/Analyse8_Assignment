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

from setup import Setup

setup = Setup()
setup.install_required_packages()
    
from db.db_connection import CreateDB, ConnectToDB

from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin

from classes.menu import Menu
from functions.login import Login
from functions.file_funcions import FileFunc


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
        user = SuperAdmin(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    else:
        print("Something went wrong, please try again.")
        input("Press Enter to Continue")
  



def easy_login():
    print("1. Consultant \n2. Admin \n3. Super Admin")
    user = input("Enter level:")

    if user == "1":
        user = Consultant("Consultant", "1")
        while user.logged_in:
            user.display_menu()
    elif user == "2":
        user = Admin("admin", "2")
        while user.logged_in:
            user.display_menu()
    elif user == "3":
        user = SuperAdmin("super admin", "3")
        while user.logged_in:
            user.display_menu()
    else:
        print("Something went wrong, please try again.")
        input("Press Enter to Continue")

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

    # FileFunc.generate_key()
    # FileFunc.encrypt_file()
    # input("Press Enter to Continue")
    # FileFunc.decrypt_file()
    # input("Press Enter to Continue")
    # FileFunc.encrypt_file()
    


if __name__ == "__main__":
    conn = CreateDB()


    main()