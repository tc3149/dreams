from src.error import InputError, AccessError
import src.database as database
from src.utils import get_user_id_from_token, search_email
from src.utils import search_handle, search_user
from json import loads
import re

'''
Arguments:
    token (string)         - jwt encrypted session id
    u_id (int)             - user id

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type

Return Value:
    Dictionary of this format = {
        'u_id': u_id,                                                      - user id (int)
        'email': database.data["userProfiles"][u_id]["email"],             - user email (string)
        'name_first': database.data["userProfiles"][u_id]["name_first"],   - user first name (string)
        'name_last': database.data["userProfiles"][u_id]["name_last"],     - user last name (string)
        'handle_str': database.data["userProfiles"][u_id]["handle_str"],   - user handle (string)
    }
'''
def user_profile_v2(token, u_id):
    _ = get_user_id_from_token(token)

    for user in database.data["userProfiles"]:
        if user["u_id"] == u_id:
            return user


'''
Arguments:
    token (string)      - jwt encrypted session id
    name_first (string) - new first name to set to
    name_last (string)  - new last name to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type

Return Value:
    {}  - empty dictionary
'''
def user_profile_setname_v2(token, name_first, name_last):
    userId = get_user_id_from_token(token)
    
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError("Error: First and/or last name is less than 1 character")
    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError("Error: First and/or last name is more than 50 characters")
    
    for user in database.data["accData"]:
        if user["id"] == userId:
            user["name_first"] = name_first
            user["name_last"] = name_last
    for user in database.data["userProfiles"]:
        if user["u_id"] == userId:
            user["name_first"] = name_first
            user["name_last"] = name_last

    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id
    email (string)      - new email string to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type
    InputError  - Email already in use by someone else
    InputError  - Invalid email regex

Return Value:
    {}  - empty dictionary
'''
def user_profile_setemail_v2(token, email):
    userId = get_user_id_from_token(token)

    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        if not search_email(email):
            for user in database.data["accData"]:
                if user["id"] == userId:
                    user["email"] = email
            for user in database.data["userProfiles"]:
                if user["u_id"] == userId:
                    user["email"] = email
        else:
            raise InputError("Email already in use")
    else:
        raise InputError("Email entered is not a valid email")
    
    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id
    handle_str (string) - new handle name to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type
    InputError  - Handle is taken by someone else
    InputError  - New handle is not within the given constraints

Return Value:
    {}  - empty dictionary
'''
def user_profile_sethandle_v1(token, handle_str):
    userId = get_user_id_from_token(token)

    if len(handle_str) > 20:
        raise InputError("Handle is not allowed to be longer than 20 characters")
    if len(handle_str) < 3:
        raise InputError("Handle is not allowed to be shorter than 3 characters")

    if not search_handle(handle_str):
        for user in database.data["accData"]:
            if user["id"] == userId:
                user["handle"] = handle_str
        for user in database.data["userProfiles"]:
            if user["u_id"] == userId:
                user["handle_str"] = handle_str
    else:
        raise InputError("Handle is taken by another user")

    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type

Return Value:
    List of dictionarys of the following format = {
        'u_id': u_id,                                                      - user id (int)
        'email': database.data["userProfiles"][u_id]["email"],             - user email (string)
        'name_first': database.data["userProfiles"][u_id]["name_first"],   - user first name (string)
        'name_last': database.data["userProfiles"][u_id]["name_last"],     - user last name (string)
        'handle_str': database.data["userProfiles"][u_id]["handle_str"],   - user handle (string)
    }
'''
def users_all_v1(token):
    _ = get_user_id_from_token(token)
    
    return database.data["userProfiles"] 