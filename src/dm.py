import re
import src.database as database
from src.utils import get_user_id_from_token, make_dm_name, valid_dmid, valid_userid
from src.error import InputError, AccessError

'''
Direct Messages
'''

def dm_create_v1(token, u_ids):
    
    #Obtain user id of creator from token
    auth_user_id = get_user_id_from_token(token)

    # Check if u_ids are valid
    for u_id in u_ids:
        if valid_userid(u_id) is False:
            raise InputError(description="User ID does not exist")

    # Set dm_id to length of dmlist in database
    total_ids = [auth_user_id]
    total_ids.extend(u_ids)



    # Make dm name as alphabetically sorted list of handles
    dm_name = make_dm_name(total_ids)
    dm_id = database.idData["dmId"]

    dmData = {
        'dm_name': dm_name,
        'id': dm_id,
        'messages': [],
        'member_ids': total_ids,
        'owner_ids': [auth_user_id],
    }
    database.idData["dmId"] = database.idData["dmId"] + 1
    # Adding user data and database
    database.data["dmList"].append(dmData)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }

def dm_list_v1(token):
    auth_user_id = get_user_id_from_token(token)

    newdmList = []

    for dm in database.data["dmList"]:
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
    for dm in database.data["dmList"]:
        if dm_id is dm["id"]:
            # Dm exists
            dmExists = True
            break
    if dmExists is False:
        # Dm doesnt exist
        raise InputError(description="DM does not exist")

    # Check if u_id refers to a valid user
    if valid_userid(u_id) is False:
        raise InputError(description="User ID does not exist")

    # Check if the inviter is part of the dm
    authorised = False
    for dm in database.data["dmList"]:
        if dm.get("id") is dm_id:
            if auth_user_id in dm.get("member_ids"):
                authorised = True
                break
    if authorised is False:
        raise AccessError(description="User is not a part of the DM to be able to invite")

    # Security measures complete
    # assumption they will not be in the dm already?
    # Add user id into the list of member ids
    for dm in database.data["dmList"]:
        if dm.get("id") is dm_id:
            dm["member_ids"].append(u_id)

    return {}


'''
dm_messages_v1 takes in a user id, a specific dm id, and a 'start' to
determine after what amount of messages to show, e.g. recent 5 messages have 
already been seen, thus start would equal 5 to see later messages.
The function first does security checks, then reverses the messages list, so
that the most recent messages are at the head of the list, then appends to a new
list for return.

Arguments:
    token (string) - Unique user id created by auth_register_v2
    channel_id (integer) - Unique channel id created by channels_create_v2
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    AccessError - Occurs when token is not valid (i.e. not created)

Return Value:
    Most cases Returns:
        'messages': messages_shown,
        'start': start,
        'end': end,
    If there are less than 50 messages in the list, or no 'later' messages
    returns: 
        'messages': messages_shown,
        'start': start,
        'end': -1,

'''

def dm_messages_v1(token, dm_id, start):

    auth_user_id = get_user_id_from_token(token)

    # Check if user id is valid
    if valid_userid(auth_user_id) is False:
        raise AccessError(description="Error: Invalid user id")

    # Check if dm id is valid
    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: Invalid dm")

    #Check if user is authorised to be in the dm
    authorisation = False
    for dm in database.data["dmList"]:
        if dm["id"] is dm_id:
            for user in dm["member_ids"]:
                if user is auth_user_id:
                    authorisation = True
                    break
    if authorisation is False:
        raise AccessError(description="User is not in dm")



    # Return Function
    for dm in database.data["dmList"]:
        if dm["id"] is dm_id:
            messages = dm["messages"].copy()

    if start > len(messages):
        raise InputError(description="Start is greater than total number of messages")

    # 0th index is the most recent message... therefore must reverse list?
    messages.reverse()
    
    # start + 50 messages is what is shown, so must create a list with these
    # messages within and transfer data from messages to messages_shown
    messages_shown = []
    end = start + 50
    msg_amt = 0
    while msg_amt < 50:
        # Where we start and increment from
        starting_index = start + msg_amt
        if starting_index >= end or starting_index >= len(messages):
            break

        messages_shown.append(messages[starting_index])
        msg_amt = msg_amt + 1
    if len(messages) == 0 or msg_amt < 50:
        end = -1
    return {
        'messages': messages_shown,
        'start': start,
        'end': end,
    }

'''
dm_leave_v1 takes in a token and a specific dm id.
The first segment checks for inputError when a invalid dm_id is added.
After that segment is passed, the next segment checks if the user is in the channel
and if the user is present, the user is removed from the list of member ids in channel database.
Otherwise, if the user is not present, an AccessError is raised.

Arguments:
    token (string) - Unique user id created by auth_register_v2
    channel_id (integer) - Unique channel id created by channels_create_v2
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    InputError - dm_id is invalid
    AccessError - Occurs when token is not valid (i.e. not created)

Return Value:
    Most cases Returns:
        '{}'

'''


def dm_leave_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError
    # Main Implemenation
    for dm in database.data["dmList"]:
        if dm_id is dm["id"]:
            for users in dm["member_ids"]:
                if auth_user_id is users:
                    dm["member_ids"].remove(auth_user_id)
                    return {}
    raise AccessError(description="Invalid")
                    
'''
dm_remove_v1 takes in a token and a specific dm id.
The first segment checks for inputError when a invalid dm_id is added.
After that segment is passed, the next segment checks if the user the creator
and if the user is the creator, the dm is removed from the list of dm_ids in dmList database.
Otherwise, if the user is not the creator, an AccessError is raised.

Arguments:
    token (string) - Unique user id created by auth_register_v2
    channel_id (integer) - Unique channel id created by channels_create_v2
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    InputError - dm_id is invalid
    AccessError - Occurs when token is not valid (i.e. not created)

Return Value:
    Most cases Returns:
        '{}'

'''

def dm_remove_v1(token, dm_id):

    auth_user_id = get_user_id_from_token(token)

    # Invalid dm_id
    if valid_dmid(dm_id) is False:
        raise InputError

    # User is not DM creator and main Implementation
    for dm in database.data["dmList"]:
        if dm_id is dm["id"]:
            if auth_user_id not in dm["owner_ids"]:
                raise AccessError(description="User not the creator of DM")
            else:
                database.data["dmList"].remove(dm)
                return {}
