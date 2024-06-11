# Consultants are employees of the Unique Meal who are in direct contact with the members. 
# They process the requests of the members. Hence, they need to be able to manage the member’s information and data. 
# For this purpose, when a new client requests for membership, a consultant needs to register the client's information in the system. 
# So, the minimum required functions of a consultant in the system are summarized as below:

# FUNCTIONS TO DO:

import uuid
from classes.menu import Menu
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.log_functions import LogFunc
from functions.hash_functions import HashFunctions
import functions.login as Login


from db.db_connection import ConnectToDB

class Consultant:
    def __init__(self, username, level):
        self.username = username
        self.level = level
        self.logged_in = True
        self.menu_options = ["Update password", "Add member", "Update member", "Search member"]
        self.menu_functions = [self.update_password, self.add_member, self.update_member, self.search_member]
        self.menu = Menu(
            options=self.menu_options + ["Logout"],
            functions=self.menu_functions + [self.logout]
        )

    # ● To update their own password
    def update_password(self):
        
        # Connect to the database and fetch the hashed password for the current user
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM users WHERE username=?", (self.username,))
        result = c.fetchone()
        c.close()

        if not result:
            print("User not found in the database.")
            return
        
        print("Enter your old password: ")
        old_password = Login.get_masked_password()
        hashed_password = result[5]

        if not HashFunctions.check_password(old_password, hashed_password):
            print("Old password does not match. Password update failed.")
            return
        
        # Get the new password
        print("- must have a length of at least 12 characters\n- must be no longer than 30 characters\n- must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character")
        print("New password: ")
        new_password = Login.get_masked_password()
        if not Checks.password_check():
            print("Invalid password")

        # Hash the new password
        hashed_password = HashFunctions.hash_password(new_password)

        print("Updating password...")

        # Update the password in the database
        c = ConnectToDB()
        c.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, self.username))
        c.commit()
        c.close()

        print("Password updated successfully!")

    # ● To add a new member to the system
    def add_member(self):
        cities = [
        "New York", "Tokyo", "Paris", "London", "Sydney",
        "Dubai", "Moscow", "Rio de Janeiro", "Mumbai", "Cape Town"
        ]

        print("Enter the info of the new Member:")

        member_id = IdFunc.generate_membership_id()
        first_name = input("First name: ")
        if not Checks.string_check(first_name):
            print("name too long, try again.")
            return
        
        last_name = input("Last name: ")
        if not Checks.string_check(last_name):
            print("name too long, try again.")
            return

        age = input("Age: ")
        if not Checks.number_check(age):
            print("not a number, try again.")
            return
        
        
        gender = input("What is the Gender: \nM = Male\nF = Female\nO = Other\nN = Prefer not to say\n W = Who knows\nChoice: ")
        if not Checks.gender_check(gender):
            print("Wrong gender input, try again.")
            return
        weight = input("Weight: ")
        if not Checks.number_check(weight):
            print("not a number, try again.")
            return

        street = input("Street name: ")
        if not Checks.string_check(street):
            print("street too long, try again.")
            return
        house_number = input("House number: ")
        if not Checks.number_check(house_number):
            print("not a number, try again.")
            return
        zip_code = input("Zip code: ")
        if not Checks.zip_code_check(zip_code):
            print("zip code in wrong format, try again.")
            return
        
        for index, city in enumerate(cities, start=1):
            print(f"{index}. {city}")
        city_input = input("City: ")
        city_number = Checks.city_check(city_input, cities)
        if city_number == -1:
            print("no valid number, try again.")
            return
        city = cities[city_number - 1]

        email = input("Email: ")
        if not Checks.email_check(email):
            print("email in wrong format, try again.")
            return
        phone_number = input("Phone number: ")
        if not Checks.phone_number_check(phone_number):
            print("phone number in wrong format, try again.")
            return

        print("Now adding Member...")

        c = ConnectToDB()
        c.execute("INSERT INTO members (id, first_name, last_name, age, gender, weight, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(member_id), first_name, last_name, age, gender, weight, email, phone_number))
        c.execute("INSERT INTO address (id, member_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), member_id, street, house_number, zip_code, city))
        c.commit()
        c.close()

        print("Adding Member successful!")
        LogFunc.append_to_file(f"{self.username}", "Member added", f"{self.username} addeded member named: {first_name} {last_name}", "no")
        input("Press Enter to Continue")

    # ● To modify or update the information of a member in the system
    def update_member(self):
        cities = [
        "New York", "Tokyo", "Paris", "London", "Sydney",
        "Dubai", "Moscow", "Rio de Janeiro", "Mumbai", "Cape Town"
        ]
                
        last_name_input = input("Enter the last name of the member you want to update: ")
        if not Checks.string_check(last_name_input):
            print("invalid input, try again.")
            return

        # Check if the member exists
        query = """
        SELECT * FROM members
        WHERE last_name=?
        """
        c = ConnectToDB().cursor()
        c.execute(query, (last_name_input,))
        members = c.fetchall()
        if members:
            member = members[0]
        else:
            print("no member found with the provided search input. try again")
            return

        query = """
        SELECT * FROM address
        WHERE member_id=?
        """
        c.execute(query, (member[0],))
        address = c.fetchall()[0]
        c.close()

        if not address:
            print("Address not found with the provided ID.")
            return

        # Display member's current information
        print("Current Member Information:")
        print("ID:", member[0])
        print("First Name:", member[1])
        print("Last Name:", member[2])
        print("Age:", member[3])
        print("Gender:", member[4])
        print("Weight:", member[5])

        print("Street name:", address[2])
        print("House number:", address[3])
        print("Zip code:", address[4])
        print("City:", address[5])


        print("Email:", member[6])
        print("Phone Number:", member[7])

        # Ask for updated information
        print("\nEnter the updated information (leave blank if not updating):")

        updated_first_name = input("First name: ").strip()
        if updated_first_name:
            if not Checks.string_check(updated_first_name):
                print("name too long, try again.")
                return
        updated_last_name = input("Last name: ").strip()
        if updated_last_name:
            if not Checks.string_check(updated_last_name):
                print("name too long, try again.")
                return
        updated_age = input("Age: ").strip()
        if updated_age:
            if not Checks.number_check(updated_age):
                print("not a number, try again.")
                return
        updated_gender = input("Gender: ").strip()
        if updated_gender:
            if not Checks.gender_check(updated_gender):
                print("gender too long, try again.")
                return
        updated_weight = input("Weight: ").strip()
        if updated_weight:
            if not Checks.number_check(updated_weight):
                print("not a number, try again.")
                return

        updated_street = input("Street name: ").strip()
        if updated_street:
            if not Checks.string_check(updated_street):
                print("street too long, try again.")
                return
        updated_house_number = input("House number: ").strip()
        if updated_house_number:
            if not Checks.number_check(updated_house_number):
                print("not a number, try again.")
                return
        updated_zip_code = input("Zip code: ").strip()
        if updated_zip_code:
            if not Checks.zip_code_check(updated_zip_code):
                print("zip code in wrong format, try again.")
                return
        for index, city in enumerate(cities, start=1):
            print(f"{index}. {city}")
        city_input = input("City: ").strip()
        if city_input:
            city_number = Checks.city_check(city_input, cities)
            if city_number == -1:
                print("no valid number, try again.")
                return
            updated_city = cities[city_number - 1]
        else:
            updated_city = None

        updated_email = input("Email: ").strip()
        if updated_email:
            if not Checks.email_check(updated_email):
                print("email in wrong format, try again.")
                return
        updated_phone_number = input("Phone number: ").strip()
        if updated_phone_number:
            if not Checks.phone_number_check(updated_phone_number):
                print("phone number in wrong format, try again.")
                return

        print("Updating member info...")

        # Update member's information in the database
        c = ConnectToDB()
        if updated_first_name:
            c.execute("UPDATE members SET first_name=? WHERE last_name=?", (updated_first_name, last_name_input))
        if updated_last_name:
            c.execute("UPDATE members SET last_name=? WHERE last_name=?", (updated_last_name, last_name_input))
        if updated_age:
            c.execute("UPDATE members SET age=? WHERE last_name=?", (updated_age, last_name_input))
        if updated_gender:
            c.execute("UPDATE members SET gender=? WHERE last_name=?", (updated_gender, last_name_input))
        if updated_weight:
            c.execute("UPDATE members SET weight=? WHERE last_name=?", (updated_weight, last_name_input))
        if updated_email:
            c.execute("UPDATE members SET email=? WHERE last_name=?", (updated_email, last_name_input))
        if updated_phone_number:
            c.execute("UPDATE members SET phone_number=? WHERE last_name=?", (updated_phone_number, last_name_input))

        if updated_street:
            c.execute("UPDATE address SET street=? WHERE member_id=?", (updated_street, member[0]))
        if updated_house_number:
            c.execute("UPDATE address SET house_number=? WHERE member_id=?", (updated_house_number, member[0]))
        if updated_zip_code:
            c.execute("UPDATE address SET zip_code=? WHERE member_id=?", (updated_zip_code, member[0]))
        if updated_city:
            c.execute("UPDATE address SET city=? WHERE member_id=?", (updated_city, member[0]))

        c.commit()
        c.close()

        print("Member information updated successfully!")
        input("Press Enter to Continue")

    # ● To search and retrieve the information of a member.
    def search_member(self):
        search_input = input("Search: ")
        if not Checks.string_check(search_input):
            print("input too long, try again.")
            return
    
        search_term = f"%{search_input}%"
        query = """
        SELECT * FROM members
        WHERE id LIKE ? OR
              first_name LIKE ? OR
              last_name LIKE ? OR
              age LIKE ? OR
              gender LIKE ? OR
              weight LIKE ? OR
              email LIKE ? OR
              phone_number LIKE ?
        """

        c = ConnectToDB().cursor()
        c.execute(query, (search_term, search_term, search_term, search_term, search_term, search_term, search_term, search_term))
        results = c.fetchall()
        c.close()
        
        if results:
            for row in results:
                print(row)
        else:
            print("no member found with the provided search input. try again")

    def display_menu(self):
        self.menu.display()
        self.menu.execute_choice()

    def logout(self):
        print("Logging out...")
        self.logged_in = False
