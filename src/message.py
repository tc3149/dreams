from src.error import InputError, AccessError
from src.utils import valid_userid, valid_dmid, check_useralreadyindm, valid_channelid, check_useralreadyinchannel, check_messageid, get_user_id_from_token, getchannelID, checkOwner
from src.utils import check_messageid_in_DM, getdmID, checkOwnerinDM, checkTags
import src.database as database
from datetime import datetime
from threading import Timer
from time import sleep


'''
message_send_v2 takes in the token of a user, a channel ID and a message the user wishes to send to the channel.
The function then checks whether the message's length is not over 1000 characters, if the token is valid, if the message is not empty, if the channel's ID is valid and 
if the user is in the channel to send that message.
If so, it appends a channelList of a message dictionary containing the message, message_id, the u_ID of whoever sent the message and when the message was created. 
The function then returns a dictionary containing the message_id.
If conditions are breached, it raises an InputError or AccessError.

Arguments:
    token (string) - User's Authorisation Hash
    channel_id (int) - Channel's ID
    message (string) - User's desired message

Exceptions:
    InputError - when the message is over 1000 characters
    AccessError - when the token is invalid
    InputError - when the message is empty
    InputError - when the channel ID is invalid
    AccessError - when the user is not in the channel

Return Value:
    Returns {
        'message_id': new_message_id (which is the dictionary of the message ID)
    }
'''
def message_send_v2(token, channel_id, message):
    
    length = int(len(message))

    if length > 1000:
        raise InputError(description="Error: Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError(description="Error: Empty Message")

    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel")

    if check_useralreadyinchannel(u_id, channel_id) is False:
        raise AccessError(description="Error: User not in channel")
        
    checkTags(u_id, message, channel_id, -1)
    # setting the time and date

    final_time = int(datetime.timestamp(datetime.now()))
    
    database.idData['messageId'] = database.idData["messageId"] + 1
    new_message_id = database.idData["messageId"]

    react_dictionary = [{
        "react_id": 1,
        "u_ids": [],
        "is_this_user_reacted": False,
    }]
    
    message_final = {
        'message': message,
        'message_id': new_message_id,
        'u_id': u_id,
        'time_created': final_time,
        "reacts": react_dictionary,
        "is_pinned": False,
    }

    for right_channel in database.data["channelList"]:
        if right_channel["id"] is channel_id:
            right_channel['messages'].append(message_final)

    message_id = {
        'message_id': new_message_id,
    }

    database.data["message_ids"].append(message_id)

    return message_id


'''
message_remove_v1 takes in the token of a user and the message ID of which they wish to remove.
The function then checks whether the message's length is not over 1000 characters, if the token is valid and if the message's ID is valid to remove the message.
If so, it loops to through each channel then messages to match the message_id of the given, and thus removes the message. Through this loop, it also checks whether
the user (token) is authorised to do so; if the user is an owner of the channel, or the original poster. The message cannot be removed also if it is empty (i.e. already removed)
If conditions are breached, it raises an InputError or AccessError.
The function then returns nothing.

Arguments:
    token (string) - User's Authorisation Hash
    message_id (int) - Message's ID

Exceptions:
    AccessError - when the token is invalid
    InputError - when the message ID is invalid
    AccessError - when the user (token) is not authorised to do so
    InputError - when the message is removed already

Return Value:
    Returns {
    }
'''
def message_remove_v1(token, message_id):
    
    u_id = get_user_id_from_token(token)

    if check_messageid(message_id) is True:
        raise InputError(description="Error: Invalid message ID")

    channel_id = getchannelID(message_id)

    for channel in database.data["channelList"]:
        for messages1 in channel["messages"]:
            if messages1["message_id"] == message_id:
                if checkOwner(u_id, channel_id) is True or messages1["u_id"] == u_id:
                    if not messages1["message"]:
                        raise InputError(description="Error: Message already removed")
                    else:
                        messages1["message"] = ""
                else:
                    raise AccessError(description="Error: Remover not an owner nor original poster")



    """
    for channels1 in database.data["channelLisSt"]:
        for message_info in channels1.get('messages'):
            if message_info.get("message_id") is message_id:
                if checkOwner(u_id, channel_id) or message_info.get("u_id") is u_id:
                    if message_info['message'] is "":
                        raise InputError(description="Message already removed")
                    else:
                        message_info["message"] == ""
                else:
                    raise AccessError(description="Error: Remover not an owner nor original poster")
    """
            
    return {}


'''
message_edit_v2 takes in the token of a user, a message ID the user wishes to edit, and that edited message.
The function then checks whether the message's length is not over 1000 characters, if the token is valid, if the message is not empty, if the message's ID is valid to edit the message.
If so, it loops to through each channel then messages to match the message_id of the given, and thus edit the message. Through this loop, it also checks whether
the user (token) is authorised to do so; if the user is an owner of the channel, or the original poster.
If conditions are breached, it raises an InputError or AccessError.
The function then returns nothing.

Arguments:
    token (string) - User's Authorisation Hash
    message_id (int) - Message's ID
    message (string) - User's desired edits

Exceptions:
    InputError - when the message is over 1000 characters
    AccessError - when the token is invalid
    InputError - when the message is empty
    InputError - when the message ID is invalid
    AccessError - when the user (token) is not authorised to do so

Return Value:
    Returns {
    }
'''

def message_edit_v2(token, message_id, message):
    length = int(len(message))

    if length > 1000:
        raise InputError(description="Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError(description="Error: Empty Message")

    if check_messageid(message_id) is True:
        raise InputError(description="Error: Invalid message ID")

    channel_id = getchannelID(message_id)

    for channels1 in database.data["channelList"]:
        for message_info in channels1.get('messages'):
            if message_info.get("message_id") is message_id:
                if checkOwner(u_id, channel_id):
                    message_info["message"] = message
                
                elif message_info.get("u_id") is u_id:
                    message_info["message"] = message
                
                else:
                    raise AccessError(description="Error: Editor not an owner nor original poster")

    return {}


'''
message_senddm_v1 takes in the token of a user, a dm ID and a message the user wishes to send to the channel.
The function then checks whether the message's length is not over 1000 characters, if the token is valid, if the message is not empty, if the dm's ID is valid and 
if the user is in the channel to send that message.
If so, it appends to a dmList of a message dictionary containing the message, message_id, the u_ID of whoever sent the message and when the message was created. 
The function then returns a dictionary containing the message_id.
If conditions are breached, it raises an InputError or AccessError.

Arguments:
    token (string) - User's Authorisation Hash
    message_id (int) - DM's ID
    message (string) - User's desired message

Exceptions:
    InputError - when the message is over 1000 characters
    AccessError - when the token is invalid
    InputError - when the message is empty
    InputError - when the DM's ID is invalid
    AccessError - when the user is not in the dm

Return Value:
    Returns {
        'message_id': new_message_id (which is the dictionary of the message ID)
    }
'''
def message_senddm_v1(token, dm_id, message):
    length = int(len(message))

    if length > 1000:
        raise InputError(description="Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError(description="Error: Empty Message")

    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: Invalid dm ID")

    if check_useralreadyindm(u_id, dm_id) is False:
        raise AccessError(description="Error: User not in dm")

    checkTags(u_id, message, -1, dm_id)

    final_time = int(datetime.timestamp(datetime.now()))
    
    database.idData['messageId'] = database.idData["messageId"] + 1
    new_message_id = database.idData['messageId']

    react_dictionary = [{
        "react_id": 1,
        "u_ids": [],
        "is_this_user_reacted": False
    }]

    message_final = {
        'message': message,
        'message_id': new_message_id,
        'u_id': u_id,
        'time_created': final_time,
        "reacts": react_dictionary,
        "is_pinned": False,
    }

    for right_dm in database.data["dmList"]:
        if right_dm["id"] is dm_id:
            right_dm['messages'].append(message_final)

    message_id = {
        'message_id': new_message_id,
    }

    database.data["message_ids"].append(message_id)

    return message_id

'''
message_share_v1 takes in a token from the user calling the function, an og_message_id integer from the message the user wantsshare, an optional message string, the channel_id or dm_id of the channel or dm the user wants to share the message to.
The function then checks whether the user wants to share to a DM or a channel indicated by the non target function which has the value(-1).
Then the fuction checks if the dm_id or channel_id exist depending on the intended target also verifies if the authorising user is indeed a member of the channel or DM they a sharing the message to.
If all requirements are met the function then shares the og_message combined with the optional message, and returns the id of the shared function(shared_messag-id).

Arguments:
    token (integer)             - Users authorisation Hash
    og_message_id(integre)      -Id of the message being shared
    message                     -String a user may add to the original message    
    channel_id (integer)        - Id of channel
    dm_id (integer)             - Id of dm  
    ...

Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when given dm_id does not exist
    InputError  - Occurs when given u_id already a member of the channel they are being added to
    ValueError  - Occurs when given token is not a member of the channel
    ValueError  - Occurs when given token is not a member of the DM

Return Value:
    Returns {shared_message_id}
'''
def message_share_v1(token,og_message_id,message,channel_id,dm_id):
    if channel_id == -1 and dm_id == -1:
        raise InputError(description="No channel or dm id specified")

    user_id = get_user_id_from_token(token)
    # Set og_message to False
    og_message = ""

    if channel_id == -1:
        # Sharing to a dm
        # Check if user is in dm
        if check_useralreadyindm(user_id, dm_id):
            # Find message using message id
            # Check channel messages
            for channel in database.data["channelList"]:
                for messages in channel["messages"]:
                    if messages["message_id"] == og_message_id:
                        og_message = messages["message"]
            if not og_message:
                # Check dm messages
                for dm in database.data["dmList"]:
                    for dmMessages in dm["messages"]:
                        if dmMessages["message_id"] == og_message_id:
                            og_message = dmMessages["message"]
            if not og_message:
                raise InputError(description="Message does not exist")
            final_message = message + '\n\n"""\n' + og_message + '\n"""'
            if len(final_message) > 1000 or len(final_message) == 0:
                raise InputError(description="Messages must be between 0 and 1000 characters")
            shared_message_id = message_senddm_v1(token,dm_id,final_message)        
        else:
            raise AccessError ('User not member of target dm')
    elif dm_id == -1:
        # Sharing to a channel
        # Check if user is in channel
        if check_useralreadyinchannel(user_id, channel_id):
            # Find message using message id
            # Check dm messages
            for dm in database.data["dmList"]:
                    for dmMessages in dm["messages"]:
                        if dmMessages["message_id"] == og_message_id:
                            og_message = dmMessages["message"]
            if not og_message:
                # Check channel messages
                for channel in database.data["channelList"]:
                    for messages in channel["messages"]:
                        if messages["message_id"] == og_message_id:
                            og_message = messages["message"]
            if not og_message:
                raise InputError(description="Message does not exist")
            final_message = message + '\n\n"""\n' + og_message + '\n"""'
            if len(final_message) > 1000 or len(final_message) == 0:
                raise InputError("Messages must be between 0 and 1000 characters")
            shared_message_id = message_send_v2(token, channel_id, final_message)
        else:
            raise AccessError (description='User not member of target Channel')
    else:
        raise InputError(description="Only specify either a dm or channel")

    return {
        "shared_message_id": shared_message_id
    }


def message_sendlater_v1(token, channel_id, message, time_sent):

    u_id = get_user_id_from_token(token)

    length = len(message)

    if length > 1000:
        raise InputError(description="Message is more than 1000 characters")

    if not message:
        raise InputError(description="Error: Empty Message")

    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid Channel ID")

    if check_useralreadyinchannel(u_id, channel_id) is False:
        raise AccessError(description="Error: User not in channel")

    time_now = int(datetime.timestamp(datetime.now()))
    time_difference = int(time_sent - time_now)

    if time_difference < 0:
        raise InputError(description="Error: Time is in the past")

    timer_to_send = Timer(time_difference, message_send_v2, args=[token, channel_id, message])
    timer_to_send.start()


    return {
        "message_id": database.idData["messageId"] + 1
    }
                     

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    u_id = get_user_id_from_token(token)

    length = len(message)

    if length > 1000:
        raise InputError(description="Message is more than 1000 characters")

    if not message:
        raise InputError(description="Error: Empty Message")

    if valid_dmid(dm_id) is False:
        raise InputError(description="Error: Invalid dm ID")

    if check_useralreadyindm(u_id, dm_id) is False:
        raise AccessError(description="Error: User not in dm")

    time_now = int(datetime.timestamp(datetime.now()))
    time_difference = int(time_sent - time_now)

    if time_difference < 0:
        raise InputError(description="Error: Time is in the past")

    timer_to_send = Timer(time_difference, message_senddm_v1, args=[token, dm_id, message])
    timer_to_send.start()

    return {
        "message_id": database.idData["messageId"] + 1
    }

def message_react_v1(token, message_id, react_id):

    u_id = get_user_id_from_token(token)

    if react_id != 1:
        raise InputError(description="Error: Invalid react ID")

    in_channel = check_messageid(message_id)
    in_dm = check_messageid_in_DM(message_id)

    if in_channel and in_dm is True:
        raise InputError(description="Error: Invalid message ID")


    if in_channel is False:
        channel_id = getchannelID(message_id)

        if check_useralreadyinchannel(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not in channel")

        address = database.data["channelList"]

    elif in_dm is False:
        dm_id = getdmID(message_id)

        if check_useralreadyindm(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not in dm")

        address = database.data["dmList"]
        
    
    for channels in address:
        for msg in channels["messages"]:
            if msg["message_id"] == message_id:
                for react_info in msg["reacts"]:
                    if u_id not in react_info["u_ids"]:
                        react_info["u_ids"].append(u_id)

                        if u_id == msg["u_id"]:
                            react_info["is_this_user_reacted"] = True
                    
                    else:
                        raise InputError(description="Error: User has already reacted to this message")

    return {}


def message_unreact_v1(token, message_id, react_id):

    u_id = get_user_id_from_token(token)

    if react_id != 1:
        raise InputError(description="Error: Invalid react ID")

    in_channel = check_messageid(message_id)
    in_dm = check_messageid_in_DM(message_id)

    if in_channel and in_dm is True:
        raise InputError(description="Error: Invalid message ID")

    if in_channel is False:
        channel_id = getchannelID(message_id)

        if check_useralreadyinchannel(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not in channel")

        address = database.data["channelList"]

    elif in_dm is False:
        dm_id = getdmID(message_id)

        if check_useralreadyindm(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not in dm")

        address = database.data["dmList"]
        
    for channels in address:
        for msg in channels["messages"]:
            if msg["message_id"] == message_id:

                for react_info in msg["reacts"]:

                    if u_id in react_info["u_ids"]:
                        react_info["u_ids"].remove(u_id)

                        if u_id == msg["u_id"]:
                            react_info["is_this_user_reacted"] = False
                    
                    else:
                        raise InputError(description="Error: User has already unreacted to this message")

    return {}


def message_pin_v1(token, message_id):
    u_id = get_user_id_from_token(token)

    in_channel = check_messageid(message_id)
    in_dm = check_messageid_in_DM(message_id)

    if in_channel and in_dm is True:
        raise InputError(description="Error: Invalid message ID")


    if in_channel is False:
        channel_id = getchannelID(message_id)

        if check_useralreadyinchannel(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not in channel")

        if checkOwner(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not authorised to do so")

        address = database.data["channelList"]


    elif in_dm is False:
        dm_id = getdmID(message_id)

        if check_useralreadyindm(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not in DM")

        if checkOwnerinDM(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not authorised to do so")

        address = database.data["dmList"]
    

    for channels in address:
        for msg in channels["messages"]:
            if msg["message_id"] == message_id:

                if msg["is_pinned"] is True:
                    raise InputError(description="Error: Message is already pinned")
                
                else:
                    msg["is_pinned"] = True
  
    return {}


def message_unpin_v1(token, message_id):
    u_id = get_user_id_from_token(token)

    in_channel = check_messageid(message_id)
    in_dm = check_messageid_in_DM(message_id)

    if in_channel and in_dm is True:
        raise InputError(description="Error: Invalid message ID")


    if in_channel is False:
        channel_id = getchannelID(message_id)

        if check_useralreadyinchannel(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not in channel")

        if checkOwner(u_id, channel_id) is False:
            raise AccessError(description="Error: User is not authorised to do so")

        address = database.data["channelList"]

    elif in_dm is False:
        dm_id = getdmID(message_id)

        if check_useralreadyindm(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not in DM")

        if checkOwnerinDM(u_id, dm_id) is False:
            raise AccessError(description="Error: User is not authorised to do so")
        
        address = database.data["dmList"]


    for channels in address:
        for msg in channels["messages"]:
            if msg["message_id"] == message_id:

                if msg["is_pinned"] is False:
                    raise InputError(description="Error: Message is already unpinned")
                
                else:
                    msg["is_pinned"] = False

    return {}