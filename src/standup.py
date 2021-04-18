import re
import src.database as database
from src.utils import get_user_id_from_token, valid_channelid, check_useralreadyinchannel
from src.error import InputError, AccessError
from src.message import message_send_v2
import datetime
import threading

def standup_start_v1(token, channel_id, length):

    auth_user_id = get_user_id_from_token(token)

    # Check if channel id is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel ID")

    # Check if a standup is already running on this channel
    #check the databse
    
    if standup_active_v1(token, channel_id)["is_active"] is True:
        raise InputError(description="Error: Standup is already active in this channel.")
    
    # Check if user is authorised in calling the standup
    if check_useralreadyinchannel(auth_user_id, channel_id) is False:
        raise AccessError(description="User is not a member of the channel")

    # Standup Main
    # Time Finish is time now + the input length (seconds)
    time_finish = datetime.datetime.now() + datetime.timedelta(0, int(length))

    # Store the data of newly active standup
    standupData = {
        'time_finish': int(time_finish.timestamp()),
        'channel_id': channel_id,
        'messages': [],
    }
    database.data["standupList"].append(standupData)

    # Now, to buffer every message sent using standup_send
    # temporarily store messags in standupData["messages"] then after a
    # timer (length) send all in the form of one message
    t = threading.Timer(int(length), standup_collection_send, args=[token, channel_id])
    t.start()

    return {
        "time_finish": int(time_finish.timestamp()),
    }

def standup_collection_send(token, channel_id):

    # This function is active when the standup is finished.
    lines = []
    for standup in database.data["standupList"]:
        if standup.get("channel_id") is channel_id:
            lines = standup.get("messages")
            break

    # Since standup has ended remove all data from database
    for standup in database.data["standupList"]:
        if standup.get("channel_id") is channel_id:
            # This removes all standupData including messages
            database.data["standupList"].remove(standup)

    # for the case where no messages are sent in the standup
    if not lines:
        return

    #combine strings and send from the creator of the standup
    package = '\n'.join(lines)
    message_send_v2(token, channel_id, package)  
    
    return

'''
Check if Standup is active in channel. COMPLETED
'''
def standup_active_v1(token, channel_id):

    auth_user_id = get_user_id_from_token(token)

    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel ID")

    is_active = False
    time_finish = None

    for standup in database.data["standupList"]:
        if standup.get("channel_id") is channel_id:
            is_active = True
            time_finish = standup["time_finish"]

    return {
        "is_active": is_active,
        "time_finish": time_finish,
    }
    


def standup_send_v1(token, channel_id, message):

    auth_user_id = get_user_id_from_token(token)

    # Check if channel id is valid
    if valid_channelid(channel_id) is False:
        raise InputError(description="Error: Invalid channel ID")

    # Check if message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message length greater than 1000 characters.")

    # Check if a standup is active for standup send to work
    if standup_active_v1(token, channel_id)["is_active"] is False:
        raise InputError(description="Error: Standup is not active in this channel.")

    # Check if user is authorised to send message
    if check_useralreadyinchannel(auth_user_id, channel_id) is False:
        raise AccessError(description="User is not a member of the channel")

    # Create and store the message
    # Message format is for example "Hayden: Hello World"
    for user in database.data["accData"]:
        if user.get("id") == auth_user_id:
            user_handle = user["handle"]
            break

    new_message = user_handle + ": " + message

    # Append message into standupList
    for standup in database.data["standupList"]:
        if standup.get("channel_id") is channel_id:
            standup["messages"].append(new_message)

    return {}