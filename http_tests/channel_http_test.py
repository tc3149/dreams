import pytest
import requests
import json
import jwt
import urllib
from src.database import data, secretSauce
from src import config
from src.utils import checkOwner
from src.other import clear_v1

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
    print(json.loads(_.text))
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