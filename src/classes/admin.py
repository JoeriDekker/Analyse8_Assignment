# A system administrator is a person who can maintain the system and perform some administration tasks on the application. 
# They are IT technical people and not intended to work with the members. 
# However, for security reasons, they should be able to perform all the functions of consultants, if needed. 
# The minimum required functions of an administrator are listed below:

# FUNCTIONS TO DO:

# ● To update their own password.

# ● To check the list of users and their roles.

# ● To define and add a new consultant to the system.

# ● To modify or update an existing consultant’s account and profile.

# ● To delete an existing consultant’s account.

# ● To reset an existing consultant’s password (a temporary password).

# ● To make a backup of the system and restore a backup (members information and users’ data).

# ● To see the logs file(s) of the system.

# ● To add a new member to the system.

# ● To modify or update the information of a member in the system.

# ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).

# ● To search and retrieve the information of a member.

from consultant import Consultant

class Admin(Consultant):
    def __init__(self, username, level):
        super().__init__(username, level)

    def check_users(self):
        pass

    def add_consultant(self):
        pass

    def update_consultant(self):
        pass

    def delete_consultant(self):
        pass

    def reset_consultant_password(self):
        pass

    def backup_system(self):
        pass

    def restore_backup(self):
        pass

    def see_logs(self):
        pass

    def delete_member(self):
        pass