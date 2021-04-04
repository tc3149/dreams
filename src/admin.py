import re
from src.error import InputError, AccessError
from src.database import data
from src.utils import get_user_id_from_token, make_dm_name, valid_userid, valid_dmid,

def admin_user_remove_v1(token,u_id):
    #get auth_user_id 
    auth_user_id = get_user_id_from_token(token)

    #check if auth_user_id is member 
    auth_id_status = valid_userid(auth_user_id)
    #if not a member
    if auth_id_satus == False:
        # auth_user_id does not exist
        raise InputError ("User does not exist")

    #check if u_id is exists 
    user_id_satus = valid_userid(u_id)
    #user does not exist
    if user_id_satus == False:
        # user_id does not exist
        raise InputError ("User does not exist")
    
    #if user is only owner and is trying to remove themselves
    if auth_user_id == u_id:
        ownerCount = 1
        for mem in data['accData']['permission_id']
            if permission_id == 1
                ownerCount ++ 
        
        if ownerCount == 1:
            raise InputError ('User is currently the only owner of Dreams')
    
    #auth_user_id not an owner
    permission_id = data['accData']['permission_id']
    if permission_id not 1:
        raise AccessError("User is not an owner")

    #remove u_id from database 
    for user in data['message_ids']['']
    data['accData']['removed user'] = data['accData']['u_id']
    del data['accData']['u_id']


    return{}


def admin_userpermission_change_v1(token,u_id,permission_id):
    #get auth_user_id
    auth_user_id = get_user_id_from_token(token)
    
    #check if auth_user_id is member 
    auth_id_status = valid_userid(auth_user_id)
    #if not a member
    if auth_id_satus == False:
        # auth_user_id does not exist
        raise InputError ("User does not exist")

    #check if u_id is exists 
    user_id_satus = valid_userid(u_id)
    #user does not exist
    if user_id_satus == False:
        # user_id does not exist
        raise InputError ("User does not exist")
    
    #if user is only owner and is trying to remove themselves
    if auth_user_id == u_id:
        ownerCount = 1
        for mem in data['accData']['permission_id']
            if permission_id == 1
                ownerCount +=
        
        if ownerCount == 1:
            raise InputError ('User is currently the only owner of Dreams')
    
    #auth_user_id not an owner
    permission_id = data['accData']['permission_id']
    if permission_id not 1:
        raise AccessError("User is not an owner")

    #permission_id is not valid
    if permission_id is 1 or permission_id is 2:
        #replace value of key permission_id
        data['accData'][u_id]['permission_id'] = permission_id

    else:
        raise InputError('permission_id does not refer to a value permission')

    return{}


    


