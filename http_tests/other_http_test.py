import pytest
import requests
import json
import jwt
import urllib
import src.database as database
from src import config
from src.other import clear_v1


# CLEAR TEST #####################################################

def test_http_clear_working():

    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    requests.delete(config.url + "clear/v1")

    # If clear works properly we can register again without email already registered**
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text) 

    assert respD == {
        "token": respD["token"], 
        "auth_user_id": respD["auth_user_id"]
    }


def test_http_clear_channel():

    requests.delete(config.url + "clear/v1")

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
        "is_public": True,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    requests.delete(config.url + "clear/v1")

    assert database.data == {
        "accData": [],
        "channelList": [],
        "message_ids": [],
        "dmList": [],
        "userProfiles": [],
    }

def test_http_clear_dm():

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

    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    assert dmR == {
        'dm_id': 0,
        'dm_name': "namefirstnamelast,namefirstnamelast0"
    }

    requests.delete(config.url + "clear/v1")

    assert database.data == {
        "accData": [],
        "channelList": [],
        "message_ids": [],
        "dmList": [],
        "userProfiles": [],
    }

# SEARCH TEST #################################################

def test_search_working():

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
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Hello Guys",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Hello World",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Should not be seen in search",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)

    # Search
    funcURL = "search/v2"
    inputData = {
        "token": userR["token"],
        "query_str": "Hello",
    }
    qData = urllib.parse.urlencode(inputData)
    searchx = requests.get(config.url + funcURL + "?" + qData)
    searchxR = json.loads(searchx.text)
    search_list = searchxR["messages"]

    assert search_list[0].get("message_id") == 1
    assert search_list[0].get('message') == "Hello Guys"
    assert search_list[1].get('message') == "Hello World"
    
def test_search_invalid_token():

    requests.delete(config.url + "clear/v1")
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")

    # Search
    funcURL = "search/v2"
    inputData = {
        "token": temp,
        "query_str": "Hello",
    }
    qData = urllib.parse.urlencode(inputData)
    searchx = requests.get(config.url + funcURL + "?" + qData)
    searchxR = json.loads(searchx.text)
    assert searchxR["code"] == 403