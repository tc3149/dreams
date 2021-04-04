import re
from src.database import data
from src.error import InputError, AccessError
from src.utils import get_user_id_from_token, make_dm_name, valid_dmid

'''
Direct Messages
'''
def dm_create_v1(token, u_ids):
    
    #Obtain user id of creator from token
    auth_user_id = get_user_id_from_token(token)

    # Set dm_id to length of dmlist in database
    total_ids = [auth_user_id]
    total_ids.extend(u_ids)

    dm_id = len(data["dmList"])

    # Make dm name as alphabetically sorted list of handles
    dm_name = make_dm_name(total_ids)

    dmData = {
        'dm_name': dm_name,
        'id': dm_id,
        'messages': [],
        'member_ids': total_ids,
        'owner_ids': [auth_user_id],
    }

    # Adding user data and database
    data["dmList"].append(dmData)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }



def dm_list_v1(token):
    auth_user_id = get_user_id_from_token(token)

    newdmList = []

    for dm in data["dmList"]:
        if auth_user_id in dm.get('member_ids'):
            dmDict = {}
            dmDict['dm_id'] = dm.get('id')
            dmDict['dm_name'] = dm.get('dm_name')
            newdmList.append(dmDict)
    
    return {'dms': newdmList}



'''
def dm_invite_v1(token, dm_id, u_id):
'''

#def dm_messages_v1(token, dm_id, start):

def dm_leave_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError
    # Main Implemenation
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            for users in dm["member_ids"]:
                if auth_user_id is users:
                    dm["member_ids"].remove(auth_user_id)

def dm_remove_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError

    # User is not DM creator and main Implementation
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            if auth_user_id not in dm["owner_ids"]:
                raise AccessError
            else:
                data["dmList"].remove(dm)