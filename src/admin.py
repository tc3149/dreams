import re
from src.error import InputError, AccessError
from src.database import data
from src.utils import get_user_id_from_token, make_dm_name, valid_userid, valid_dmid

def admin_user_remove_v1(token,u_id):
    #get auth_user_id 
    auth_user_id = get_user_id_from_token(token)

    #check if auth_user_id is member 
    auth_id_status = valid_userid(auth_user_id)
    #if not a member
    if auth_id_status == False:
        # auth_user_id does not exist
        raise InputError ("User does not exist")

    #check if u_id is exists 
    user_id_status = valid_userid(u_id)
    #user does not exist
    if user_id_status == False:
        # user_id does not exist
        raise InputError ("User does not exist")
    
    #if user is only owner and is trying to remove themselves
    if auth_user_id == u_id:
        ownerCount = 1
        for mem in data['accData']:
            if mem['id']['permission'] == 1:
                ownerCount = ownerCount + 1 
                break
        
        if ownerCount == 1:
            raise InputError ('User is currently the only owner of Dreams')
    
    #auth_user_id not an owner
    permission_id = data['accData'][auth_user_id]['permission']
    if permission_id != 1:
        raise AccessError("User is not an owner")
    
    for channel in data['channelList']:
        for messages in channel['messages']:
            if messages['u_id'] is u_id:
                messages['message'] = "Removed User"
    for user in data['userProfiles']:
        if user['u_id'] is u_id:
            user['name_first'] = 'Removed'
            user['name_last'] = 'User'
    remove_data = []

    for user in data['accData']:
        if user['id'] is u_id:
            data['accData'].remove(user)

    return{}


def admin_userpermission_change_v1(token,u_id,permission_id):
    #get auth_user_id
    auth_user_id = get_user_id_from_token(token)
    
    #check if auth_user_id is member 
    auth_id_status = valid_userid(auth_user_id)
    #if not a member
    if auth_id_status == False:
        # auth_user_id does not exist
        raise InputError ("User does not exist")

    #check if u_id is exists 
    user_id_status = valid_userid(u_id)
    #user does not exist
    if user_id_status == False:
        # user_id does not exist
        raise InputError ("User does not exist")
    
    #if user is only owner and is trying to change their permission while being the only owner
    if auth_user_id == u_id:
        ownerCount = 1
        for mem in data['accData']['permission']:
            if permission_id == 1:
                ownerCount = ownerCount + 1
        
        if ownerCount == 1:
            raise InputError ('User is currently the only owner of Dreams')
    
    #auth_user_id not an owner
    auth_permission_id = data['accData'][auth_user_id]['permission']
    if auth_permission_id != 1:
        raise AccessError('User is not an owner')

    #permission_id is not valid
    if permission_id is 1 or permission_id is 2:
        #replace value of key permission_id
        data['accData'][u_id]['permission'] = permission_id

    else:
        raise InputError('permission_id does not refer to a value permission')

    return{}


    


