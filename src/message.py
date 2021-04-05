from src.error import InputError, AccessError
from src.utils import valid_userid, valid_dmid, check_useralreadyindm, valid_channelid, check_useralreadyinchannel, check_messageid, get_user_id_from_token, getchannelID, checkOwner
import src.database as database
from datetime import datetime

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
        raise InputError("Error: Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError("Error: Empty Message")

    if valid_channelid(channel_id) is False:
        raise InputError("Error: Invalid channel")

    if check_useralreadyinchannel(u_id, channel_id) is False:
        raise AccessError("Error: User not in channel")
        

    # setting the time and date

    temp = datetime.now()
    remove_temp = temp.replace(microsecond = 0)
    final_time = remove_temp.timestamp()
    
    length_of_total = len(database.data["message_ids"])
    new_message_id = length_of_total + 1

    message_final = {
        'message': message,
        'message_id': new_message_id,
        'u_id': u_id,
        'time_created': final_time
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
        raise InputError("Error: Invalid message ID")

    channel_id = getchannelID(message_id)

    for channels1 in database.data["channelList"]:
        for message_info in channels1.get('messages'):
            if message_info.get("message_id") is message_id:
                if checkOwner(u_id, channel_id):
                    if message_info['message'] is None:
                        raise InputError("Message already removed")
                    else:
                        channels1['messages'].remove(message_info)
                        break
                
                elif message_info.get("u_id") is u_id:
                    if message_info['message'] is None:
                        raise InputError("Message already removed")
                    else:
                        channels1['messages'].remove(message_info)
                        break   
                else:
                    raise AccessError("Erorr: Remover not an owner nor original poster")
            
            
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
        raise InputError("Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError("Error: Empty Message")

    if check_messageid(message_id) is True:
        raise InputError("Error: Invalid message ID")

    channel_id = getchannelID(message_id)

    for channels1 in database.data["channelList"]:
        for message_info in channels1.get('messages'):
            if message_info.get("message_id") is message_id:
                if checkOwner(u_id, channel_id):
                    message_info["message"] = message
                    break
                
                elif message_info.get("u_id") is u_id:
                    message_info["message"] = message
                    break
                
                else:
                    raise AccessError("Error: Editor not an owner nor original poster")

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
    dm_id (int) - DM's ID
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
        raise InputError("Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

    if not message:
        raise InputError("Error: Empty Message")

    if valid_dmid(dm_id) is False:
        raise InputError("Error: Invalid dm ID")

    if check_useralreadyindm(u_id, dm_id) is False:
        raise AccessError("Error: User not in dm")

    temp = datetime.now()
    remove_temp = temp.replace(microsecond = 0)
    final_time = remove_temp.timestamp()
    
    length_of_total = len(database.data["message_ids"])
    new_message_id = length_of_total + 1

    message_final = {
        'message': message,
        'message_id': new_message_id,
        'u_id': u_id,
        'time_created': final_time
    }

    for right_dm in database.data["dmList"]:
        if right_dm["id"] is dm_id:
            right_dm['messages'].append(message_final)

    message_id = {
        'message_id': new_message_id,
    }

    database.data["message_ids"].append(message_id)

    return message_id