import sqlite3

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
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))
    users = c.fetchall()
    conn.close()

    if len(users) > 0:
        print("Login successful!")
        return users[0]
    


def CheckUsername(username):
    if len(username) < 4:
        return False
    
    if username.length() > 20:
        return False
    
    return True

def CheckPassword(password):
    if len(password) < 8:
        return False
    
    if password.length() > 20:
        return False
    
    return True