import sqlite3
import uuid
from functions.id_functions import IdFunc
from functions.hash_functions import HashFunctions
from functions.encrypt_functions import EncryptFunc

def ConnectToDB():
    conn = sqlite3.connect('src/assignment.db')
    return conn


def CreateDB():
      conn = sqlite3.connect('src/assignment.db')

      # Create a cursor object
      c = conn.cursor()

      # Create a User object
      # create uuid for each user
      id = IdFunc.generate_membership_id()
      first_name = EncryptFunc.encrypt_value("Sjaak")
      last_name = EncryptFunc.encrypt_value("Minton")
      username = EncryptFunc.encrypt_value("super_admin")
      level = 3
      password = HashFunctions.hash_value("Admin_123?")
      SuperAdmin = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      id = IdFunc.generate_membership_id()
      first_name = EncryptFunc.encrypt_value("Klaas")
      last_name = EncryptFunc.encrypt_value("Jansen")
      username = EncryptFunc.encrypt_value("admin_acc")
      level = 2
      password = HashFunctions.hash_value("Supersecret123!")
      Admin = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      id = IdFunc.generate_membership_id()
      first_name = EncryptFunc.encrypt_value("Samantha")
      last_name = EncryptFunc.encrypt_value("Julias")
      username = EncryptFunc.encrypt_value("Consultant")
      level = 1
      password = HashFunctions.hash_value("Supersecret123!")
      Consultant = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      # TODO: members have age, first and last name for input. aslo registration date. the ID also has a specific structure (see page 2 assignment)
      id = IdFunc.generate_membership_id()
      first_name = EncryptFunc.encrypt_value("John")
      last_name = EncryptFunc.encrypt_value("Doe")
      age = EncryptFunc.encrypt_value(25)
      gender = EncryptFunc.encrypt_value("M")
      weight = EncryptFunc.encrypt_value(80)
      email = EncryptFunc.encrypt_value("joe@doe.com")
      phone_number = EncryptFunc.encrypt_value("0612345678")

      Member = {"id": id, "first_name": first_name, "last_name": last_name, "age": age, "gender":gender, "weight": weight, "email": email, "phone_number": phone_number}

      # Drop the table if it exists
      c.execute("DROP TABLE IF EXISTS users")
      c.execute("DROP TABLE IF EXISTS address")
      c.execute("DROP TABLE IF EXISTS members")

      # -Users  
      #     First Name, Last Name, Age, Gender, Weight, Email Address, Mobile Phone, Password?
      #         - Mobile Phone (+31-6-DDDDDDDD) – only DDDDDDDD to be entered by the user.
      # -Address
      #     Street name, House number, Zip Code (DDDDXX), City (system should generate a list of 10 city names of your choice predefined in the system

     
      
      # Create the 'users' table
      c.execute('''CREATE TABLE users
                  (id TEXT PRIMARY KEY, 
                  first_name TEXT,
                  last_name TEXT, 
                  username TEXT,
                  level INTEGER, 
                  password TEXT)''')
      
      # Create the 'members' table
      c.execute('''CREATE TABLE members
                  (id TEXT PRIMARY KEY, 
                  first_name TEXT,
                  last_name TEXT, 
                  age INTEGER,
                  gender TEXT, 
                  weight INTEGER, 
                  email TEXT, 
                  phone_number TEXT)''')

      # Create Address Table
      c.execute('''CREATE TABLE address
                  (id TEXT PRIMARY KEY, 
                  member_id TEXT,
                  street TEXT, 
                  house_number INTEGER, 
                  zip_code TEXT, 
                  city TEXT,
                  FOREIGN KEY(member_id) REFERENCES members(id))''')

      # Insert the user data into the 'users' table
      c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
            (str(SuperAdmin['id']), SuperAdmin['first_name'], SuperAdmin['last_name'], SuperAdmin['username'], SuperAdmin['password'], SuperAdmin['level']))
      c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
            (str(Admin['id']), Admin['first_name'], Admin['last_name'], Admin['username'], Admin['password'], Admin['level']))
      c.execute("INSERT INTO users (id, first_name, last_name, username, password, level) VALUES (?, ?, ?, ?, ?, ?)",
            (str(Consultant['id']), Consultant['first_name'], Consultant['last_name'], Consultant['username'], Consultant['password'], Consultant['level']))
      

      c.execute("INSERT INTO members (id, first_name, last_name, age, gender, weight, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(Member['id']), Member['first_name'], Member['last_name'], Member['age'], Member['gender'], Member['weight'], Member['email'], Member['phone_number']))

      c.execute("INSERT INTO address (id, member_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), str(Member['id']), EncryptFunc.encrypt_value("teststreet"), EncryptFunc.encrypt_value(58), EncryptFunc.encrypt_value("1029AB"), EncryptFunc.encrypt_value("Rotterdam")))

      # Commit the changes
      conn.commit()

      return conn


if __name__ == "__main__":
    conn = CreateDB()
    print("Database created successfully!")
    conn.close()
