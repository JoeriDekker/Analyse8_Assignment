import sqlite3
import classes.user as u


def ConnectToDB():
    conn = sqlite3.connect('src/assignment.db')

    # Create a cursor object
    c = conn.cursor()

    # Create a User object
    user = u.User("John", "buurtboer :)")

    # Drop the table if it exists
    c.execute("DROP TABLE IF EXISTS users")

    # Create a table
    c.execute('''Create TABLE IF NOT EXISTS users
             (name text, password text)''')

    # Insert the user data into the 'users' table
    c.execute("INSERT INTO users VALUES (?, ?)", (user.name, user.password))

    # Commit the changes
    conn.commit()

    print("Database has been made")

    return conn

