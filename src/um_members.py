# ==========[CREATED BY]============
# STUDENT 1
# NAME: Joeri Dekker
# STUDENT NUMBER:

# STUDENT 2
# NAME: Alysha van Etten
# STUDENT NUMBER: 

# STUDENT 3
# NAME: Kim leeters
# STUDENT NUMBER:
# ===================================

from db.db_connection import ConnectToDB
import classes.user as u

conn = ConnectToDB()

u = u.User("Jo", "123")

print("This is a very epic python project biatches")
print(u)