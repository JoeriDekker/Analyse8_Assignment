class User:
    def __init__(self, username, password):
        self.name = username
        self.password = password

    def __str__(self):
        return f"Username: {self.name}, Password: {self.password}"