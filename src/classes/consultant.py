import uuid
from classes.menu import Menu
from functions.input_checks import Checks
from functions.id_functions import IdFunc
from functions.log_functions import LogFunc
from functions.hash_functions import HashFunctions
import functions.login as Login
from functions.encrypt_functions import EncryptFunc


# Consultants are employees of the Unique Meal who are in direct contact with the members. 
# They process the requests of the members. Hence, they need to be able to manage the member’s information and data. 
# For this purpose, when a new client requests for membership, a consultant needs to register the client's information in the system. 
# So, the minimum required functions of a consultant in the system are summarized as below:

# FUNCTIONS TO DO:
    # ● To update their own password (complete)
    # ● To add a new member to the system (complete)
    # ● To modify or update the information of a member in the system (complete)
    # ● To search and retrieve the information of a member (complete)


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


    cities = [
    "New York", "Tokyo", "Paris", "London", "Sydney",
    "Dubai", "Moscow", "Rio de Janeiro", "Mumbai", "Cape Town"
    ]


    def update_password(self):
    
        # gets all users
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM users")
        results = c.fetchall()
        c.close()

        user_info = None
        
        # searches user by username
        if not results:
            print("User not found in the database.")
            return
        else:
            for result in results:
                if EncryptFunc.decrypt_value(result[3]) == self.username:
                    user_info = result
                    break

        if user_info == None:
            print("User not found between users")
            return

        # checks old password
        print("Enter your old password: ")
        old_password = Login.get_masked_password()
        hashed_password = user_info[5]
        if not HashFunctions.check_password(old_password, hashed_password):
            print("Old password does not match. Password update failed.")
            return
        
        # gets the new password
        print("- must have a length of at least 12 characters\n- must be no longer than 30 characters\n- must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character")
        print("New password: ")
        new_password = Login.get_masked_password()
        if not Checks.password_check(new_password):
            print("Invalid password")
            LogFunc.append_to_file(f"{self.username}", "Tried changing password", f"{self.username} tried to change their own password, but failed", "no")

        # hashes the new password
        hashed_password = HashFunctions.hash_value(new_password)

        print("Updating password...")

        # updates the password in the database
        c = ConnectToDB()
        c.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, user_info[3]))
        c.commit()
        c.close()

        print("Password updated successfully!")
        LogFunc.append_to_file(f"{self.username}", "Changed password", f"{self.username} changed their own password", "no")
        input("Press Enter to Continue")


    def add_member(self):

        # asks member info and address
        print("Enter the info of the new Member:")

        member_id = IdFunc.generate_membership_id()

        first_name = input("First name: ")
        if not Checks.string_check(first_name):
            print("first name too long or empty, try again.")
            return
        
        last_name = input("Last name: ")
        if not Checks.string_check(last_name):
            print("last name too long or empty, try again.")
            return
        
        age = input("Age: ")
        if not Checks.number_check(age):
            print("not a number, try again.")
            return
        
        gender = input("What is the Gender: \nM = Male\nF = Female\nO = Other\nN = Prefer not to say\nW = Who knows\nChoice: ")
        if not Checks.gender_check(gender):
            print("Wrong gender input, try again.")
            return
        
        weight = input("Weight: ")
        if not Checks.number_check(weight):
            print("not a number, try again.")
            return

        street = input("Street name: ")
        if not Checks.string_check(street):
            print("street too long or empty, try again.")
            return
        
        house_number = input("House number: ")
        if not Checks.number_check(house_number):
            print("not a number, try again.")
            return
        
        zip_code = input("Zip code: ")
        if not Checks.zip_code_check(zip_code):
            print("zip code in wrong format, try again.")
            return
        
        for index, city in enumerate(self.cities, start=1):
            print(f"{index}. {city}")
        city_input = input("City: ")
        city_number = Checks.city_check(city_input, self.cities)
        if city_number == -1:
            print("no valid number, try again.")
            return
        city = self.cities[city_number - 1]

        email = input("Email: ")
        if not Checks.email_check(email):
            print("email in wrong format, try again.")
            return
        
        phone_number = input("Phone number: ")
        if not Checks.phone_number_check(phone_number):
            print("phone number in wrong format, try again.")
            return

        print("Now adding Member...")

        # encrypts all given data and adds to database
        encrypted_first_name = EncryptFunc.encrypt_value(first_name)
        encrypted_last_name = EncryptFunc.encrypt_value(last_name)
        encrypted_age = EncryptFunc.encrypt_int_value(age)
        encrypted_gender = EncryptFunc.encrypt_value(gender)
        encrypted_weight = EncryptFunc.encrypt_int_value(weight)
        encrypted_email = EncryptFunc.encrypt_value(email)
        encrypted_phone_number = EncryptFunc.encrypt_value(phone_number)

        encrypted_street = EncryptFunc.encrypt_value(street)
        encrypted_house_number = EncryptFunc.encrypt_int_value(house_number)
        encrypted_zip_code = EncryptFunc.encrypt_value(zip_code)
        encrypted_city = EncryptFunc.encrypt_value(city)
        
        c = ConnectToDB()
        c.execute("INSERT INTO members (id, first_name, last_name, age, gender, weight, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(member_id), encrypted_first_name, encrypted_last_name, encrypted_age, encrypted_gender, encrypted_weight, encrypted_email, encrypted_phone_number))
        c.execute("INSERT INTO address (id, member_id, street, house_number, zip_code, city) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), member_id, encrypted_street, encrypted_house_number, encrypted_zip_code, encrypted_city))
        c.commit()
        c.close()

        print("Adding Member successful!")
        LogFunc.append_to_file(f"{self.username}", "Member added", f"{self.username} added member named: {first_name} {last_name}", "no")
        input("Press Enter to Continue")


    def update_member(self):

        # asks member last name  
        last_name_input = input("Enter the last name of the member you want to update: ")
        if not Checks.string_check(last_name_input):
            print("invalid input, try again.")
            return

        # gets all members
        c = ConnectToDB().cursor()
        c.execute("SELECT * FROM members")
        results = c.fetchall()
        c.close()

        member_info = None
        
        # searches member by last name
        if not results:
            print("Member not found in the database.")
            return
        else:
            for result in results:
                if EncryptFunc.decrypt_value(result[2]) == last_name_input:
                    member_info = result
                    break

        if member_info == None:
            print("Member not found between members")
            return

        # gets the matching address
        query = """
        SELECT * FROM address
        WHERE member_id=?
        """
        c = ConnectToDB().cursor()
        c.execute(query, (member_info[0],))
        address = c.fetchone()
        c.close()

        if not address:
            print("Address not found with the provided ID.")
            return

        # displays member info
        print("Current Member Information:")
        print("ID:", member_info[0])
        print("First Name:", EncryptFunc.decrypt_value(member_info[1]))
        print("Last Name:", EncryptFunc.decrypt_value(member_info[2]))
        print("Age:", EncryptFunc.decrypt_value(member_info[3]))
        print("Gender:", EncryptFunc.decrypt_value(member_info[4]))
        print("Weight:", EncryptFunc.decrypt_value(member_info[5]))

        print("Street name:", EncryptFunc.decrypt_value(address[2]))
        print("House number:", EncryptFunc.decrypt_value(address[3]))
        print("Zip code:", EncryptFunc.decrypt_value(address[4]))
        print("City:", EncryptFunc.decrypt_value(address[5]))

        print("Email:", EncryptFunc.decrypt_value(member_info[6]))
        print("Phone Number:", EncryptFunc.decrypt_value(member_info[7]))
        print(f"Register Date: {member_info[8]}")


        # asks for updated information
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
                print("Wrong gender input, try again.")
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
            
        for index, city in enumerate(self.cities, start=1):
            print(f"{index}. {city}")
        city_input = input("City: ").strip()
        if city_input:
            city_number = Checks.city_check(city_input, self.cities)
            if city_number == -1:
                print("no valid number, try again.")
                return
            updated_city = self.cities[city_number - 1]
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

        # updates member info in database
        c = ConnectToDB()
        if updated_first_name:
            encrypted_first_name = EncryptFunc.encrypt_value(updated_first_name)
            c.execute("UPDATE members SET first_name=? WHERE last_name=?", (encrypted_first_name, member_info[2]))
        if updated_last_name:
            encrypted_last_name = EncryptFunc.encrypt_value(updated_last_name)
            c.execute("UPDATE members SET last_name=? WHERE last_name=?", (encrypted_last_name, member_info[2]))
        if updated_age:
            encrypted_age = EncryptFunc.encrypt_int_value(updated_age)
            c.execute("UPDATE members SET age=? WHERE last_name=?", (encrypted_age, member_info[2]))
        if updated_gender:
            encrypted_gender = EncryptFunc.encrypt_value(updated_gender)
            c.execute("UPDATE members SET gender=? WHERE last_name=?", (encrypted_gender, member_info[2]))
        if updated_weight:
            encrypted_weight = EncryptFunc.encrypt_int_value(updated_weight)
            c.execute("UPDATE members SET weight=? WHERE last_name=?", (encrypted_weight, member_info[2]))
        if updated_email:
            encrypted_email = EncryptFunc.encrypt_value(updated_email)
            c.execute("UPDATE members SET email=? WHERE last_name=?", (encrypted_email, member_info[2]))
        if updated_phone_number:
            encrypted_phone_number = EncryptFunc.encrypt_value(updated_phone_number)
            c.execute("UPDATE members SET phone_number=? WHERE last_name=?", (encrypted_phone_number, member_info[2]))

        # updates address info of member in database
        if updated_street:
            encrypted_street = EncryptFunc.encrypt_value(updated_street)
            c.execute("UPDATE address SET street=? WHERE member_id=?", (encrypted_street, member_info[0]))
        if updated_house_number:
            encrypted_house_number = EncryptFunc.encrypt_int_value(updated_house_number)
            c.execute("UPDATE address SET house_number=? WHERE member_id=?", (encrypted_house_number, member_info[0]))
        if updated_zip_code:
            encrypted_zip_code = EncryptFunc.encrypt_value(updated_zip_code)
            c.execute("UPDATE address SET zip_code=? WHERE member_id=?", (encrypted_zip_code, member_info[0]))
        if updated_city:
            encrypted_city = EncryptFunc.encrypt_value(updated_city)
            c.execute("UPDATE address SET city=? WHERE member_id=?", (encrypted_city, member_info[0]))

        c.commit()
        c.close()

        print("Member information updated successfully!")
        LogFunc.append_to_file(f"{self.username}", "Member updated", f"{self.username} updated member with Id: {member_info[0]}", "no")
        input("Press Enter to Continue")


    def search_member(self):

        # asks for search input
        search_input = input("Search: ")
        if not Checks.string_check(search_input):
            print("input too long or empty, try again.")
            return

        # gets all members from database
        query = "SELECT * FROM members"
        c = ConnectToDB().cursor()
        c.execute(query)
        members = c.fetchall()
        c.close()

        # sees if there are any members that match the search on any of the fields
        found_members = []
        for member in members:
            for value in member[1:-1]:
                if search_input in str(EncryptFunc.decrypt_value(value)):
                    found_members.append(member)
                    break

        # loops thru the found members if there are any
        if found_members:
            for member in found_members:

                # gets the matching address
                query = """
                SELECT * FROM address
                WHERE member_id=?
                """
                c = ConnectToDB().cursor()
                c.execute(query, (member[0],))
                address = c.fetchone()
                c.close()

                if not address:
                    print("Address not found with the provided ID.")
                    return
                
                # prints all found members that matched the search 
                print(f"ID: {member[0]}")
                print(f"First Name: {EncryptFunc.decrypt_value(member[1])}")
                print(f"Last Name: {EncryptFunc.decrypt_value(member[2])}")
                print(f"Age: {EncryptFunc.decrypt_value(member[3])}")
                print(f"Gender: {EncryptFunc.decrypt_value(member[4])}")
                print(f"Weight: {EncryptFunc.decrypt_value(member[5])}")

                print("Street name:", EncryptFunc.decrypt_value(address[2]))
                print("House number:", EncryptFunc.decrypt_value(address[3]))
                print("Zip code:", EncryptFunc.decrypt_value(address[4]))
                print("City:", EncryptFunc.decrypt_value(address[5]))

                print(f"Email: {EncryptFunc.decrypt_value(member[6])}")
                print(f"Phone Number: {EncryptFunc.decrypt_value(member[7])}")
                print(f"Register Date: {member[8]}\n")
        else:
            print("no member found with the provided search input. try again")

    def display_menu(self):
        self.menu.display()
        self.menu.execute_choice()

    def logout(self):
        print("Logging out...")
        self.logged_in = False
