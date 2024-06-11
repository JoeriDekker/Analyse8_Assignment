import bcrypt

class HashFunctions:
    def hash_value(plain_value):
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password
        hashed_password = bcrypt.hashpw(plain_value.encode(), salt)
        return hashed_password

    # Function to check a password against a hashed password
    def check_password(plain_value, hashed_password):
        plain_value = plain_value.encode('utf-8')
        return bcrypt.checkpw(plain_value, hashed_password)
    