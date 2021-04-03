from src.database import data, secretSauce
from src.error import InputError, AccessError
import jwt


def valid_userid(auth_user_id):
    # Check if user id is valid
    for user in data["accData"]:
        if user.get("id") is auth_user_id:
            return True
    return False

def valid_channelid(channel_id):
    # Check if channel id is valid
    for channel in data["channelList"]:
        if channel.get("id") is channel_id:
            return True
    return False


def check_channelprivate(channel_id):

    for channel in data["channelList"]:
        if channel.get("id") is channel_id:
            if channel.get("is_public") is True:
                return False
    return True

def check_useralreadyinchannel(auth_user_id, channel_id):

    for channel in data["channelList"]:
        if channel.get("id") is channel_id:
            for member in channel["member_ids"]:
                if auth_user_id is member:
                    return True
    return False

def check_messageid(message_id):

    for i in data["channelList"]:
        for message1 in i['messages']:
            if message1.get('message_id') is message_id:
                return False
    return True

def getchannelID(message_id):

    for i in data["channelList"]:
        for message1 in i['messages']:
            if message1.get('message_id') is message_id:
                channel_id1 = i.get("channel_id")
                break
    return channel_id1

def checkOwner(auth_user_id, channel_id):

    for channel in data["channelList"]:
        if channel["id"] is channel_id:
            for users in channel["owner_ids"]:
                if users is auth_user_id:
                    return True

    return False



def detoken(token):
    u_id = jwt.decode(token, secretSauce, algorithm="HS256")

    return u_id["auth_user_id"]

def get_user_id_from_token(token):
    sessionId = jwt.decode(token, secretSauce, algorithms="HS256")
    for user in data["accData"]:
        for session in user["sessions"]:
            if sessionId["sessionId"] == session:
                return user["id"]
    
    raise InputError("Token does not exist")
