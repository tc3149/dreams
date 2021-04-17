import re
import random
import string
import jwt
import string
import random
import src.database as database
from flask import request
from src.utils import is_valid_token_return_data, check_reset_code, find_reset_email
import src.config as config
from src.error import InputError, AccessError
from hashlib import sha256
from json import loads
from flask import Flask, current_app
from flask_mail import Mail, Message



'''
auth_login_v2 takes in an email and password. 
The function then checks if the email is valid, if a user exists for that email and if the password is correct.
Returns the session id and user id if above conditions are met, otherwise raises an InputError

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

def auth_login_v2(email, password):
    hashedPass = sha256(password.encode()).hexdigest()
    # Check if email is valid
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        # Email is valid
        # Check if user exists for that email
        if search_email(email):
            # User exists, now check if password is correct
            if verify_password(email, hashedPass):
                # Create JWT
                newSessionId = new_session_id()
                sessionToken = create_session_token(newSessionId)
                email_search_append_sessiontoken(email, newSessionId)
                # Password is correct, return JWT & user_id
                return {
                    "token": sessionToken,
                    "auth_user_id": get_user_id(email),
                }
            else:
                # Password not found
                raise InputError(description="Wrong password")
        else:
            # User does not exist
            raise InputError(description="A registered user does not exist with given email")
    else:
        # Email is not valid
        raise InputError(description="Email given is not a valid email")


'''
auth_register_v2 takes in an email string, password string, first name string and last name string. 
The function then checks if the names are within length, password is wwithin lengh and email is a valid email
according to the regex.
If all conditions are met, the function will create a session id, handle for the user, hash the password, assign a id 
and append accData list with a dictionary of the users information (first name, last name, email, password, id, handle).
Also creates a profile for that user and appends it to a profileList
Returns the token that is associated the the new user if above conditions are met, otherwise raises an InputError

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
    Returns token | 'auth_user_id': userID
'''
def auth_register_v2(email, password, name_first, name_last):
    # Checking length of input variables | Error checking for inputs
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError(description="Error: First and/or last name is less than 1 character")

    if len(password) < 6:
        # Error
        raise InputError(description="Error: Password is less than 6 characters")

    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError(description="Error: First and/or last name is more than 50 characters")
    
    # Check if email is valid
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        # Valid 
        if search_email(email):
            # Error, email already exists in database
            raise InputError(description="Error: Email already registered")
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
            userID = database.idData["userId"]
            database.idData["userId"] += 1
            userData = {
                "name_first": name_first,
                "name_last": name_last,
                "email": email,
                "password": sha256(password.encode()).hexdigest(),
                "id": userID,
                "handle": userHandle, 
                "sessions": [],
                "permission": (1 if userID == 0 else 2),
                "notifications": [],
            }
            newSessionId = new_session_id()
            sessionToken = create_session_token(newSessionId)
            userData["sessions"].append(newSessionId)
            database.data["accData"].append(userData)

            # Create profile
            userProfile = {
                "u_id": userID,
                "email": email,
                "name_first": name_first,
                "name_last": name_last,
                "handle_str": userHandle,
                "profile_img_url": f"{config.url}static/default.jpg",
            }
            database.data["userProfiles"].append(userProfile)
    else:
        # Error
        raise InputError(description="Error: Email is not valid")

    # Return JWT string and the user id
    return {
        "token": sessionToken,
        "auth_user_id": userID,
    }

'''
Arguments:
    token (string)    - jwt encrypted session id



Exceptions:
    AccessError - Occurs when session does not exist
    AccessError - Occurs when token is invalid value
    AccessError - Occurs when token is invalid data type

Return Value:
    Returns token | 'auth_user_id': userID
'''
def auth_logout_v1(token):
    sessionId = is_valid_token_return_data(token)
    for user in database.data["accData"]:
        for session in user["sessions"]:
            if session == sessionId["sessionId"]:
                user["sessions"].remove(sessionId["sessionId"])
                return {
                    "is_success": True,
                }
    raise AccessError(description="Session doesn't exist")

'''
auth_passwordreset_request_v1 takes in an email.
The function then checks if the email is valid and if a user exists for that email.
The function then creates a reset code that is emailed to the user's email if the email is valid.
Returns an empty dictionary, otherwise raises an InputError.

Arguments:
    email (string)    - Email of user

Exceptions:
    InputError  - Occurs when given email is not registered

Return Value:
    Returns {}
'''
def auth_passwordreset_request_v1(email):
    # Creating the resetData 
    resetData = {
        "reset_code": None,
        "email": email
    }
    # Creating a randomized 5 character code
    reset_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for characters in range(5))
    # Appending the Data
    for user in database.data["accData"]:
        if user["email"] == email:
            resetData["reset_code"] = reset_code
            database.data["resetdataList"].append(resetData)
        else:
            raise InputError(description="Email doesn't exist")
    # Setting mail contents and sending
    msg = Message('Your reset code for Dream Server',
                recipients = [email]
               )
    msg.body = "Hello,\nThis is your reset code: {}".format(reset_code)
    return msg
'''
auth_passwordreset_request_v1 takes in an email.
The function then checks if the email is valid and if a user exists for that email.
The function then creates a reset code that is emailed to the user's email if the email is valid.
Returns an empty dictionary, otherwise raises an InputError.

Arguments:
    email (string)    - Email of user

Exceptions:
    InputError  - Occurs when given email is not registered

Return Value:
    Returns {}
'''
def auth_passwordreset_reset_v1(reset_code, new_password):
    #Checking length of password
    if len(new_password) < 6:
        raise InputError(description="Password needs to be at least 6 characters")
    #Checking validity of code
    if check_reset_code(reset_code) is False:
        raise InputError(description="Code is invalid")
    #Retrieving the email of user
    reset_email = find_reset_email(reset_code)
    #Assigning the new password
    for user in database.data["accData"]:
        if user["email"] == reset_email:
            user["password"] = new_password
    #Removing the token
    for resetData in database.data["resetdataList"]:
        if resetData["reset_code"] == reset_code:
            del resetData
            return {}

# util functions
def search_email(email):
    for items in database.data["accData"]:
        if items["email"] == email:
            return True
    return False

def verify_password(email, password):
    for items in database.data["accData"]:
        if items["email"] == email:
            if items["password"] == password:
                return True
            else:
                return False

def search_handle(currUserHandle):
    for items in database.data["accData"]:
        if items["handle"] == currUserHandle:
            return True
    return False

def get_user_id(email):
    for items in database.data["accData"]:
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

def new_session_id():
    database.idData["sessionId"] = database.idData["sessionId"] + 1
    return database.idData["sessionId"]


def create_session_token(sessionId):
    sessionToken = jwt.encode({"sessionId": sessionId}, database.secretSauce, algorithm="HS256")
    return sessionToken

def email_search_append_sessiontoken(email, sessionId):
    for items in database.data["accData"]:
        if items["email"] == email:
            items["sessions"].append(sessionId)
