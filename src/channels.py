import re
import src.database as database
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.error import InputError, AccessError
from src.utils import get_user_id_from_token

'''
channels_list_v2 takes in a token, converted to auth_user_id.
If the user_id is valid, the function then returns all the channels associated
with the user_id in a list.
Arguments:
    token (string) - ID of user
Exceptions:
    AccessError - Occurs when given id does not match accData
Return Value:
    Returns list | {'channels': newchannelList}
'''
def channels_list_v2(token):
    auth_user_id = get_user_id_from_token(token)

    newchannelList = []
    for channel in database.data["channelList"]:
        if auth_user_id in channel.get('member_ids'):
                channelDict = {}
                channelDict['channel_id'] = channel.get('id')
                channelDict['name'] = channel.get('name')
                newchannelList.append(channelDict)

    return {'channels': newchannelList}

'''
channels_listall_v2 takes in a token string converted to auth_user_id.
If the user_id is valid, the function then returns all channels.
Arguments:
    token (string) - ID of user
Exceptions:
    AccessError - Occurs when given id does not match accData
Return Value:
    Returns list | {'channels': newchannelList}
'''
def channels_listall_v2(token):
    _ = get_user_id_from_token(token)

    newchannelList = []
    for channel in database.data["channelList"]:
        channelDict = {}
        channelDict['channel_id'] = channel.get('id')
        channelDict['name'] = channel.get('name')
        newchannelList.append(channelDict)

    return {'channels': newchannelList}

'''
channels_create_v2 takes in token (converted to auth_user_id), a specified channel name, and a boolean for 
whether or not the channel is intended to be public. This function creates an empty channel dictionary 
and appends the user id as an owner and member of the channel, then returns the newly created
channel id.

Arguments:
    token (string) - User's Authorisation Hash
    name (string) - Name of the channel
    is_public (boolean) - Either true or false, sets the channel to public or private

Exceptions:
    InputError - Occurs when length of name is greater than 20 characters
    InputError - Occurs when length of name is less than 1 character (not listed on spec but added anyways)
    AccessError - Occurs when token is invalid

Return Value:
    Returns channel_id | 'channel_id': channel_id,

'''

def channels_create_v2(token, name, is_public):
    auth_user_id = get_user_id_from_token(token)

    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    # Check if length of name is valid
    if len(name) > 20:
        raise InputError(description="Error: Name is greater than 20 characters")

    if len(name) < 1:
        raise InputError(description="Error: Name is less than 1 character")
  
    channel_id = len(database.data["channelList"])

    channelData = {
        'name': name,
        'id': channel_id,
        'is_public': is_public,
        'member_ids': [],
        'owner_ids': [],
        'messages': [],
    }

    # Adding user data
    channelData['owner_ids'].append(auth_user_id)
    channelData['member_ids'].append(auth_user_id)
    database.data["channelList"].append(channelData)

    return {
        'channel_id': channel_id,
    }
