import sqlite3
import uuid
import datetime
import random

def ConnectToDB():
    conn = sqlite3.connect('src/assignment.db')
    return conn


def CreateDB():
      conn = sqlite3.connect('src/assignment.db')

      # Create a cursor object
      c = conn.cursor()

      # Create a User object
      # create uuid for each user
      id = generate_membership_id()
      first_name = "Sjaak"
      last_name = "Minton"
      username = "super_admin"
      level = 3
      password = "Supersecret123!"
      SuperAdmin = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      id = generate_membership_id()
      first_name = "Klaas"
      last_name = "Jansen"
      username = "admin_acc"
      level = 2
      password = "Supersecret123!"
      Admin = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      id = generate_membership_id()
      first_name = "Samantha"
      last_name = "Julias"
      username = "Consultant"
      level = 1
      password = "Supersecret123!"
      Consultant = {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "level": level, "password": password}

      # TODO: members have age, first and last name for input. aslo registration date. the ID also has a specific structure (see page 2 assignment)
      id = generate_membership_id()
      first_name = "John"
      last_name = "Doe"
      age = 25
      gender = "M"
      weight = 80
      email = "joe@doe.com"
      phone_number = "0612345678"

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
            (str(uuid.uuid4()), str(Member['id']), "teststreet", 58, "1029AB", "Rotterdam"))

      # Commit the changes
      conn.commit()

      return conn

def generate_membership_id():
      # Get the current year
      current_year = datetime.datetime.now().year

      # Get first two digits of the current year
      first_two_digits = str(current_year)[2:]

      # Create 7 random digits
      random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])

      # calculate the checksum for last digit
      checksum = sum(int(digit) for digit in first_two_digits + random_digits) % 10

      # Return the membership ID
      finalnumber = first_two_digits + random_digits + str(checksum)

      if is_valid_membership_id(finalnumber):
            return finalnumber
      else:
            print("Error: Invalid membership ID generated")
            return None
      

def is_valid_membership_id(id):
    # Check if the length is correct
    if len(id) != 10:
        return False

    # Check if the first two digits are less than or equal to the current year
    if int(id[:2]) > int(str(datetime.datetime.now().year)[2:]):
        return False

    # Calculate the checksum
    checksum = sum(int(digit) for digit in id[:9]) % 10

    # Check if the checksum is correct
    if checksum != int(id[9]):
        return False

    # If all checks passed, the ID is valid
    return True



if __name__ == "__main__":
    conn = CreateDB()
    print("Database created successfully!")
    conn.close()
