from src.error import InputError, AccessError
from src.database import data
from src.utils import get_user_id_from_token
from json import loads
import re

def user_profile_v2(token, u_id):
    _ = get_user_id_from_token(token)

    if searchUser(u_id) == True:
        return {
            'user': {
                'u_id': u_id,
                'email': data["accData"][u_id]["email"],
                'name_first': data["accData"][u_id]["name_first"],
                'name_last': data["accData"][u_id]["name_last"],
                'handle_str': data["accData"][u_id]["handle"],
            },
        }
    else:
        raise InputError("User not found")

def user_profile_setname_v2(token, name_first, name_last):
    userId = get_user_id_from_token(token)
    
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError("Error: First and/or last name is less than 1 character")
    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError("Error: First and/or last name is more than 50 characters")
    data["accData"][userId]["name_first"] = name_first
    data["accData"][userId]["name_last"] = name_last

    return {}


def user_profile_setemail_v2(token, email):
    userId = get_user_id_from_token(token)

    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        if not search_email(email):
            data["accData"][userId]["email"] = email
        else:
            raise InputError("Email already in use")
    else:
        raise InputError("Email entered is not a valid email")
    
    return {}


def user_profile_sethandle_v1(token, handle_str):
    userId = get_user_id_from_token(token)

    if len(handle_str) > 20:
        raise InputError("Handle is not allowed to be longer than 20 characters")
    if len(handle_str) < 3:
        raise InputError("Handle is not allowed to be shorter than 3 characters")

    if not search_handle(handle_str):
        data["accData"][userId]["handle"] = handle_str
    else:
        raise InputError("Handle is taken by another user")

    return {}

def users_all_v1(token):
    _ = get_user_id_from_token(token)

    usersList = []
    for items in range(len(data["accData"])):
        userData = {
            'u_id': data["accData"][items]["id"],
            'email': data["accData"][items]["email"],
            'name_first': data["accData"][items]["name_first"],
            'name_last': data["accData"][items]["name_last"],
            'handle_str': data["accData"][items]["handle"],
        }
        usersList.append(userData)
    
    return usersList

# Helpers
def searchUser(user):
    for items in data["accData"]:
        if items["id"] == user:
            return True
    return False

def search_email(email):
    for items in data["accData"]:
        if items["email"] == email:
            return True
    return False

def search_handle(currUserHandle):
    for items in data["accData"]:
        if items["handle"] == currUserHandle:
            return True
    return False