import datetime
import random

class IdFunc:
    def generate_membership_id():
      # Get the current year
      current_year = datetime.datetime.now().year

      # Get first two digits of the current year
      first_two_digits = str(current_year)[2:]

      # Create 7 random digits
      random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])

      # Calculate the checksum for last digit
      checksum = sum(int(digit) for digit in first_two_digits + random_digits) % 10

      # Return the membership ID
      finalnumber = first_two_digits + random_digits + str(checksum)

      if is_valid_membership_id(finalnumber):
            return finalnumber
      else:
            print("Error: Invalid membership ID generated")
            return None
      

def is_valid_membership_id(id):
    # Check if the length is correct
    if len(id) != 10:
        return False

    # Check if the first two digits are less than or equal to the current year
    if int(id[:2]) > int(str(datetime.datetime.now().year)[2:]):
        return False

    # Calculate the checksum
    checksum = sum(int(digit) for digit in id[:9]) % 10

    # Check if the checksum is correct
    if checksum != int(id[9]):
        return False

    return True
