import re
from src.error import InputError, AccessError
import src.database as database
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.utils import valid_channelid, valid_userid, check_channelprivate, check_useralreadyinchannel, get_user_id_from_token, checkOwner, inviteNotification, checkDreamowner

'''
channel_invite_v2 takes in a token, a channel_id integer and u_id integer. 
The function then checks if the channel_id is exists, if both users exists, if the token is already a member of the channel and if u_id is a member of the channel.
If all requirements are met the function then adds u_id to the channel and returns {}, otherwise it raises InputError or AccessError.

Arguments:
    token (string)              - User's Authorisation Hash
    channel_id (integer)        - Id of channel
    u_id (integer)              - Id of user being added to the channel   
    ...

Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when given u_id does not exist
    AccessError  - Occurs when given token is invalid
    InputError  - Occurs when given u_id already a member of the channel they are being added to
    ValueError  - Occurs when given auth_user_id is not a member of the channel

Return Value:
    Returns {}
'''

def channel_invite_v2(token, channel_id, u_id):
    auth_user_id = get_user_id_from_token(token)

    #check if channel exists
    channelExists = False
    for channel in database.data["channelList"]:
        if channel_id is channel["id"]:
            #channel does exist
            channelExists = True
            break
    if channelExists is False:
        #channel does not exist
        raise InputError ("Channel does not exist")
       
    #check if auth_user_id owner member of channel
    owner_status = check_useralreadyinchannel(auth_user_id, channel_id)
               
    if owner_status is False:
        #user does not have access
        raise AccessError (description="User does not have access")

    #check if u_id exists
    u_id_status = False
    for user2 in database.data["accData"]:
        if user2.get("id") is u_id:
            #u_id exists
            u_id_status = True
            break
            
    if u_id_status is False:
        # u_id does not exist
        raise InputError ("Invited user does not exist")
    
    #check if u_id already member of the channel
    for user2 in database.data["channelList"][channel_id]['member_ids']:
        if u_id in database.data["channelList"][channel_id]['member_ids']:
            #u_id is member of channel
            raise InputError ("User already a member")    

            
    
    #add u_id to channel
    
    database.data["channelList"][channel_id]['member_ids'].append(u_id)
    inviteNotification(channel_id, -1, u_id, auth_user_id)
    
    return {

    }

'''
channel_details_v2 takes in a token string and a channel_id integer. 
The function then checks if the channel_id is exists, if token (into auth_user_id) exists and is already a member of the channel.
If all requirements are met the function then returns the contents of the channel including the name, ownermembers and all members, otherwise it raises InputError or AccessError.

Arguments:
    token (string)              - User's Authorisation Hash
    channel_id (integer)        - Id of channel 
    ...

Exceptions:
    InputError  - Occurs when given channel_id does not exist
    AccessError  - Occurs when given token does not exist
    ValueError  - Occurs when given auth_user_id is not a member of the channel

Return Value:
    Returns {
        'name': 'testchannel',
        'owner_members': [
            {
                'u_id': 
                'email': 
                'name_first': 
                'name_last': 
                'handle_str':
            }
        ],
        'all_members': [
            {
                'u_id':
                'email': 
                'name_first': 
                'name_last': 
                'handle_str':
                
            }
        ],
    }
'''

def channel_details_v2(token, channel_id):
    auth_user_id = get_user_id_from_token(token)
    #check if channel exists
    channelExists = False
    for channel in database.data["channelList"]:
        if channel_id is channel["id"]:
            #channel does exist
            channelExists = True
            channelName = channel["name"]
            is_public = channel["is_public"]
            break
    if channelExists is False:
        #channel does not exist
        raise InputError ("Channel does not exist")
  
    
    #check if auth_user_id owner member of channel
    member_status = check_useralreadyinchannel(auth_user_id, channel_id)
               
    if member_status is False:
        #user does not have access
        raise AccessError ("User does not have access")
    
    #loop to add member details
    
    allMembers = []
    ownMembers = []
    for memberID in database.data["channelList"][channel_id]['member_ids']:
        for mem in database.data["accData"]:
            if memberID is mem['id']:
                new_member = {
                    'u_id':memberID,
                    'email': database.data["accData"][memberID]['email'],
                    'name_first': database.data["accData"][memberID]['name_first'],
                    'name_last': database.data["accData"][memberID]['name_last'],
                    'handle_str': database.data["accData"][memberID]['handle']
                }
                allMembers.append(new_member)
                break
            
            
    #loop to add owner details
    
    for ownerID in database.data["channelList"][channel_id]['owner_ids']:       
        for own in database.data["accData"]:
            if ownerID is own['id']:
                owner = {
                    'u_id':ownerID,
                    'email': database.data["accData"][ownerID]['email'],
                    'name_first': database.data["accData"][ownerID]['name_first'],
                    'name_last': database.data["accData"][ownerID]['name_last'],
                    'handle_str': database.data["accData"][ownerID]['handle']
                }
                ownMembers.append(owner)
                break
            
            
    
    return {
        'name': channelName,
        'is_public': is_public,
        'owner_members':ownMembers,
        'all_members':allMembers,
    }


'''
channel_messages_v2 takes in a token, a specific channel id, and a 'start' to
determine after what amount of messages to show, e.g. recent 5 messages have 
already been seen, thus start would equal 5 to see later messages.
The function first does security checks, then reverses the messages list, so
that the most recent messages are at the head of the list, then appends to a new
list for return.

Arguments:
    token (string) - User's Authorisation Hash
    channel_id (integer) - Unique channel id created by channels_create_v2
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    AccessError - Occurs when token is not valid

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

def channel_messages_v2(token, channel_id, start):
    auth_user_id = get_user_id_from_token(token)

    # Check if channel id is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel")

    #Check if user is authorised to be in the channel
    authorisation = False
    for channel in database.data["channelList"]:
        if channel["id"] is channel_id:
            for user in channel["member_ids"]:
                if user is auth_user_id:
                    authorisation = True
                    break
    if authorisation is False:
        raise AccessError(description="User is not in channel")

    # Return Function
    for channel in database.data["channelList"]:
        if channel["id"] is channel_id:
            messages = channel["messages"].copy()

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
channel_leave_v1 takes in a token and a specific channel id.
The first segment checks for inputError when a invalid channel_id is added.
After that segment is passed, the next segment checks if the user is in the channel
and if the user is present, the user is removed from the list of member ids in channel database.
Otherwise, if the user is not present, an AccessError is raised.

Arguments:
    token (string) - User's Authorisation Hash
    channel_id (integer) - Unique channel id created by channels_create_v2
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    InputError - channel_id is invalid
    AccessError - Occurs when token is not valid

Return Value:
    Most cases Returns:
        '{}'

'''

def channel_leave_v1(token, channel_id):
    auth_user_id = get_user_id_from_token(token)
    
    #Checking if channel is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Channel ID is not a valid channel")
    #Checking if user is in the channel and removing the user
    id_status = False
    for channel in database.data["channelList"]:
        if channel.get("id") is channel_id:
            for member in channel["member_ids"]:
                if auth_user_id is member:
                    id_status = True
                    channel["member_ids"].remove(member)
    #If the user is invalid
    if id_status is False:
        raise AccessError(description="Error: Authorised user is not a member of channel with channel_id")
    return {
    }

'''
channel_join_v2 takes in the user's token and the channel they wish to join.
The function then checks whether the token is valid, the channel is valid, if the channel is private or if the user is already in the channel.
If so, it appends the user's ID into the channel's 'member ids' and returns nothing. If conditions are breached, it raises an InputError or AccessError

Arguments:
    token (string) - User's Authorisation Hash
    channel_id (string) - Channel's ID

Exceptions:
    AccessError - when the user's token is invalid
    InputError - when the channel ID is invalid
    AccessError - when user tries to join a private channel
    AccessError - when user is already in the channel

Return Value:
    Returns nothing.
'''

def channel_join_v2(token, channel_id):
    auth_user_id = get_user_id_from_token(token)

    # check whether channel is invalid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel")

    # check if channel is private
    if check_channelprivate(channel_id) is True:
        raise AccessError(description="Private Channel")
    
    # check user already in channel
    if check_useralreadyinchannel(auth_user_id, channel_id) is True:
        raise AccessError(description="User already in channel")

    for channel in database.data["channelList"]:
        if channel["id"] is channel_id:
            channel["member_ids"].append(auth_user_id)

    return {
    }


'''
channel_addowner_v1 takes in the token of an authorised user (owner), a channel ID and a user's ID that wishes to be owner of the channel.
The function then checks whether the u_ID is valid, the channel_ID is valid, if the user (u_ID) is in the channel, if the user (u_ID) is in the channel,
or if the token is authorised to do so.
If so, it appends the user's ID into the channel's 'owner_ids' and returns nothing. If conditions are breached, it raises an InputError or AccessError.

Arguments:
    token (string) - User A's Authorisation Hash
    channel_id (int) - Channel's ID
    u_id (int) - User B's ID

Exceptions:
    InputError - when the user's ID is invalid
    InputError - when the channel ID is invalid
    InputError - when the user is already an owner
    AccessError - when the user is not in the channel
    AccessError - when the authorised user is not in channel
    AccessError - when the authorised user is not authorised (not an owner)

Return Value:
    Returns nothing.
'''

def channel_addowner_v1(token, channel_id, u_id):

    auth_user_id = get_user_id_from_token(token)

    DreamOwner = checkDreamowner(auth_user_id)
    
    # If u_id is valid
    if valid_userid(u_id) is False:
        raise InputError(description="Error: Invalid user id")
    
    # If channel_id is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel ID")

    # If u_id is in channel
    if check_useralreadyinchannel(u_id, channel_id) is False:
        raise AccessError(description="Error: Not in channel")

    # If the u_id is already an owner
    if checkOwner(u_id, channel_id) is True:
        raise InputError(description="Error: Already Owner")

    # If the token is not an owner / also checks if they're in channel
    if checkOwner(auth_user_id, channel_id) is False and DreamOwner is False:
        raise AccessError(description="Error: Not an owner")
    
    for counter in database.data["channelList"]:
        if counter["id"] is channel_id:
            counter["owner_ids"].append(u_id)
            break

    return {
    }

'''
channel_removeowner_v1 takes in the user's token and the u_id they wish to remove as owner.
The function then checks whether both the token and u_id is valid, the channel is valid, if the user's token is the only owner and if u_id is not an owner.
If so, it removed the user's ID in the channel's 'member ids' and returns nothing. If conditions are breached, it raises an InputError or AccessError

Arguments:
    token(string) - User's ID
    channel_id (string) - Channel's ID

Exceptions:
    InputError - when the user's ID is invalid
    InputError - when the channel ID is invalid
    InputError - when the u_id is not an owner
    InputError - when the token is not an owner

Return Value:
    Returns nothing.
'''

def channel_removeowner_v1(token, channel_id, u_id):

    auth_user_id = get_user_id_from_token(token)

    DreamOwner = checkDreamowner(auth_user_id)

    # If u_id is valid
    if valid_userid(u_id) is False:
        raise InputError(description="Error: Invalid user id")

    # If channel_id is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel ID")

    # If the u_id is not an owner
    if checkOwner(u_id, channel_id) is False:
        raise InputError(description="Error: Not An Owner")

    # If the u_id is the only owner
    for channel in database.data["channelList"]:
        if channel_id == channel["id"]:
            if len(channel["owner_ids"]) == 1:
                raise InputError(description="Error: Only one owner")

    # If the token is not an owner
    if checkOwner(auth_user_id, channel_id) is False and DreamOwner is False:
        raise InputError(description="Error: Token is Not Owner")

    # Main Implemenation
    for channel in database.data["channelList"]:
        if channel_id == channel["id"]:
            for owner in channel["owner_ids"]:
                if u_id is owner:
                    channel["owner_ids"].remove(u_id)
    return {
    }
