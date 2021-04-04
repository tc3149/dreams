import re
from src.error import InputError, AccessError
from src.database import data
from src.utils import get_user_id_from_token, make_dm_name, valid_userid

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


def dm_invite_v1(token, dm_id, u_id):
    # Obtain user id from token
    #
    auth_user_id = get_user_id_from_token(token)

    # Check if dm_id exists
    dmExists = False
    for dm in data["dmList"]:
        if dm_id is dm["id"]:
            # Dm exists
            dmExists = True
            break
    if dmExists is False:
        # Dm doesnt exist
        raise InputError("DM does not exist")

    # Check if u_id refers to a valid user
    if valid_userid(u_id) is False:
        raise InputError("User ID does not exist")

    # Check if the inviter is part of the dm
    authorised = False
    for dm in data["dmList"]:
        if dm.get("id") is dm_id:
            if auth_user_id in dm.get("member_ids"):
                authorised = True
                break
    if authorised is False:
        raise AccessError("User is not a part of the DM to be able to invite")

    # Security measures complete
    # assumption they will not be in the dm already?
    # Add user id into the list of member ids
    for dm in data["dmList"]:
        if dm.get("id") is dm_id:
            dm["member_ids"].append(u_id)

    return {}
