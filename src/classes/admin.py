# A system administrator is a person who can maintain the system and perform some administration tasks on the application. 
# They are IT technical people and not intended to work with the members. 
# However, for security reasons, they should be able to perform all the functions of consultants, if needed. 
# The minimum required functions of an administrator are listed below:

# FUNCTIONS TO DO:

# (inherited from consultant)

    # ● To update their own password.

    # ● To add a new member to the system.

    # ● To modify or update the information of a member in the system.

    # ● To search and retrieve the information of a member.

from classes.menu import Menu
from classes.consultant import Consultant

class Admin(Consultant):
    def __init__(self, username, level):
        super().__init__(username, level)
        admin_options = [
            "Check users", "Add consultant", "Update consultant", "Delete consultant",
            "Reset consultant password", "Backup system", "Restore backup",
            "See logs", "Delete member"
        ]
        admin_functions = [
            self.check_users, self.add_consultant, self.update_consultant, self.delete_consultant,
            self.reset_consultant_password, self.backup_system, self.restore_backup,
            self.see_logs, self.delete_member
        ]
        self.menu_options += admin_options
        self.menu_functions += admin_functions
        self.menu = Menu(options=self.menu_options, functions=self.menu_functions)
        
    # ● To check the list of users and their roles. (member to admin??)
    def check_users(self):
        pass
    
    # ● To define and add a new consultant to the system.
    def add_consultant(self):
        pass

    # ● To modify or update an existing consultant’s account and profile.
    def update_consultant(self):
        pass

    # ● To delete an existing consultant’s account.
    def delete_consultant(self):
        pass

    # ● To reset an existing consultant’s password (a temporary password).
    def reset_consultant_password(self):
        pass

    # ● To make a backup of the system... 
    def backup_system(self):
        pass

    # ...and restore a backup (members information and users’ data).
    def restore_backup(self):
        pass

    # ● To see the logs file(s) of the system.
    def see_logs(self):
        pass

    # ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).
    def delete_member(self):
        pass