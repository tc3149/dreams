import re
import jwt
from src.database import accData, secretSauce
from src.error import InputError


'''
auth_login_v1 takes in an email string and password string. 
The function then checks if the email is valid, if a user exists for that email and if the password is correct.
Returns the user id associated with that email if above conditions are met, otherwise raises an InputError

Arguments:
    email (string)    - Email of user
    password (string)    - Password of user
    ...

Exceptions:
    InputError  - Occurs when given email does not match regex
    InputError  - Occurs when given email is not registered
    InputError  - Occurs when given password does not exist or match

Return Value:
    Returns user id | 'auth_user_id': get_user_id(email)
'''
def auth_login_v1(email, password):

    # Check if email is valid
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        # Email is valid
        # Check if user exists for that email
        if search_email(email):
            # User exists, now check if password is correct
            if verify_password(email, password):
                # Create JWT
                secret = jwt.encode({'auth_user_id': get_user_id(email),}, secretSauce, algorithm="HS256")
                # Password is correct, return JWT & user_id
                return {
                    "token": secret,
                    "auth_user_id": get_user_id(email),
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


'''
auth_register_v1 takes in an email string, password string, first name string and last name string. 
The function then checks if the names are within length, password is wwithin lengh and email is a valid email
according to the regex.
If all conditions are met, the function will create a handle for the user, assign a id and append accData list 
with a dictionary of the users information (first name, last name, email, password, id, handle).
Returns the user id that is associated the the new user if above conditions are met, otherwise raises an InputError

Arguments:
    email (string)    - Email of user
    password (string)    - Password of user
    name_first (string)    - First name of user
    name_last (string)    - Last name of user
    ...

Exceptions:
    InputError  - Occurs when given email does not match regex
    InputError  - Occurs when given length of first name is < 1 or > 50
    InputError  - Occurs when given length of last name is < 1 or > 50
    InputError  - Occurs when given length of password < 6
    InputError  - Occurs when given email is already registered

Return Value:
    Returns user id | 'auth_user_id': userID
'''
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
            userHandle = create_handle(name_first, name_last)
            # Check if handle is over 20 characters
            if len(userHandle) > 20:
                # Truncate string if over 20 characters
                userHandle = userHandle[0:20]
            # Check if userHandle already exists
            if search_handle(userHandle):
                # Same handle exists, appending latest handle according to spec
                userHandle = append_handle(userHandle)
            userID = len(accData)
            userData = {
                "name_first": name_first,
                "name_last": name_last,
                "email": email,
                "password": password,
                "id": userID,
                "handle": userHandle, 
            }
            accData.append(userData)
    else:
        # Error
        raise InputError("Error: Email is not valid")

    # Create JWT
    secret = jwt.encode({'auth_user_id': userID}, secretSauce, algorithm="HS256")
    # Return JWT string and the user id
    return {
        "token": secret,
        "auth_user_id": userID,
    }

# Helper functions
def search_email(email):
    for items in accData:
        if items["email"] == email:
            return True
    return False

def verify_password(email, password):
    for items in accData:
        if items["email"] == email:
            if items["password"] == password:
                return True
            else:
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
