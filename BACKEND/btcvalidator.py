import re
 
# Function to validate
# BITCOIN Address
def isValidBTCAddress(str):
 
    # Regex to check valid BITCOIN Address
    regex = "^(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,34}$"
 
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False