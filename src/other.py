import pytest
import re
from json import dumps
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
import src.config as config
from src.error import InputError, AccessError
from src.channel import channel_messages_v2
from src.channels import channels_create_v2
import src.database as database
from json import dumps, loads
import os
from src.utils import saveData, get_user_id_from_token

'''
clear_v1 resets everything to default state by clearing the database list, and
setting id data to 0.

Arguments:
    N/A
Exceptions:
    N/A
Return Value:
    N/A
'''
def clear_v1():

    if database.data["accData"]:
        for userId in database.data["userProfiles"]:
            pImageName = userId["profile_img_url"][-9:]
            if os.path.exists(f"src/static/{pImageName}"):
                os.remove(f"src/static/{pImageName}")

    database.idData["sessionId"] = 0
    database.idData["userId"] = 0
    database.idData["dmId"] = 0
    database.idData["messageId"] = 0
    database.data["accData"].clear() 
    database.data["channelList"].clear() 
    database.data["message_ids"].clear()
    database.data["dmList"].clear()
    database.data["userProfiles"].clear()
    database.dreamsAnalytics["channels_exist"].clear()
    database.dreamsAnalytics["dms_exist"].clear()
    database.dreamsAnalytics["messages_exist"].clear()
    database.dreamsAnalytics["utilization_rate"] = 0

    database.userAnalytics["channels_joined"].clear()
    database.userAnalytics["dms_joined"].clear()
    database.userAnalytics["messages_sent"].clear()
    database.userAnalytics["involvement_rate"] = 0

    database.onlineURL = ""

    with open("src/serverDatabase.json", "w") as dataFile:
        dataFile.write(dumps(database.data))

'''
search_v1 takens in a query string and returns a collection of messages in all 
of the channels/DMS that the user has joined that match the query. Firstly, security
checks are made (ensuring token is valid) and query string is not too long (< 1000)
The function first creates a message list of EVERY message that the user has access to
and would visibly be able to see - this is done by looping through every channel and dm
and extending any messages to the message list
It then filters the message list using a lambda function and regex search to remove any
messages that do not match the query string

Arguments:
    token (string) - User's Authorisation Hash
    query_str (string) - User's desired string to search for

Exceptions:
    AccessError - when the token is invalid
    InputError - when the query string is above 1000 characters
'''
def search_v1(token, query_str):

    auth_user_id = get_user_id_from_token(token)
    
    if len(query_str) > 1000:
        raise InputError(description="Error: Query string is above 1000 characters")

    # Store every message in channels/dms that the user is a part of
    message_list = []
    for channel in database.data["channelList"]:
        if auth_user_id in channel.get("member_ids"):
            message_list.extend(channel["messages"])

    for dm in database.data["dmList"]:
        if auth_user_id in dm.get("member_ids"):
            message_list.extend(dm["messages"])
    
    filtered_message = list(filter(lambda message: re.search(query_str, message["message"]), message_list))
    return {
        'messages': filtered_message
    }
