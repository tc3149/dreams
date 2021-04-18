import src.database as database
from src.error import InputError, AccessError
import string
import random
from json import dumps
import jwt


def valid_userid(auth_user_id):
    # Check if user id is valid
    for user in database.data["accData"]:
        if user.get("id") == auth_user_id:
            return True
    return False

def valid_channelid(channel_id):
    # Check if channel id is valid
    for channel in database.data["channelList"]:
        if channel.get("id") == channel_id:
            return True
    return False

def valid_dmid(dm_id):
    # Check if dm id is valid
    for dm in database.data["dmList"]:
        if dm.get("id") == dm_id:
            return True
    return False


def check_channelprivate(channel_id):

    for channel in database.data["channelList"]:
        if channel.get("id") == channel_id:
            if channel.get("is_public") == True:
                return False
    return True

def check_useralreadyinchannel(auth_user_id, channel_id):

    for channel in database.data["channelList"]:
        if channel.get("id") == channel_id:
            for member in channel["member_ids"]:
                if auth_user_id is member:
                    return True
    return False

def check_useralreadyindm(auth_user_id, dm_id):
    for dms in database.data["dmList"]:
        if dms.get("id") == dm_id:
            for member in dms["member_ids"]:
                if auth_user_id is member:
                    return True
    return False



def check_messageid(message_id):

    for i in database.data["channelList"]:
        for message1 in i['messages']:
            if message1.get('message_id') == message_id:
                if message1["message"] is not "":
                    return False
    return True

def check_messageid_in_DM(message_id):

    for i in database.data["dmList"]:
        for message1 in i["messages"]:
            if message1.get("message_id") == message_id:
                    if message1["message"] is not "":
                        return False
    return True

def getchannelID(message_id):

    for i in database.data["channelList"]:
        for message1 in i['messages']:
            if message1["message_id"] is message_id:
                channel_id1 = i.get("id")
                break
    return channel_id1

def getdmID(message_id):
    for i in database.data["dmList"]:
        for message1 in i['messages']:
            if message1["message_id"] is message_id:
                dm_id1 = i.get("id")
                break
    return dm_id1

def checkOwner(auth_user_id, channel_id):

    for channel in database.data["channelList"]:
        if channel["id"] is channel_id:
            for users in channel["owner_ids"]:
                if users is auth_user_id:
                    return True

    return False

def checkOwnerinDM(auth_user_id, dm_id):

    for dm in database.data["dmList"]:
        if dm["id"] is dm_id:
            for users in dm["owner_ids"]:
                if users is auth_user_id:
                    return True
    
    return False

def search_email(email):
    for items in database.data["accData"]:
        if items["email"] == email:
            return True
    return False


def search_handle(currUserHandle):
    for items in database.data["accData"]:
        if items["handle"] == currUserHandle:
            return True
    return False


def search_user(user):
    for items in database.data["accData"]:
        if items["id"] == user:
            return True
    return False

def get_user_id_from_token(token):
    sessionId = is_valid_token_return_data(token)
    for user in database.data["accData"]:
        for session in user["sessions"]:
            if sessionId["sessionId"] == session:
                return user["id"]
    
    raise AccessError(description="Token does not exist")

def is_valid_token_return_data(token):
    try:
        tokenData = jwt.decode(token, database.secretSauce, algorithms="HS256")
    except jwt.exceptions.InvalidSignatureError as e:
        raise AccessError(description="Invalid signature") from e
    if not isinstance(tokenData, dict):
        raise AccessError(description="Invalid type")

    checkKey = list(tokenData.keys())[0]
    if checkKey == "sessionId" and isinstance(tokenData["sessionId"], int):
        return tokenData
    raise AccessError(description="Invalid key or value")

def make_dm_name(u_ids):
    handle_list = []
    for user in database.data["accData"]:
        if user["id"] in u_ids:
            handle_list.append(user["handle"])
    sortedHandle = sorted(handle_list)
    return ",".join(sortedHandle)


# Save to data file
def saveData():
    with open("src/serverDatabase.json", "w") as dataFile:
        dataFile.write(dumps(database.data))

def getUserAccData(u_id):
    for user in database.data["accData"]:
        if user["id"] == u_id:
            return user

def getUserProfileData(u_id):
    for user in database.data["userProfiles"]:
        if user["u_id"] == u_id:
            return user    

def createAddNotification(channelId, dmId, notification_message, userId):
    userNotification = {
        "channel_id": channelId,
        "dm_id": dmId,
        "notification_message": notification_message,
    }
    for user in database.data["accData"]:
        if user["id"] == userId:
            user["notifications"].append(userNotification)
            return
    raise InputError(description="User ID not found")

def inviteNotification(channelId, dmId, userId, userInviterId):
    if channelId == -1 and dmId == -1:
        raise InputError(description="Both ids cannot be -1")
    if channelId != -1 and dmId != -1:
        raise InputError(description="Both ids cannot be ! -1")

    userInviterHandle = getHandleFromId(userInviterId)
    if channelId == -1:
        dmName = getDmNameFromId(dmId)
        notiMessage = f"{userInviterHandle} added you to {dmName}."
    elif dmId == -1:
        channelName = getChannelNameFromId(channelId)
        notiMessage = f"{userInviterHandle} added you to {channelName}"
    createAddNotification(channelId, dmId, notiMessage, userId)

def checkTags(userSendId, message, channel_id, dm_id):
    if channel_id == -1 and dm_id == -1:
        raise InputError(description="Both ids cannot be -1")
    if channel_id != -1 and dm_id != -1:
        raise InputError(description="Both ids cannot be ! -1")


    if channel_id == -1:
        checkDmExists = False
        for dm in database.data["dmList"]:
            if dm["id"] == dm_id:
                checkDmExists = True
                dmMems = dm["member_ids"]
        if not checkDmExists:
            raise AccessError(description="DM id does not exist")
        for mem in dmMems:
            memHandle = getHandleFromId(mem)
            if "@" + memHandle in message:
                userSendHandle = getHandleFromId(userSendId)
                dmRoomName = getDmNameFromId(dm_id)
                notiMessage = f"{userSendHandle} tagged you in {dmRoomName}: {message[:20]}"
                createAddNotification(channel_id, dm_id, notiMessage, mem)
                return
    if dm_id == -1:
        checkChannelExists = False
        for channel in database.data["channelList"]:
            if channel["id"] == channel_id:
                checkChannelExists = True
                channelMems = channel["member_ids"]
        if not checkChannelExists:
            raise AccessError(description="Channel id does not exist")
        for mem in channelMems:
            memHandle = getHandleFromId(mem)
            if "@" + memHandle in message:
                userSendHandle = getHandleFromId(userSendId)
                channelName = getChannelNameFromId(channel_id)
                notiMessage = f"{userSendHandle} tagged you in {channelName}: {message[:20]}"
                createAddNotification(channel_id, dm_id, notiMessage, mem)
                return

def getHandleFromId(u_id):
    for user in database.data["accData"]:
        if user["id"] == u_id:
            return user["handle"]
    raise AccessError(description="User does not exist")

def getDmNameFromId(dm_id):
    for dm in database.data["dmList"]:
        if dm["id"] == dm_id:
            return dm["dm_name"]
    raise AccessError(description="Dm room does not exist")

def getChannelNameFromId(channel_id):
    for channel in database.data["channelList"]:
        if channel["id"] == channel_id:
            return channel["name"]
    raise AccessError(description="Channel room does not exist")

def createImageName():
    # Create imageName
    lowercase = string.ascii_lowercase
    pImageName = ("".join(random.choice(lowercase) for _ in range(5)))

    return pImageName

def check_reset_code(reset_code):
    status = False
    for resetData in database.data["resetdataList"]:
        if reset_code == resetData["reset_code"]:
            status = True
    return status

def find_reset_email(reset_code):
    for resetData in database.data["resetdataList"]:
        if reset_code == resetData["reset_code"]:
            reset_email = resetData["email"]
    return reset_email


# Helper Functions for message send later channel
def message_send_sendlater_channel(token, channel_id, message, message_id):
    u_id = get_user_id_from_token(token)
   
    checkTags(u_id, message, channel_id, -1)

    final_time = int(datetime.timestamp(datetime.now()))

    react_dictionary = [{
        "react_id": 1,
        "u_ids": [],
        "is_this_user_reacted": False,
    }]
    
    message_final = {
        'message': message,
        'message_id': message_id,
        'u_id': u_id,
        'time_created': final_time,
        "reacts": react_dictionary,
        "is_pinned": False,
    }

    for right_channel in database.data["channelList"]:
        if right_channel["id"] is channel_id:
            right_channel['messages'].append(message_final)
    
    return {}

# Helper function for message send later DM
def message_send_sendlater_dm(token, dm_id, message, message_id):
    u_id = get_user_id_from_token(token)

    checkTags(u_id, message, -1, dm_id)

    final_time = int(datetime.timestamp(datetime.now()))

    react_dictionary = [{
        "react_id": 1,
        "u_ids": [],
        "is_this_user_reacted": False
    }]

    message_final = {
        'message': message,
        'message_id': message_id,
        'u_id': u_id,
        'time_created': final_time,
        "reacts": react_dictionary,
        "is_pinned": False,
    }

    for right_dm in database.data["dmList"]:
        if right_dm["id"] is dm_id:
            right_dm['messages'].append(message_final)
    
    return {}