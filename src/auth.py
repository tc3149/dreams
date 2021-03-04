import re
from src.database import memberSize, accData
from src.error import InputError

def auth_login_v1(email, password):

    # Check if email is valid
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        # Email is valid
        # Check if user exists for that email
        if search_email(email):
            # User exists, now check if password is correct
            if search_password(password):
                # Password exists, return user_id
                return {
                    'auth_user_id': get_user_id(email),
                }
            else:
                # Password not found
                raise InputError("Wrong password")
        else:
            # User does not exist
            raise InputError("A registered user does not exist with given email")
    else:
        # Email is not valid
        raise InputError("Email given is not a valid email")


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
            userID = memberSize
            memberSize += 1
    else:
        # Error
        raise InputError("Error: Email is not valid")

    return {
        'auth_user_id': userID,
    }

def search_email(email):
    for items in accData:
        if items["email"] == email:
            return True
    return False

def search_password(password):
    for items in accData:
        if items["password"] == password:
            return True
    return False

def search_handle(currUserHandle):
    for items in accData:
        if items["handle"] == currUserHandle:
            return True
    return False

def get_user_id(email):
    for items in accData:
        if items["email"] == email:
            userID = items["id"]
            return userID

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
