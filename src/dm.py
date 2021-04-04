import re
from src.database import data
from src.utils import get_user_id_from_token

'''
Direct Messages
'''

def makedmName(u_ids):

    handle_list = []
    for user in data["accData"]:
        if user["id"] in u_ids:
            handle_list.append(user["handle"])
    sortedHandle = sorted(handle_list)
    return ",".join(sortedHandle)
   

def dm_create_v1(token, u_ids):
    
    #Obtain user id of creator from token
    auth_user_id = get_user_id_from_token(token)

    # Set dm_id to length of dmlist in database
    total_ids = [auth_user_id]
    total_ids.extend(u_ids)

    dm_id = len(data["dmList"])

    # Make dm name as alphabetically sorted list of handles
    dm_name = makedmName(total_ids)

    dmData = {
        'dm_name': dm_name,
        'id': dm_id,
        'messages': [],
        'member_ids': [total_ids],
        'owner_ids': [auth_user_id],
    }

    # Adding user data and database
    data["dmList"].append(dmData)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }


'''
def dm_list_v1(token):




def dm_invite_v1(token, dm_id, u_id):
'''

