import bcrypt

class HashFunctions:
    def hash_password(plain_password):
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password
        hashed_password = bcrypt.hashpw(plain_password.encode(), salt)
        return hashed_password

    # Function to check a password against a hashed password
    def check_password(plain_password, hashed_password):
        plain_password = plain_password.encode('utf-8')
        return bcrypt.checkpw(plain_password, hashed_password)