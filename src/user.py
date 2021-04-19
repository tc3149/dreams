import os
from src.error import InputError, AccessError
import src.config as config
import src.database as database
from flask import request
from src.utils import get_user_id_from_token, search_email, createImageName, getUserProfileData
from datetime import datetime
from PIL import Image
import urllib.request
from src.utils import search_handle, search_user
from json import loads
import re

'''
Arguments:
    token (string)         - jwt encrypted session id
    u_id (int)             - user id

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type
    InputError  - Occurs when given u_id is not a valid user

Return Value:
    Dictionary of this format = {
        'u_id': u_id,                                                      - user id (int)
        'email': database.data["userProfiles"][u_id]["email"],             - user email (string)
        'name_first': database.data["userProfiles"][u_id]["name_first"],   - user first name (string)
        'name_last': database.data["userProfiles"][u_id]["name_last"],     - user last name (string)
        'handle_str': database.data["userProfiles"][u_id]["handle_str"],   - user handle (string)
    }
'''
def user_profile_v2(token, u_id):
    _ = get_user_id_from_token(token)

    if search_user(u_id):
        for user in database.data["userProfiles"]:
            if user["u_id"] == u_id:
                return {"user": user}
    else:
        raise InputError(description="User does not exist")


'''
Arguments:
    token (string)      - jwt encrypted session id
    name_first (string) - new first name to set to
    name_last (string)  - new last name to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type

Return Value:
    {}  - empty dictionary
'''
def user_profile_setname_v2(token, name_first, name_last):
    userId = get_user_id_from_token(token)
    
    if len(name_first) < 1 or len(name_last) < 1:
        # Error
        raise InputError(description="Error: First and/or last name is less than 1 character")
    if len(name_first) > 50 or len(name_last) > 50:
        # Error
        raise InputError(description="Error: First and/or last name is more than 50 characters")
    
    for user in database.data["accData"]:
        if user["id"] == userId:
            user["name_first"] = name_first
            user["name_last"] = name_last
    for user in database.data["userProfiles"]:
        if user["u_id"] == userId:
            user["name_first"] = name_first
            user["name_last"] = name_last

    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id
    email (string)      - new email string to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type
    InputError  - Email already in use by someone else
    InputError  - Invalid email regex

Return Value:
    {}  - empty dictionary
'''
def user_profile_setemail_v2(token, email):
    userId = get_user_id_from_token(token)

    isValidEmail = bool(re.match("^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$", email))
    if isValidEmail:
        if not search_email(email):
            for user in database.data["accData"]:
                if user["id"] == userId:
                    user["email"] = email
            for user in database.data["userProfiles"]:
                if user["u_id"] == userId:
                    user["email"] = email
        else:
            raise InputError(description="Email already in use")
    else:
        raise InputError(description="Email entered is not a valid email")
    
    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id
    handle_str (string) - new handle name to set to

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type
    InputError  - Handle is taken by someone else
    InputError  - New handle is not within the given constraints

Return Value:
    {}  - empty dictionary
'''
def user_profile_sethandle_v1(token, handle_str):
    userId = get_user_id_from_token(token)

    if len(handle_str) > 20:
        raise InputError(description="Handle is not allowed to be longer than 20 characters")
    if len(handle_str) < 3:
        raise InputError(description="Handle is not allowed to be shorter than 3 characters")

    if not search_handle(handle_str):
        for user in database.data["accData"]:
            if user["id"] == userId:
                user["handle"] = handle_str
        for user in database.data["userProfiles"]:
            if user["u_id"] == userId:
                user["handle_str"] = handle_str
    else:
        raise InputError(description="Handle is taken by another user")

    return {}

'''
Arguments:
    token (string)      - jwt encrypted session id

Exceptions:
    AccessError - Occurs when value does not exist in database
    AccessError - Occurs when token value is invalid data type
    AccessError - Occurs when token is invalid data type

Return Value:
    List of dictionarys of the following format = {
        'u_id': u_id,                                                      - user id (int)
        'email': database.data["userProfiles"][u_id]["email"],             - user email (string)
        'name_first': database.data["userProfiles"][u_id]["name_first"],   - user first name (string)
        'name_last': database.data["userProfiles"][u_id]["name_last"],     - user last name (string)
        'handle_str': database.data["userProfiles"][u_id]["handle_str"],   - user handle (string)
    }
'''
def users_all_v1(token):
    _ = get_user_id_from_token(token)
    
    return {"users": database.data["userProfiles"]}


'''
Arguments:
    token (string)      - jwt encrypted session id
    img_url (string)    - url of jpg image to be used for user profile photo
    x_start (int)       - x axis starting crop
    y_start (int)       - y axis starting crop
    x_end (int)         - x axis ending crop
    y_end (int)         - y axis ending crop

Exceptions:
    InputError - Occurs when img_url does not return success
    InputError - Occurs when cropping dimensins are out of image bounds
    InputError - Occurs when image is not a jpg

Return Value:
    {}  - empty dictionary
'''
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    userId = get_user_id_from_token(token)
    user = getUserProfileData(userId)

    imageName = createImageName()
    while imageName == user["profile_img_url"][-9:]:
        imageName = createImageName()
    
    respCode = urllib.request.urlopen(img_url)
    if respCode.getcode() != 200:
        print(respCode)
        raise InputError(description="URL did not return a success")
    _ = urllib.request.urlretrieve(img_url, f"src/static/{imageName}.jpg")
    imageObject = Image.open(f"src/static/{imageName}.jpg")
    imageW, imageH = imageObject.size
    imageType = imageObject.format
    if imageType != "JPEG":
        print(imageType)
        raise InputError(description="Image is not of type JPEG")
    if (x_start not in range(0, imageW + 1) or x_end not in range(0, imageW + 1)) or (
            y_start not in range(0, imageH + 1) or y_end not in range(0, imageH + 1)):
        raise InputError(description="Dimesions are not within image bounds")
    croppedImage = imageObject.crop((x_start, y_start, x_end, y_end))
    croppedImage.save(f"src/static/{imageName}.jpg")

    if user["profile_img_url"][-11:] != "default.jpg":
        pImageName = user["profile_img_url"][-9:]
        os.remove(f"src/static/{pImageName}")
    user["profile_img_url"] = f"{config.url}static/{imageName}.jpg"


    return {}



'''
Arguments:
    token (string)      - jwt encrypted session id

Exceptions:
    N/A

Return Value:
    {user_stats}  - Dictionary of shape {
                     channels_joined: [{num_channels_joined, time_stamp}],
                     dms_joined: [{num_dms_joined, time_stamp}], 
                     messages_sent: [{num_messages_sent, time_stamp}], 
                     involvement_rate 
                    }
'''
def user_stats_v1(token):
    userId = get_user_id_from_token(token)
    funcCallDatetime = int(datetime.timestamp(datetime.now()))

    numChannels = 0
    if database.data["channelList"]:
        for channel in database.data["channelList"]:
            if userId in channel["member_ids"]:
                numChannels += 1

    numDms = 0
    if database.data["dmList"]:
        for dm in database.data["dmList"]:
            if userId in dm["member_ids"]:
                numDms +=1

    numMessages = 0
    if database.data["channelList"]:
        for channel in database.data["channelList"]:
            if channel["messages"]:
                for message in channel["messages"]:
                    if message["u_id"] == userId:
                        numMessages += 1
    
    if database.data["dmList"]:
        for dm in database.data["dmList"]:
            if dm["messages"]:
                for message in dm["messages"]:
                    if message["u_id"] == userId:
                        numMessages += 1

    numerator = numChannels + numDms + numMessages
    totalChannels = 0 if not len(database.data["channelList"]) else len(database.data["channelList"])
    totalDms = 0 if not len(database.data["dmList"]) else len(database.data["dmList"])
    totalMessages = 0 if not len(database.data["message_ids"]) else len(database.data["message_ids"])
    denominator = totalChannels + totalDms + totalMessages

    
    involvementRate = 0 if denominator == 0 else numerator/denominator

    channels_joined = {
        "num_channels_joined": numChannels,
        "time_stamp": funcCallDatetime,
    }

    dms_joined = {
        "num_dms_joined": numDms,
        "time_stamp": funcCallDatetime,
    }

    messages_sent = {
        "num_messages_sent": numMessages,
        "time_stamp": funcCallDatetime,
    }
    database.userAnalytics["channels_joined"].append(channels_joined)
    database.userAnalytics["dms_joined"].append(dms_joined)
    database.userAnalytics["messages_sent"].append(messages_sent)
    database.userAnalytics["involvement_rate"] = involvementRate

    return {
        "user_stats": database.userAnalytics
    }



'''
Arguments:
    token (string)      - jwt encrypted session id

Exceptions:
    N/A

Return Value:
    {dreams_stats}  - Dictionary of shape {
                     channels_exist: [{num_channels_exist, time_stamp}], 
                     dms_exist: [{num_dms_exist, time_stamp}], 
                     messages_exist: [{num_messages_exist, time_stamp}], 
                     utilization_rate 
                    }
'''
def users_stats_v1(token):
    funcCallDatetime = int(datetime.timestamp(datetime.now()))

    numUsers = 0
    for user in database.data["accData"]:
        userJoined = False
        if not userJoined and database.data["channelList"]:
            for channel in database.data["channelList"]:
                if user["id"] in channel["member_ids"]:
                    userJoined = True
        if not userJoined and database.data["dmList"]:
            for dm in database.data["dmList"]:
                if user["id"] in dm["member_ids"]:
                    userJoined = True
        if userJoined is True:
            numUsers += 1

    numerator = numUsers
    denominator = 0 if not len(database.data["accData"]) else len(database.data["accData"]) 
    utilisationRate = 0 if denominator == 0 else numerator/denominator
    numChannels = 0 if not len(database.data["channelList"]) else len(database.data["channelList"])
    numDms = 0 if not len(database.data["dmList"]) else len(database.data["dmList"])
    numMessages = 0 if not len(database.data["message_ids"]) else len(database.data["message_ids"])

    channels_exist = {
        "num_channels_exist": numChannels,
        "time_stamp": funcCallDatetime,
    }
    dms_exist = {
        "num_dms_exist": numDms, 
        "time_stamp": funcCallDatetime,
    }
    messages_exist = {
        "num_messages_exist": numMessages, 
        "time_stamp": funcCallDatetime,
    }
    database.dreamsAnalytics["channels_exist"].append(channels_exist)
    database.dreamsAnalytics["dms_exist"].append(dms_exist)
    database.dreamsAnalytics["messages_exist"].append(messages_exist)
    database.dreamsAnalytics["utilization_rate"] = utilisationRate

    return {
        "dreams_stats": database.dreamsAnalytics
    }