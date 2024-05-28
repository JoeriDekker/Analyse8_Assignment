import sqlite3
import classes.user as u
import uuid


def ConnectToDB():
    conn = sqlite3.connect('src/assignment.db')

    # Create a cursor object
    c = conn.cursor()

    # Create a User object
    # create uuid for each user
    id = uuid.uuid4()
    name = "super_admin"
    password = "Admin_123"
    level = 2
    SuperAdmin = {"id": id, "name": name, "password": password, "level": level}

    id = uuid.uuid4()
    name = "admin"
    password = "admin"
    level = 2
    Admin = {"id": id, "name": name, "password": password, "level": level}

    id = uuid.uuid4()
    name = "consultant"
    password = "con"
    level = 1
    Consultant = {"id": id, "name": name, "password": password, "level": level}

    id = uuid.uuid4()
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

