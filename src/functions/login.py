import os
import sqlite3

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

def Login():
    username = input("Enter username: ")

    password = input("Enter password: ")

    if not CheckUsername(username):
        print("Invalid username")
        return
    
    if not CheckPassword(password):
        print("Invalid password")
        return

    conn = sqlite3.connect('src/assignment.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))
    users = c.fetchall()
    conn.close()

    if len(users) > 0:
        print("Login successful!")
        # Show nice user and role
        print(f"""
              ████████████████████████████████████████
              ██                                    ██                                   
                      User: {users[0]['name']}         
                                                 
                      Role: {users[0]['level']}   
              ██                                    ██    
              ████████████████████████████████████████
              """)
        print(f"Welcome {users[0]['name']}!")
        print("/////////////////////////")
        return users[0]
    
    else:
        print("Login failed")
        return None
    


def CheckUsername(username):
    if len(username) < 4:
        return False
    
    if len(username) > 20:
        return False
    
    return True

def CheckPassword(password):
    # if len(password) < 8:
    #     return False
    
    if len(password) > 20:
        return False
    
    return True