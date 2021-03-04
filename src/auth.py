import re
from src.database import memberSize, accData
from src.error import InputError

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):

    # Checking length of input variables | Error checking for inputs
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError("Error: First and/or last name is less than 1 character")

    if len(password) < 6:
        # Error
        raise InputError("Error: Password is less than 6 characters")

    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError("Error: First and/or last name is more than 50 characters")
    
    # Check if email is valid
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        # Valid 
        if search_email(email):
            # Error, email already exists in database
            raise InputError("Error: Email already registered")
        else:
            # Valid input, generate handle & register user by inputing given details into database
            global memberSize
            userHandle = create_handle(name_first, name_last)
            # Check if handle is over 20 characters
            if len(userHandle) > 20:
                # Truncate string if over 20 characters
                userHandle = userHandle[0:20]
            # Check if userHandle already exists
            if search_handle(userHandle):
                # Same handle exists, appending latest handle according to spec
                userHandle = append_handle(userHandle)
            userData = {
                "name_first": name_first,
                "name_last": name_last,
                "email": email,
                "password": password,
                "id": memberSize,
                "handle": userHandle, 
            }
            accData.append(userData)
            memberSize += 1
    else:
        # Error
        raise InputError("Error: Email is not valid")

    return {
        'auth_user_id': memberSize,
    }

def search_email(email):
    for items in accData:
        if items["email"] == email:
            return True
    return False

def search_handle(currUserHandle):
    for items in accData:
        if items["handle"] == currUserHandle:
            return True
    return False

def append_handle(currUserHandle):
    # Check number of users with same handle
    availableNumber = 0
    while True:
        testModCurrUserHandle = currUserHandle + str(availableNumber)
        if search_handle(testModCurrUserHandle):
            # Handle isnt avaiable, increment availableNumber
            availableNumber += 1
        else:
            # Handle is available, return number
            return testModCurrUserHandle

def create_handle(first, last):
    createUserHandle = first + last
    createUserHandle = createUserHandle.lower()
    createUserHandle = createUserHandle.replace("@", "")
    return createUserHandle
