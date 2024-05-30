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
      name = "super_admin"
      password = "Admin_123"
      level = 3
      SuperAdmin = {"id": id, "name": name, "password": password, "level": level}

      id = generate_membership_id()
      name = "admin"
      password = "admin"
      level = 2
      Admin = {"id": id, "name": name, "password": password, "level": level}

      id = generate_membership_id()
      name = "consultant"
      password = "con"
      level = 1
      Consultant = {"id": id, "name": name, "password": password, "level": level}


      # TODO: members have age, first and last name for input. aslo registration date. the ID also has a specific structure (see page 2 assignment)
      id = generate_membership_id()
      name = "member"
      password = "mem"
      level = 0
      Member = {"id": id, "name": name, "password": password, "level": level}

      # Drop the table if it exists
      c.execute("DROP TABLE IF EXISTS users")
      c.execute("DROP TABLE IF EXISTS address")

      # -Users  
      #     First Name, Last Name, Age, Gender, Weight, Email Address, Mobile Phone, Password?
      #         - Mobile Phone (+31-6-DDDDDDDD) – only DDDDDDDD to be entered by the user.
      # -Address
      #     Street name, House number, Zip Code (DDDDXX), City (system should generate a list of 10 city names of your choice predefined in the system

      # Create the 'users' table
      c.execute('''CREATE TABLE users
                  (id TEXT PRIMARY KEY, 
                  name TEXT, 
                  password TEXT, 
                  level INTEGER, 
                  gender TEXT, 
                  weight INTEGER, 
                  email TEXT, 
                  mobile TEXT)''')

      # Create Address Table
      c.execute('''CREATE TABLE address
                  (id TEXT PRIMARY KEY, 
                  user_id TEXT,
                  street TEXT, 
                  house_number INTEGER, 
                  zip_code TEXT, 
                  city TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')

      # Insert the user data into the 'users' table
      c.execute("INSERT INTO users (id, name, password, level, gender, weight, email, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(SuperAdmin['id']), SuperAdmin['name'], SuperAdmin['password'], SuperAdmin['level'], '', 0, '', ''))
      c.execute("INSERT INTO users (id, name, password, level, gender, weight, email, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(Admin['id']), Admin['name'], Admin['password'], Admin['level'], '', 0, '', ''))
      c.execute("INSERT INTO users (id, name, password, level, gender, weight, email, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(Consultant['id']), Consultant['name'], Consultant['password'], Consultant['level'], '', 0, '', ''))
      c.execute("INSERT INTO users (id, name, password, level, gender, weight, email, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(Member['id']), Member['name'], Member['password'], Member['level'], '', 0, '', ''))

      c.execute("INSERT INTO address (id, user_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), str(SuperAdmin['id']), "teststreet", 58, "1029AB", "Rotterdam"))
      c.execute("INSERT INTO address (id, user_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), str(Admin['id']), "teststreet", 58, "1029AB", "Rotterdam"))
      c.execute("INSERT INTO address (id, user_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), str(Consultant['id']), "teststreet", 58, "1029AB", "Rotterdam"))
      c.execute("INSERT INTO address (id, user_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
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
