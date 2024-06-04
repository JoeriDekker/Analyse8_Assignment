import re



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

def zip_code_check(zip_code):
    if re.fullmatch(r'^\d{4}[A-Z]{2}$', zip_code):
        return True
    return False

def phone_number_check(phone_number):
    if re.fullmatch(r'^\d{8}$', phone_number):
        return True
    return False

# print(zip_code_check("1234AB"))
# print(zip_code_check("A2342B"))
# print(zip_code_check("1234A"))
# print(zip_code_check("1234ABC"))


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
