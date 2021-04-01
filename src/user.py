from src.error import InputError, AccessError
from src.database import accData
import re


def user_profile_v1(auth_user_id, u_id):
    if (searchUser(u_id)):
        return {
            'user': {
                'u_id': u_id,
                'email': accData[u_id]["email"],
                'name_first': accData[u_id]["name_first"],
                'name_last': accData[u_id]["name_last"],
                'handle_str': accData[u_id]["handle"],
            },
        }
    else:
        raise InputError("User not found")

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError("Error: First and/or last name is less than 1 character")
    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError("Error: First and/or last name is more than 50 characters")
    accData[auth_user_id]["name_first"] = name_first
    accData[auth_user_id]["name_last"] = name_last


def user_profile_setemail_v1(auth_user_id, email):
    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        if not search_email(email):
            accData[auth_user_id]["email"] = email
        else:
            raise InputError("Email already in use")
    else:
        raise InputError("Email entered is not a valid email")


def user_profile_sethandle_v1(auth_user_id, handle_str):
    if len(handle_str) > 20:
        raise InputError("Handle is not allowed to be longer than 20 characters")
    if len(handle_str) < 3:
        raise InputError("Handle is not allowed to be shorter than 3 characters")

    if not search_handle(handle_str):
        accData[auth_user_id]["handle"] = handle_str
    else:
        raise InputError("Handle is taken by another user")

def users_all_v1(auth_user_id):
    if not searchUser(auth_user_id):
        raise AccessError("Invalid token")

    usersList = []
    for items in range(len(accData)):
        userData = {
            'u_id': accData[items]["id"],
            'email': accData[items]["email"],
            'name_first': accData[items]["name_first"],
            'name_last': accData[items]["name_last"],
            'handle_str': accData[items]["handle"],
        }
        usersList.append(userData)
    
    return usersList

# Helpers
def searchUser(user):
    for items in accData:
        if items["id"] == user:
            return True
    return False

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