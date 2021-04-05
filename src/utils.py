import src.database as database
from src.error import InputError, AccessError
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
                return False
    return True

def getchannelID(message_id):

    for i in database.data["channelList"]:
        for message1 in i['messages']:
            if message1["message_id"] is message_id:
                channel_id1 = i.get("id")
                break
    return channel_id1

def checkOwner(auth_user_id, channel_id):

    for channel in database.data["channelList"]:
        if channel["id"] is channel_id:
            for users in channel["owner_ids"]:
                if users is auth_user_id:
                    return True

    return False

def search_email(email):
    for items in database.data["accData"]:
        if items["email"] == email:
            return True
    return False

def verify_password(email, password):
    for items in database.data["accData"]:
        if items["email"] == email:
            if items["password"] == password:
                return True
            else:
                return False

def search_handle(currUserHandle):
    for items in database.data["accData"]:
        if items["handle"] == currUserHandle:
            return True
    return False

def get_user_id(email):
    for items in database.data["accData"]:
        if items["email"] == email:
            userID = items["id"]
            return userID

def append_handle(currUserHandle):
    # Check number of users with same handle
    availableNumber = 0
    while True:
        testModCurrUserHandle = currUserHandle + str(availableNumber)
        if search_handle(testModCurrUserHandle):
            # Handle isnt avaiable, increment availableNumber
            availableNumber += 1
        else:
            # Handle is available, return number
            return testModCurrUserHandle

def create_handle(first, last):
    createUserHandle = first + last
    createUserHandle = createUserHandle.lower()
    createUserHandle = createUserHandle.replace("@", "")
    return createUserHandle

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
    tokenData = jwt.decode(token, database.secretSauce, algorithms="HS256")
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
    with open("serverDatabase.json", "w") as dataFile:
        dataFile.write(dumps(database.data))

def getUserAccData(u_id):
    for user in database.data["accData"]:
        if user["id"] == u_id:
            return user

def getUserProfileData(u_id):
    for user in database.data["userProfiles"]:
        if user["u_id"] == u_id:
            return user
