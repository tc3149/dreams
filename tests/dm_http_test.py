import pytest
import requests
import json
import jwt
import urllib
from src.database import data, secretSauce
from src import config
from src.other import clear_v1

#DM LEAVE TEST---------------------------------------------------------------------------------------------------------
def test_http_dm_leave_working():
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

    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # Leaving DM-----------------
    funcURL = "dm/leave/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Listing DM's the user is part of
    funcURL = "dm/list/v1"
    inputData = {
            "token": user2R["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    assert dmListR == {'dms': []}

def test_http_dm_leave_invalid_dm():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Leaving DM-----------------
    funcURL = "dm/leave/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": "invalid_dm_id",
    }
    dmLeft = requests.post(config.url + funcURL, json=inputData)
    dmLeftR = json.loads(dmLeft.text)
    assert dmLeftR["code"] == 400
    # ----------------------------

def test_http_dm_leave_unauthorized_user():
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
     # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)
    # ----------------------------
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Leaving DM-----------------
    funcURL = "dm/leave/v1"
    inputData = {
        "token": user3R["token"],
        "dm_id": dmR["dm_id"],
    }
    dmLeft = requests.post(config.url + funcURL, json=inputData)
    dmLeftR = json.loads(dmLeft.text)
    assert dmLeftR["code"] == 403
    # ----------------------------

def test_http_dm_leave_invalid_token():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    temp = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")
    # Leaving DM-----------------
    funcURL = "dm/leave/v1"
    inputData = {
        "token": temp,
        "dm_id": dmR["dm_id"],
    }
    dmLeft = requests.post(config.url + funcURL, json=inputData)
    dmLeftR = json.loads(dmLeft.text)
    assert dmLeftR["code"] == 403
    # ----------------------------

#DM REMOVE TEST---------------------------------------------------------------------------------------------------
def test_http_dm_remove_working():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Removing DM-----------------
    funcURL = "dm/remove/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
    }
    _ = requests.delete(config.url + funcURL, json=inputData)
    # ----------------------------
    # Listing DM's the user is part of
    funcURL = "dm/list/v1"

    inputData = {
            "token": userR["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    assert dmListR == {'dms': []}

    inputData = {
            "token": user2R["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    assert dmListR == {'dms': []}

def test_http_dm_remove_invalid_id():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Removing DM-----------------
    funcURL = "dm/remove/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": "invalid_dm_id",
    }
    dmRemoved = requests.delete(config.url + funcURL, json=inputData)
    dmRemovedR = json.loads(dmRemoved.text)
    assert dmRemovedR["code"] == 400
    # ----------------------------

def test_http_dm_remove_not_owner():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Removing DM-----------------
    funcURL = "dm/remove/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
    }
    dmRemoved = requests.delete(config.url + funcURL, json=inputData)
    dmRemovedR = json.loads(dmRemoved.text)
    assert dmRemovedR["code"] == 403
    # ----------------------------

def test_http_dm_remove_invalid_token():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    temp = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")
    # Removing DM-----------------
    funcURL = "dm/remove/v1"
    inputData = {
        "token": temp,
        "dm_id": dmR["dm_id"],
    }
    dmRemoved = requests.delete(config.url + funcURL, json=inputData)
    dmRemovedR = json.loads(dmRemoved.text)
    assert dmRemovedR["code"] == 403
    # ----------------------------
#DM MESSAGES TEST---------------------------------------------------------------------------------------------------------
def test_http_dm_message_working():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR == {'messages': [], 'start': 0, 'end': -1}
    # ----------------------------

def test_http_dm_message_invalid_user():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    temp = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": temp,
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR["code"] == 403
    # ----------------------------
def test_http_dm_message_invalid_dm():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": 999,
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR["code"] == 400
    # ----------------------------

def test_http_dm_message_unauthorised_user():
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
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)
    # ----------------------------
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": user3R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR["code"] == 403
    # ----------------------------

def test_http_dm_message_startgreater():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "start": 1,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR["code"] == 400
    # ----------------------------

def test_http_dm_message_endnegativeone():
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
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    # ----------------------------
    # Checking Messages-----------------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)
    assert dmMessagesR["end"] == -1
    # ----------------------------
