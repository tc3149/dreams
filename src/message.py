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