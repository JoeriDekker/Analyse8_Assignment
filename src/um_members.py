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
    
from db.db_connection import CreateDB, ConnectToDB, CreateSuperAdmin

from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin

from classes.menu import Menu
from functions.login import Login
from functions.encrypt_functions import EncryptFunc
from functions.backup_functions import BackupFunc
from functions.log_functions import LogFunc
import datetime


def authenticate():
    user = Login()
    if user == None:
        return
    

    if user['level'] == 1:
        user = Consultant(EncryptFunc.decrypt_value(user['username']), user['level'])
        while user.logged_in:
            user.display_menu()
    elif user['level'] == 2:
        user = Admin(EncryptFunc.decrypt_value(user['username']), user['level'])
        while user.logged_in:
            user.display_menu()
    elif user['level'] == 3:
        user = SuperAdmin(EncryptFunc.decrypt_value(user['username']), user['level'])
        while user.logged_in:
            user.display_menu()
    else:
        print("Something went wrong, please try again.")
        input("Press Enter to Continue")
  



def easy_login():
    print("1. Consultant \n2. Admin \n3. Super Admin")
    user = input("Enter level:")

    if user == "1":
        user = Consultant("Consultant", 1)
        while user.logged_in:
            user.display_menu()
    elif user == "2":
        user = Admin("admin", 2)
        while user.logged_in:
            user.display_menu()
    elif user == "3":
        user = SuperAdmin("super admin", 3)
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
    # while True:
    #     menu = Menu(["Login", "Exit"], [authenticate, exit])
    #     menu.display()
    #     menu.execute_choice()

    easy_login()
    # LogFunc.append_to_file("...", "Unsuccesful login", f"username: 'ssdf' is used for a login attempt with a wrong password ", "no")
    # LogFunc.read_log()
    # input("Press Enter to Continue")
    # BackupFunc.CreateBackup()
    # LogFunc.read_log()
    # input("Press Enter to Continue")
    # LogFunc.append_to_file("...", "Unsuccesful login", f"username: 'ssdf22' is used for a login attempt with a wrong password ", "no")
    # LogFunc.read_log()
    # input("Press Enter to Continue")
    # BackupFunc.RestoreBackup()
    # LogFunc.read_log()

    
    # FileFunc.generate_key()
    # FileFunc.encrypt_file()
    # input("Press Enter to Continue")
    # FileFunc.decrypt_file()
    # input("Press Enter to Continue")
    # FileFunc.encrypt_file()
    


if __name__ == "__main__":
    # EncryptFunc.generate_key()
    conn = CreateDB()


    main()