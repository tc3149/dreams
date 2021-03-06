import re
from src.database import accData, channelList
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):

    #Check if user is authorised to be in the channel
    authorisation = False
    for channel in channelList:
        if channel["id"] is channel_id:
            for user in channel["member_ids"]:
                if user is auth_user_id:
                    authorisation = True
                    break
    if authorisation is False:
        raise AccessError("User is not in channel")

    # Check if user id is valid
    if valid_userid is False:
        raise AccessError("Error: Invalid user id")

    # Check if channel id is valid
    if valid_channelid is False:
        raise AccessError("Error: Invalid channel")

    # Return Function
    for channel in channelList:
        if channel["id"] is channel_id:
            messages = channel["messages"]

    if start > len(messages):
        raise InputError("Start is greater than total number of messages")

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
        # TO-do/fix once iteration 2 is released
        msg = {
            'message_id': messages[starting_index]["message_id"], 
            'u_id': messages[starting_index]["u_id"],
            'message': messages[starting_index]["message"],
            'time_created': messages[starting_index]["time_created"],
        }
        messages_shown.append(msg)
        msg_amt = msg_amt + 1
    if len(messages) is 0 or counter < 50:
        end = -1
    return {
        'messages': messages_shown,
        'start': start,
        'end': end,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    # check whether id is valid
    if check_id(auth_user_id).get('status'):
        raise error.InputError("User ID invalid")

    # check whether channel is invalid
    channel_id_status = False
    for channel in database.channelList
        if channel.get("id") is channel_id:
            channel_id_status = True
            break
    if channel_id_status is False:
        raise AccessError("Error: Invalid channel")

    iduser = check_id(auth_user_id).get("u_id")

    channels = data['channelList']

    for channel1 in channels:
        if channel_id is channel1['channel_id']:
            if channel1['is public']:
                if iduser not in channel1['all_members']:
                    channel1['all_members'].append(iduser)

                else:
                    raise AccessError("User already in channel")

            else:
                raise AccessError("Private Channel")

    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# Helper Functions

def valid_userid(auth_user_id):
    # Check if user id is valid
    for user in accData:
        if user.get("id") is auth_user_id:
            return True
    return False

def valid_channelid(channel_id):
    # Check if channel id is valid
    for channel in channelList:
        if channel.get("id") is channel_id:
            return True
    return False
