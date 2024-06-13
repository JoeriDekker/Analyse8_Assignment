import re

from db.db_connection import ConnectToDB
from functions.encrypt_functions import EncryptFunc

class Checks:
  
    def password_check(password):
        if len(password) >= 12 and len(password) <= 30:
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
                if username == username_input:
                    print("username already in use, try again")
                    return False
        return True
        
    def name_check(name):
        if len(name) >= 1 and len(name) <= 50:
            # check if name is only letters 
            if re.fullmatch(r'^[a-zA-Z]+$', name):
                return True
                
        return False

    def zip_code_check(zip_code):
        if re.fullmatch(r'^\d{4}[A-Z]{2}$', zip_code):
            return True
        return False

    def phone_number_check(phone_number):
        if re.fullmatch(r'^\d{8}$', phone_number):
            return True
        return False
    
    def number_check(input):
        if len(input) >= 50:
                return False
        try:
            float(input) 
            return True
        except ValueError:
            return False
        
    def id_check(input):
        if len(input) != 10:
            return False
        try:
            float(input) 
            return True
        except ValueError:
            return False
    
    def string_check(input):
        if len(input) <= 50 and len(input) > 0:
            return True
        else:
            return False
        
    def email_check(email):
        if re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return True
        return False
    
    def city_check(input, cities):
        choice = int(input)
        if 1 <= choice <= len(cities):
            return choice
        else:
            return -1
        
    def gender_check(input):
        if input == "M" or input == "F" or input == "O" or input == "N" or input == "W":
            return True
        return False

    # print(zip_code_check("1234AB"))
    # print(zip_code_check("A2342B"))
    # print(zip_code_check("1234A"))
    # print(zip_code_check("1234ABC"))

    # print (phone_number_check("12345678"))
    # print (phone_number_check("1345678"))
    # print (phone_number_check("123456789292"))
    # print (phone_number_check("1234awfsg5678"))
    # print (phone_number_check("12c45678"))

    # print(username_check("_hallo12'"))
    # print(username_check("Hallo12_"))
    # print(username_check("2hallo12@"))

    # print("=================")

    # print(password_check("Paswoord1234112232122!")) # True
    # print(password_check("Paswoord1234112232122@")) # True
    # print(password_check("Paswoord1234112232122#")) # True
    # print(password_check("Paswoord1234112232122$")) # True 
    # print(password_check("Paswoord1234112232122%")) # True
    # print(password_check("Paswoord1234112232122&")) # True
    # print(password_check("Paswoord1234112232122(")) # True
    # print(password_check("Paswoord1234112232122)")) # True
    # print(password_check("Paswoord1234112232122_")) # True
    # print(password_check("Paswoord1234112232122+")) # True
    # print(password_check("Paswoord1234112232122=")) # True
    # print(password_check("Paswoord1234112232122[")) # True
    # print(password_check("Paswoord1234112232122]")) # True
    # print(password_check("Paswoord1234112232122{")) # True
    # print(password_check("Paswoord1234112232122}")) # True
    # print(password_check("Paswoord1234112232122;")) # True
    # print(password_check("Paswoord1234112232122:")) # True
    # print(password_check("Paswoord1234112232122'")) # True
    # print(password_check("Paswoord1234112232122`")) # True
    # print(password_check("Paswoord1234112232122~")) # True
    # print(password_check("Paswoord1234112232122.")) # True
    # print(password_check("Paswoord1234112232122,")) # True
    # print(password_check("Paswoord1234112232122>")) # True
    # print(password_check("Paswoord1234112232122<")) # True
    # print(password_check("Paswoord1234112232122/")) # True
    # print(password_check("Paswoord1234112232122?")) # True
    # print(password_check("Paswoord1234112232122|")) # True
    # print(password_check("Paswoord12341122321\we2")) # True

    # password = input("Enter password: ")
    # print(password_check(password))