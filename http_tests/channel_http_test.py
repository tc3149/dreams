import pytest
import requests
import json
import jwt
import urllib
from src import config
from src.other import clear_v1
import src.database as database

# CHANNEL JOIN TESTING

# Invalid Channel ID
def testjoin_invalid_channelID():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_id",
    }
    join = requests.post(config.url + funcURL, json=inputData)
    joinR = json.loads(join.text)
    assert joinR["code"] == 400


# Invalid Token
def testjoin_invalid_tokenn():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    temp = jwt.encode({"sessionId": 2000}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": temp,
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    joinR = json.loads(join.text)
    assert joinR["code"] == 403


# User Already In
def testjoin_joined_already():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join.text)

    # Channel Join Error -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join2 = requests.post(config.url + funcURL, json=inputData)
    join2R = json.loads(join2.text)
    assert join2R["code"] == 403

# Accessing Private Channel
def testjoin_private_channel():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": False,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    joinR = json.loads(join.text)
    assert joinR["code"] == 403


# Joining Already Joined Channel
def testjoin_already_joined():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": False,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    joinR = json.loads(join.text)
    assert joinR["code"] == 403


# Valid Case
def testjoin_valid_case():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Register Third Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join (Second Person) -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join.text)

    # Channel Join (Third Person) -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user3R["token"],
        "channel_id": channelR["channel_id"],
    }
    join2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join2.text)

    # Channel Details
    funcURL = "channel/details/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
    }
    qData = urllib.parse.urlencode(inputData)
    channelDetails = requests.get(config.url + funcURL + "?" + qData)
    channelDetailsR = json.loads(channelDetails.text)

    assert channelDetailsR["all_members"] == [
                                            {
                                                'u_id': userR["auth_user_id"],
                                                'email': 'test@hotmail.com',
                                                'name_first': 'nameFirst',
                                                'name_last': 'nameLast',
                                                'handle_str': 'namefirstnamelast',
                                                
                                            },
                                            
                                            {
                                                'u_id': user2R["auth_user_id"],
                                                'email': 'test2@hotmail.com',
                                                'name_first': 'nameFirst',
                                                'name_last': 'nameLast',
                                                'handle_str': 'namefirstnamelast0',
                                                
                                            },

                                            {
                                                'u_id': user3R["auth_user_id"],
                                                'email': 'test3@hotmail.com',
                                                'name_first': 'nameFirst',
                                                'name_last': 'nameLast',
                                                'handle_str': 'namefirstnamelast1',
                                                
                                            }
                                        ]

# ADD OWNER TESTING

# Invalid Token
def testaddowner_invalid_tokenn():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Add Owner ------
    funcURL = "channel/addowner/v1"
    temp = jwt.encode({"sessionId": 243343}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": temp,
        "channel_id": channelR["channel_id"],
        "u_id": user2R["token"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 403


# Invalid u_ID
def testaddowner_invalid_uID():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Add Owner ------
    funcURL = "channel/addowner/v1"
    temp = jwt.encode({"sessionId": 243343}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": temp,
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 400


# Invalid Channel ID
def testaddowner_invalid_channelID():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(channel.text)

    # Add Owner ------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel",
        "u_id": user2R["auth_user_id"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 400


# Owner is already Owner
def testaddowner_already_owner():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(channel.text)

    # Add Owner ------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel",
        "u_id": userR["auth_user_id"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 400


# Non-Authorised User Adding Owners
def testaddowner_unauthorised_token():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Register Third Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join Person 2 -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join.text)

    # Channel Join Person 3 -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user3R["token"],
        "channel_id": channelR["channel_id"],
    }
    join2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join2.text)
 
    # Add Owner ------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user3R["auth_user_id"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 403


# Adding Owner To Someone Not In Channel
def testaddowner_not_in_channel():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Register Third Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join Person 2 -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join.text)
 
    # Add Owner ------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user3R["auth_user_id"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    addOwnerR = json.loads(addOwner.text)
    assert addOwnerR["code"] == 403


# Valid Test Case
def testaddowner_valid_case():
    requests.delete(config.url + "clear/v1")

    # Register --------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join Person 2 -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(join.text)
 
    # Add Owner ------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user2R["auth_user_id"],
    }
    addOwner = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(addOwner.text)

    # Channel Details
    funcURL = "channel/details/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
    }
    qData = urllib.parse.urlencode(inputData)
    channelDetails = requests.get(config.url + funcURL + "?" + qData)
    channelDetailsR = json.loads(channelDetails.text)

    assert channelDetailsR["owner_members"] == [
                                            {
                                                'u_id': userR["auth_user_id"],
                                                'email': 'test@hotmail.com',
                                                'name_first': 'nameFirst',
                                                'name_last': 'nameLast',
                                                'handle_str': 'namefirstnamelast',
                                                
                                            },
                                            
                                            {
                                                'u_id': user2R["auth_user_id"],
                                                'email': 'test2@hotmail.com',
                                                'name_first': 'nameFirst',
                                                'name_last': 'nameLast',
                                                'handle_str': 'namefirstnamelast0',
                                                
                                            }
                                            ]

#CHANNEL REMOVEOWNER TEST---------------------------------------------------------------------------------------------------------
def test_http_channel_removeowner_working():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
     # Channel Join Person 2 -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # Adding Owner--------------------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user2R["auth_user_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user2R["auth_user_id"],
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR == {}

def test_http_channel_removeowner_invalid_user():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Adding Owner--------------------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user2R["auth_user_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": "invalid_user",
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR["code"] == 400

def test_http_channel_removeowner_invalid_channel():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Adding Owner--------------------
    funcURL = "channel/addowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "u_id": user2R["auth_user_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel",
        "u_id": user2R["auth_user_id"],
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR["code"] == 400

def test_http_channel_removeowner_only_owner():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel",
        "u_id": userR["auth_user_id"],
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR["code"] == 400

def test_http_channel_removeowner_not_owner():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel",
        "u_id": user2R["auth_user_id"],
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR["code"] == 400
    # ----------------------------
def test_http_channel_removeowner_invalid_token():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Removing Owner--------------------
    funcURL = "channel/removeowner/v1"
    inputData = {
        "token": user2R["token"],
        "channel_id": "invalid_channel",
        "u_id": userR["auth_user_id"],
    }
    removeOwner = requests.post(config.url + funcURL, json=inputData)
    removeOwnerR = json.loads(removeOwner.text)
    assert removeOwnerR["code"] == 400
    # ----------------------------
#CHANNEL LEAVE TEST---------------------------------------------------------------------------------------------------------
def test_http_channel_leave_working():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Creating Channel--------------
    inputData = {
        "token": userR["token"],
        "name": "testChannel2",
        "is_public": True,
    }
    channel2 = requests.post(config.url + funcURL, json=inputData)
    channel2R = json.loads(channel2.text)
    # ----------------------------
    # Leaving Channel--------------
    funcURL = "channel/leave/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Listing Channel--------------
    funcURL = "channels/list/v2"
    inputData = {
        "token": userR["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    channelList = requests.get(config.url + funcURL + "?" + qData)
    channelListR = json.loads(channelList.text)
    assert channelListR == {'channels': [{'channel_id': channel2R.get("channel_id"), 'name': 'testChannel2'}]}
    # ----------------------------
def test_http_channel_leave_channel_valid():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Leaving Channel--------------
    funcURL = "channel/leave/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_channel_id"
    }
    channelLeave = requests.post(config.url + funcURL, json=inputData)
    channelLeaveR = json.loads(channelLeave.text)
    assert channelLeaveR["code"] == 400
    # ----------------------------

def test_http_channel_leave_user_valid():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Leaving Channel--------------
    funcURL = "channel/leave/v1"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"]
    }
    channelLeave = requests.post(config.url + funcURL, json=inputData)
    channelLeaveR = json.loads(channelLeave.text)
    assert channelLeaveR["code"] == 403
    # ----------------------------