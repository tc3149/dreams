from src.error import InputError, AccessError
from src.utils import valid_userid, valid_dmid, check_useralreadyindm, valid_channelid, check_useralreadyinchannel, check_messageid, get_user_id_from_token, getchannelID, checkOwner
import src.database as database
from datetime import datetime


def message_send_v2(token, channel_id, message):
    
    length = int(len(message))

    if length > 1000:
        raise InputError("Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

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

def message_edit_v2(token, message_id, message):
    length = int(len(message))

    if length > 1000:
        raise InputError("Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

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

def message_senddm_v1(token, dm_id, message):
    length = int(len(message))

    if length > 1000:
        raise InputError("Message is more than 1000 characters")

    u_id = get_user_id_from_token(token)

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
    #if the message is being shared to a dm
    if channel_id == -1:
        #check if token belongs to a user in the DM
        user_id = get_user_id_from_token(token)
        if check_useralreadyindm(user_id,dm_id) == True: 
            #find message from the og_message_id
            
            for channel in data['channelList']:
                for messages in channel['messages']:
                    if messages['message_id'] is og_message_id:
                        og_message = messages['message_id']['message']
                        break
            #combine og message and the optional additional message
            final_message = message + '\n\n"""\n' + og_message['message'] + '\n"""'

            if len(final_message) > 1000 or len(final_message) == 0:
                raise er.InputError("Messages must be between 0 and 1000 characters")
            #share the dm
            shared_message_id = message_senddm_v1(token,dm_id,final_message)
            
        else:
            raise AccessError ('User not member of target DM')
    
    #if the message is being shared to a channel
    if dm_id == -1:
        #check if token belongs to a user in the Channel
        user_id = get_user_id_from_token(token)
        if check_useralreadyinchannel(user_id,channel_id) == True:
            #find message from the og_message_id
            
            for channel in data['channelList']:
                for messages in channel['messages']:
                    if messages['message_id'] is og_message_id:
                        og_message = messages['message_id']['message']
                        break
            #combine og message and the optional additional message
            final_message = message + '\n\n"""\n' + og_message['message'] + '\n"""'

            if len(final_message) > 1000 or len(final_message) == 0:
                raise er.InputError("Messages must be between 0 and 1000 characters")
                
            #share the message
            shared_message_id = message_send_v2(token,channel_id,final_message)
            
        else:
            raise AccessError ('User not member of target Channel')
    
    return{
        shared_message_id
    }