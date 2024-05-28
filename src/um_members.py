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

from db.db_connection import ConnectToDB
import classes.user as u

def authenticate():
    # This function will authenticate the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username == "Jo" and password == "123":
        print("Welcome!")
    else:
        print("Invalid credentials")




def main():
    while True:
        print("1. Login")
        print("2. Exit")
        menuOption = input("Choose an option: ")
        if menuOption == "1":
            authenticate()
        elif menuOption == "2":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    
    conn = ConnectToDB()

    u = u.User("Jo", "123")

    print("This is a very epic python project biatches")

    main()