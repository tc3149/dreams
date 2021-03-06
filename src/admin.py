import re
from src.error import InputError, AccessError
import src.database as database
from src.utils import get_user_id_from_token, make_dm_name, valid_userid, valid_dmid



'''
Arguments:
    token (string)      - jwt encrypted session id
    u_id (int)          - user id

Exceptions:
    InputError - Occurs when u_id is not a valid user
    InputError - Occurs when user is currently the only owner
    AccessError - Occurs when auth user is not owner

Return Value:
    {}  - empty dictionary
'''
def admin_user_remove_v1(token, u_id):
    #get auth_user_id 
    auth_user_id = get_user_id_from_token(token)

    #auth_user_id not an owner
    for user in database.data["accData"]:
        if user["id"] == auth_user_id:
            permission_id = user["permission"]
    if permission_id != 1:
        raise AccessError(description="User is not an owner")

    #user does not exist
    if not valid_userid(u_id):
        # user_id does not exist
        raise InputError ("User does not exist")
    
    #if user is only owner and is trying to remove themselves
    if auth_user_id == u_id:
        ownerCount = 0
        for mem in database.data['accData']:
            if mem['permission'] == 1:
                ownerCount += 1 
        
        if ownerCount == 1:
            raise InputError(description='User is currently the only owner of Dreams')
    
    # Change all user message contents to "Remove User" in channel
    for channel in database.data['channelList']:
        for messages in channel['messages']:
            if messages['u_id'] == u_id:
                messages['message'] = "Removed User"

    # Change all user message contents to "Remove User" in DM
    for dms in database.data["dmList"]:
        for messages in dms["messages"]:
            if messages["u_id"] == u_id:
                messages["message"] = "Removed User"
    

    # Change profile name to Removed User
    for user in database.data['userProfiles']:
        if user['u_id'] == u_id:
            user['name_first'] = 'Removed'
            user['name_last'] = 'User'
    # Remove account data
    for user in database.data['accData']:
        if user['id'] == u_id:
            database.data['accData'].remove(user)

    return{}

'''
Arguments:
    token (string)         - jwt encrypted session id
    u_id (int)             - user id 
    permission_id (int)    - permission status to set user id to

Exceptions:
    InputError - Occurs when u_id is not a valid user
    InputError - Occurs when permissioin is is not a valid permission
    AccessError - Occurs when auth_user is not owner
Return Value:
    {}  - empty dictionary
'''
def admin_userpermission_change_v1(token, u_id, permission_id):
    #get auth_user_id
    auth_user_id = get_user_id_from_token(token)

    #auth_user_id not an owner
    for user in database.data["accData"]:
        if user["id"] == auth_user_id:
            auth_permission_id = user["permission"]
    if auth_permission_id != 1:
        raise AccessError(description='User is not an owner')

    #user does not exist
    if not valid_userid(u_id):
        # user_id does not exist
        raise InputError(description="User does not exist")
    
    #if user is only owner and is trying to change their permission while being the only owner
    if auth_user_id == u_id:
        ownerCount = 0
        for mem in database.data['accData']:
            if mem["permission"] == 1:
                ownerCount += 1
        
        if ownerCount == 1:
            raise InputError(description='User is currently the only owner of Dreams')

    #permission_id is valid
    if permission_id == 1 or permission_id == 2:
        #replace value of key permission_id
        for user in database.data["accData"]:
            if user["id"] == u_id:
                user["permission"] = permission_id
    else:
        raise InputError(description='permission_id does not refer to a value permission')

    return{}


    


