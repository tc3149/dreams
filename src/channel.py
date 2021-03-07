import re
from src.error import InputError, AccessError
from src.database import accData, channelList
from src.channels import channels_create_v1
from src.auth import auth_register_v1

'''
channel_invite_v1 takes in an auth_user_id integer, a channel_id integer and u_id integer. 
The function then checks if the channel_id is exists, if both users exists, if auth_user_id is already a member of the channel and if u_id is a member of the channel.
If all requirements are met the function then adds u_id to the channel and returns {}, otherwise it raises InputError or AccessError.

Arguments:
    auth_user_id (integer)      - Id of user who owns the channel
    channel_id (integer)        - Id of channel
    u_id (integer)              - Id of user being added to the channel   
    ...

Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when given u_id does not exist
    InputError  - Occurs when given auth_user_id does not exist
    InputError  - Occurs when given u_id already a member of the channel they are being added to
    ValueError  - Occurs when given auth_user_id is not a member of the channel

Return Value:
    Returns {}
'''

def channel_invite_v1(auth_user_id, channel_id, u_id):
    #check if channel exists
    for channel in channelList:
        if channel_id <= len(channelList):
            #channel does exist
            break
        else:
            #channel does not exist
            raise InputError ("Channel does not exis")
    
    #check if auth_user_id exists 
    auth_id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            auth_id_status = True
            break
   
    if auth_id_status is False:
        # auth_user_id does not exist
        raise InputError ("Inviting user does not exist")
            
    
    #check if auth_user_id owner member of channel
    owner_status = False
    for user in channelList[channel_id]['owner_ids']:   
        if auth_user_id in channelList[channel_id]['owner_ids']:
            #user is owner member of channel
            owner_status = True
            break
               
    if owner_status is False:
        #user does not have access
        raise AccessError ("User does not have access")

    #check if u_id exists
    u_id_status = False
    for user2 in accData:
        if user2.get("id") is u_id:
            #u_id exists
            u_id_status = True
            break
            
    if u_id_status is False:
        # u_id does not exist
        raise InputError ("Invited user does not exist")
    
    #check if u_id already member of the channel
    for user2 in channelList[channel_id]['member_ids']:
        
        if u_id in channelList[channel_id]['member_ids']:
            #u_id is member of channel
            raise InputError ("User already a member")    

            
    
    #add u_id to channel
    
    channelList[channel_id]['member_ids'].append(u_id)
    
    return {

    }

'''
channel_details_v1 takes in an auth_user_id integer and a channel_id integer. 
The function then checks if the channel_id is exists, if auth_user_id exists and is already a member of the channel.
If all requirements are met the function then returns the contents of the channel including the name, ownermembers and all members, otherwise it raises InputError or AccessError.

Arguments:
    auth_user_id (integer)      - Id of user who owns the channel
    channel_id (integer)        - Id of channel 
    ...

Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when given auth_user_id does not exist
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

def channel_details_v1(auth_user_id, channel_id):

    #check if channel exists
    for channel in channelList:
        if channel_id <= len(channelList):
            #channel does exist
            break
        else:
            #channel does not exist
            raise InputError ("Channel does not exis")

    #check if auth_user_id exists 
    auth_id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            auth_id_status = True
            break
   
    if auth_id_status is False:
        # auth_user_id does not exist
        raise AccessError ("User does not exist")
            
    
    #check if auth_user_id owner member of channel
    member_status = False
    for user in channelList[channel_id]['member_ids']:
        
        if auth_user_id in channelList[channel_id]['member_ids']:
            #user is owner member of channel
            member_status = True
            break
               
    if member_status is False:
        #user does not have access
        raise AccessError ("User does not have access")
    
    #loop to add member details
    
    allMembers = []
    ownMembers = []
    for memberID in channelList[channel_id]['member_ids']:
        for mem in accData:
            if memberID is mem['id']:
                new_member = {
                    'u_id':memberID,
                    'email': accData[memberID]['email'],
                    'name_first': accData[memberID]['name_first'],
                    'name_last': accData[memberID]['name_last'],
                    'handle_str': accData[memberID]['handle']
                }
                allMembers.append(new_member)
                break
            
            
    #loop to add owner details
    
    for ownerID in channelList[channel_id]['owner_ids']:       
        for own in accData:
            if ownerID is own['id']:
                owner = {
                    'u_id':ownerID,
                    'email': accData[ownerID]['email'],
                    'name_first': accData[ownerID]['name_first'],
                    'name_last': accData[ownerID]['name_last'],
                    'handle_str': accData[ownerID]['handle']
                }
                ownMembers.append(owner)
                break
            
            
    
    return {
        'name': channelList[channel_id]['name'],
        'owner_members':ownMembers,
        'all_members':allMembers
    
    }

'''
channel_messages_v1 takes in a user id, a specific channel id, and a 'start' to
determine after what amount of messages to show, e.g. recent 5 messages have 
already been seen, thus start would equal 5 to see later messages.
The function first does security checks, then reverses the messages list, so
that the most recent messages are at the head of the list, then appends to a new
list for return.

Arguments:
    auth_user_id (integer) - Unique user id created by auth_register_v1
    channel_id (integer) - Unique channel id created by channels_create_v1
    start (integer) - Starts the message list from index start. So if start is 5, will skip the first 5 
    indexes relating to recent messages

Exceptions:
    AccessError - Occurs when auth_user_id is not valid (i.e. not created)

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

def channel_messages_v1(auth_user_id, channel_id, start):

    # Check if user id is valid
    if valid_userid(auth_user_id) is False:
        raise AccessError("Error: Invalid user id")

    # Check if channel id is valid
    if valid_channelid(channel_id) is False:
        raise AccessError("Error: Invalid channel")

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
        '''
        msg = {
            'message_id': messages[starting_index]["message_id"], 
            'u_id': messages[starting_index]["u_id"],
            'message': messages[starting_index]["message"],
            'time_created': messages[starting_index]["time_created"],
        }
        messages_shown.append(msg)
        '''
        messages_shown.append(messages[starting_index])
        msg_amt = msg_amt + 1
    if len(messages) is 0 or msg_amt < 50:
        end = -1
    return {
        'messages': messages_shown,
        'start': start,
        'end': end,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

'''
channel_join_v1 takes in the user's ID and the channel they wish to join.
The function then checks whether the ID is valid, the channel is valid, if the channel is private or if the user is already in the channel.
If so, it appends the user's ID into the channel's 'member ids' and returns nothing. If conditions are breached, it raises an InputError or AccessError

Arguments:
    auth_user_id (string) - User's ID
    channel_id (string) - Channel's ID

Exceptions:
    InputError - when the user's ID is invalid
    InputError - when the channel ID is invalid
    AccessError - when user tries to join a private channel
    AccessError - when user is already in the channel

Return Value:
    Returns nothing.
'''

def channel_join_v1(auth_user_id, channel_id):

    # check whether id is valid
    if valid_userid(auth_user_id) is False:
        raise InputError("Error: Invalid user id")

    # check whether channel is invalid
    if valid_channelid(channel_id) is False:
        raise InputError("Error: Invalid channel")

    # check if channel is private
    if check_channelprivate(channel_id) is True:
        raise AccessError("Private Channel")
    
    # check user already in channel
    if check_useralreadyinchannel(auth_user_id, channel_id) is True:
        raise AccessError("User already in channel")

    for channel in channelList:
        if channel["id"] is channel_id:
            channel["member_ids"].append(auth_user_id)

    return {
    }

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


def check_channelprivate(channel_id):

    for channel in channelList:
        if channel.get("id") is channel_id:
            if channel.get("is_public") is True:
                return False
    return True

def check_useralreadyinchannel(auth_user_id, channel_id):

    for channel in channelList:
        if channel.get("id") is channel_id:
            for member in channel["member_ids"]:
                if auth_user_id is member:
                    return True
    return False
    