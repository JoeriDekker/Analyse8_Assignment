import sqlite3
from functions.id_functions import IdFunc
from functions.hash_functions import HashFunctions
from functions.encrypt_functions import EncryptFunc

def ConnectToDB():
    conn = sqlite3.connect('assignment.db')
    return conn


def CreateDB():
      conn = sqlite3.connect('assignment.db')
      c = conn.cursor()

      # Create the 'users' table
      c.execute('''CREATE TABLE IF NOT EXISTS users
                  (id TEXT PRIMARY KEY, 
                  first_name TEXT,
                  last_name TEXT, 
                  username TEXT,
                  level INTEGER, 
                  password TEXT,
                  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
      
      # Create the 'members' table
      c.execute('''CREATE TABLE IF NOT EXISTS members
                  (id TEXT PRIMARY KEY, 
                  first_name TEXT,
                  last_name TEXT, 
                  age INTEGER,
                  gender TEXT, 
                  weight INTEGER, 
                  email TEXT, 
                  phone_number TEXT,
                  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

      # Create Address Table
      c.execute('''CREATE TABLE IF NOT EXISTS address
                  (id TEXT PRIMARY KEY, 
                  member_id TEXT,
                  street TEXT, 
                  house_number INTEGER, 
                  zip_code TEXT, 
                  city TEXT,
                  FOREIGN KEY(member_id) REFERENCES members(id))''')

      
      conn.commit()
      CreateSuperAdmin()

      return conn

def CreateSuperAdmin():
      conn = sqlite3.connect('assignment.db')
      c = conn.cursor()

      c.execute('''SELECT * FROM users ''')
      users = c.fetchall()
      conn.close()

      if len(users) > 0:
            for user in users:
                  if EncryptFunc.decrypt_value(user[3]) == "super_admin":
                        return
                  
      conn = sqlite3.connect('assignment.db')
      c = conn.cursor()
      id = IdFunc.generate_membership_id()
      first_name = EncryptFunc.encrypt_value("super")
      last_name = EncryptFunc.encrypt_value("admin")
      username = EncryptFunc.encrypt_value("super_admin")
      level = 3
      password = HashFunctions.hash_value("Admin_123?")
      # get current date  
      SuperAdmin = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}
      
      # Insert the user data into the 'users' table
      c.execute('''INSERT INTO users (id, first_name, last_name, username, password, level) 
                  VALUES (?, ?, ?, ?, ?, ?)''',
                  (str(SuperAdmin['id']), SuperAdmin['first_name'], SuperAdmin['last_name'], SuperAdmin['username'], SuperAdmin['password'], SuperAdmin['level']))
      conn.commit()
      
      conn.close()


if __name__ == "__main__":
    conn = CreateDB()
    print("Database created successfully!")
    conn.close()
