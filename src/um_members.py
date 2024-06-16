# ==========[CREATED BY]============
# STUDENT 1
# NAME: Joeri Dekker
# STUDENT NUMBER: 1056428 

# STUDENT 2
# NAME: Alysha van Etten
# STUDENT NUMBER: 1023745 

# STUDENT 3
# NAME: Kim leeters
# STUDENT NUMBER: 1039564 
# ===================================

from setup import Setup
from db.db_connection import CreateDB
from classes.consultant import Consultant
from classes.admin import Admin
from classes.super_admin import SuperAdmin
from classes.menu import Menu
from functions.login import Login
from functions.encrypt_functions import EncryptFunc

setup = Setup()
setup.install_required_packages()

def authenticate():
    user = Login()
    if user == None:
        return

    if user['level'] == 1:
        user = Consultant(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    elif user['level'] == 2:
        user = Admin(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    elif user['level'] == 3:
        user = SuperAdmin(user['username'], user['level'])
        while user.logged_in:
            user.display_menu()
    else:
        print("Something went wrong, please try again.")
        input("Press Enter to Continue")

def main():
    print("""
 _   _ _   _ _____ _____ _   _ _____  ___  ___ _____  ___   _      ___  ___ ________  _________ ___________  
| | | | \ | |_   _|  _  | | | |  ___| |  \/  ||  ___|/ _ \ | |     |  \/  ||  ___|  \/  || ___ \  ___| ___ \ 
| | | |  \| | | | | | | | | | | |__   | .  . || |__ / /_\ \| |     | .  . || |__ | .  . || |_/ / |__ | |_/ / 
| | | | . ` | | | | | | | | | |  __|  | |\/| ||  __||  _  || |     | |\/| ||  __|| |\/| || ___ \  __||    /  
| |_| | |\  |_| |_\ \/' / |_| | |___  | |  | || |___| | | || |____ | |  | || |___| |  | || |_/ / |___| |\ \  
 \___/\_| \_/\___/ \_/\_ \___/\____/  \_|  |_/\____/\_| |_/\_____/ \_|  |_/\____/\_|  |_/\____/\____/\_| \_| 
___  ___  ___   _   _   ___  _____  ________  ___ _____ _   _ _____   _______   _______ _____ ________  ___  
|  \/  | / _ \ | \ | | / _ \|  __ \|  ___|  \/  ||  ___| \ | |_   _| /  ___\ \ / /  ___|_   _|  ___|  \/  |  
| .  . |/ /_\ \|  \| |/ /_\ \ |  \/| |__ | .  . || |__ |  \| | | |   \ `--. \ V /\ `--.  | | | |__ | .  . |  
| |\/| ||  _  || . ` ||  _  | | __ |  __|| |\/| ||  __|| . ` | | |    `--. \ \ /  `--. \ | | |  __|| |\/| |  
| |  | || | | || |\  || | | | |_\ \| |___| |  | || |___| |\  | | |   /\__/ / | | /\__/ / | | | |___| |  | |  
\_|  |_/\_| |_/\_| \_/\_| |_/\____/\____/\_|  |_/\____/\_| \_/ \_/   \____/  \_/ \____/  \_/ \____/\_|  |_/ 
        """)

    while True:
        menu = Menu(["Login", "Exit"], [authenticate, exit])
        menu.display()
        menu.execute_choice()


if __name__ == "__main__":
    EncryptFunc.generate_key()
    conn = CreateDB()


    main()