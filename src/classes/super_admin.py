# Super administrator is simply the owner or the manager of the association. 
# The manager needs a super admin password through which can define a system administrator. 
# Although the main function of the super admin is to define system admin(s), and leave the system to them; however, 
# they should be able to perform all possible functionalities of the lower-level users (i.e., system admin and consultant).

# In this assignment, to make it easier for your teacher to test and assess your work, 
# a super admin must be hard coded with username: super_admin, password: Admin_123?

# § Note that we know this is not a good development practice in terms of the quality and security of the system, 
# but this is only to enable your teacher to easily test your system using this predefined hardcoded username and password.

# The minimum required functions of a super administrator are listed below:

# FUNCTIONS TO DO:

# (inherited from consultant)

# ● To add a new member to the system.

# ● To modify or update the information of a member in the system.

# ● To search and retrieve the information of a member.

# (inherited from admin)

# ● To check the list of users and their roles.

# ● To define and add a new consultant to the system.

# ● To modify or update an existing consultant’s account and profile.

# ● To delete an existing consultant account.

# ● To reset an existing consultant password (a temporary password).

# ● To make a backup of the system and restore a backup (members information and users’ data).

# ● To see the logs file of the system.

# ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).

from admin import Admin

class SuperAdmin(Admin):
    def __init__(self, username, level):
        super().__init__(username, level)

    # ● To define and add a new admin to the system.
    def add_admin(self):
        pass

    # ● To modify or update an existing admin’s account and profile.
    def update_admin(self):
        pass

    # ● To delete an existing admin’s account.
    def delete_admin(self):
        pass

    # ● To reset an existing admin’s password (a temporary password).
    def reset_admin_password(self):
        pass