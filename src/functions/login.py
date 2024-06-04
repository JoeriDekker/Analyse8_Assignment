import os
import sqlite3

import functions.input_checks as input_check

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
    print("Enter username: ")
    username = input("")

    print("Enter password: ")
    password = get_masked_password()

    if not input_check.username_check(username) or not input_check.password_check(password):
        return
    
    conn = sqlite3.connect('src/assignment.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    users = c.fetchall()
    conn.close()

    if len(users) > 0:
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
        return users[0]
    
    else:
        print("Login failed")
        return None
    

