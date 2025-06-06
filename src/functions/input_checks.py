import re

from db.db_connection import ConnectToDB
from functions.encrypt_functions import EncryptFunc

class Checks:
  
    def password_check(password):
        # Check if password is between 12 and 30 characters
        if len(password) >= 12 and len(password) <= 30:
            # Regular expression to validate password with at least 1 lowercase, upperscase, number and special character
            low_case = re.search(r"[a-z]", password)
            up_case = re.search(r"[A-Z]", password)
            numbers = re.search(r"[0-9]", password)
            special_chars = re.search(r'[~!@#$%&_+=`|\(\)\{\}\[\]:;\'<>,.?/\\-]', password)
            has_all = all((low_case, up_case, numbers, special_chars))
            if has_all:
                return True
        return False

    def username_check(username):
        if len(username) >= 8 and len(username) <= 10:
            # Check if first char is _ or letter
            if username[0] == "_" or username[0].isalpha():
                # Regular expression to validate if username contains available characters
                if re.search(r'[~!@#$%&+=`|\(\)\{\}\[\]:;\<>,?/\\-]', username):
                    return False 
                else:
                    return True
        return False
        
    def username_available_check(username_input):
        # gets all usernames
        c = ConnectToDB().cursor()
        c.execute("SELECT username FROM users")
        usernames = c.fetchall()
        c.close()
        
        # checks if username is already taken
        if usernames:
            for username in usernames:
                if EncryptFunc.decrypt_value(username[0]) == username_input:
                    return False
        return True
        
    def zip_code_check(zip_code):
        # Regular expression to validate zip code 4 numbers and 2 letters
        if re.fullmatch(r'^\d{4}[A-Z]{2}$', zip_code):
            return True
        return False

    def phone_number_check(phone_number):
        # Regular expression to validate phone number 8 numbers
        if re.fullmatch(r'^\d{8}$', phone_number):
            return True
        return False
    
    def number_check(input):
        # Check if length is not higher than 50 and if it is not negative
        if len(input) >= 50:
                return False
        try:
            input = int(input)
            if input < 0:
                return False
            return True
        except ValueError:
            return False
        
    def id_check(input):
        # Check if the length is correct and if it is not negative
        if len(input) != 10:
            return False
        try:
            input = int(input)
            if input < 0:
                return False
            return True
        except ValueError:
            return False
    
    def string_check(input):
        if len(input) >= 1 and len(input) <= 50:
            # Regular expression to validate string
            if re.fullmatch(r'^[a-zA-Z\'-]+$', input):
                return True
                
        return False
        
    def email_check(email):
        # Regular expression for email validation
        if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,3}+$', email):
            return True
        return False
    
    def city_check(input, cities):
        try:
            choice = int(input)
            if 1 <= choice <= len(cities):
                return choice
            else:
                return -1
        except ValueError:
            return -1
        
    def gender_check(input):
        if input == "M" or input == "F" or input == "O" or input == "N" or input == "W":
            return True
        return False


