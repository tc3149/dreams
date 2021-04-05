import pytest
import requests
import json
import jwt
import urllib
import src.database as database
from src import config

#DM CREATE TEST---------------------------------------------------------------------------------------------------------
def test_http_dm_create_working():
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
    userList.append(userR["auth_user_id"])
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

def test_http_dm_create_invalid_user():
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
    userList.append(userR["auth_user_id"])
    userList.append(user2R["auth_user_id"])
    userList.append(7)
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    assert dmR["code"] == 400

def test_http_dm_create_invalid_token():
    requests.delete(config.url + "clear/v1")
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")

    funcURL = "dm/create/v1"
    inputData = {
        "token": temp,
        "u_ids": [],
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)
    assert dmR["code"] == 403

#DM INVITE TEST---------------------------------------------------------------------------------------------------------

def test_http_dm_invite_working():
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
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Inviting User 3 to DM-----------------
    funcURL = "dm/invite/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": 0,
        "u_id": 2
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # List the DMS that user 3 is in
    funcURL = "dm/list/v1"
    inputData = {
            "token": user3R["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    
    assert dmListR == {"dms": [{"dm_id": 0, "dm_name": "namefirstnamelast,namefirstnamelast0"}]}

def test_http_dm_invite_invalid_dmid():
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
    _ = requests.post(config.url + funcURL, json=inputData)

    # ----------------------------

    # Invite-----------------
    funcURL = "dm/invite/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": 0,
        "u_id": 1
    }
    dmInv = requests.post(config.url + funcURL, json=inputData)
    dmInvR = json.loads(dmInv.text)
    assert dmInvR["code"] == 400

def test_http_dm_invite_invalid_uid():
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
    _ = requests.post(config.url + funcURL, json=inputData)
    
    # Invite-----------------
    funcURL = "dm/invite/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": 0,
        "u_id": 8
    }
    dmInv = requests.post(config.url + funcURL, json=inputData)
    dmInvR = json.loads(dmInv.text)
    assert dmInvR["code"] == 400

def test_http_dm_inviter_not_in_dm():

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

     # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test4@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    user4R = json.loads(user3.text)
    # ----------------------------

    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    
    # Invite-----------------
    funcURL = "dm/invite/v1"
    inputData = {
        "token": user3R["token"],
        "dm_id": 0,
        "u_id": user4R["auth_user_id"]
    }
    dmInv = requests.post(config.url + funcURL, json=inputData)
    dmInvR = json.loads(dmInv.text)
    assert dmInvR["code"] == 403

#DM LIST TEST---------------------------------------------------------------------------------------------------------

def test_http_dm_list_working():
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
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Creating DM-----------------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user3R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Creating DM LIST---------------
    funcURL = "dm/list/v1"
    inputData = {
            "token": userR["token"],
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    assert dmListR == {"dms": [{"dm_id": 0, "dm_name": "namefirstnamelast,namefirstnamelast0"},
     {"dm_id": 1, "dm_name": "namefirstnamelast,namefirstnamelast1"}]}

def test_http_dm_list_invalid_token():
    requests.delete(config.url + "clear/v1")
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")

    funcURL = "dm/list/v1"
    inputData = {
            "token": temp,
    }
    qData = urllib.parse.urlencode(inputData)
    dmList = requests.get(config.url + funcURL + "?" + qData)
    dmListR = json.loads(dmList.text)
    assert dmListR["code"] == 403


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
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")
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
    temp = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
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
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")
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

# ----------------------------#DM DETAILS TESTS -----------------------------------------------------------------------------------------------------------

def test_http_dm_details_dm_does_not_exist():
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
    _ = json.loads(dm.text) 
    # ----------------------------
    # checking details -----------
    funcURL = "dm/details/v1"
    inputData = {
        "token": userR['token'],
        "dm_id": 1242134
    }
    qData = urllib.parse.urlencode(inputData)
    dmDetails = requests.get(config.url + funcURL + "?" + qData)
    dmDetails = json.loads(dmDetails.text)
    print (dmDetails)
    assert dmDetails["code"] == 400

def test_http_dm_details_user_not_member_of_dm():
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
    # ----------------------------------
    # Creating DM-----------------
    funcURL = "dm/create/v1"
    inputData = {
        "token": userR["token"],
        "u_ids": [user2R["auth_user_id"]],
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text) 
    # ---------------------------
    # checking details -----------
    funcURL = "dm/details/v1"
    inputData = {
        "token": user3R['token'],
        "dm_id": dmR["dm_id"]
    }
    qData = urllib.parse.urlencode(inputData)
    dmDetails = requests.get(config.url + funcURL + "?" + qData)
    dmDetailsR = json.loads(dmDetails.text)
    
    assert dmDetailsR["code"] == 403

def test_http_dm_details_valid():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
     # Creating DM-----------------
    funcURL = "dm/create/v1"
    inputData = {
        "token": userR["token"],
        "u_ids": [user2R["auth_user_id"]],
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text) 
    # ---------------------------
    # checking details -----------
    funcURL = "dm/details/v1"
    inputData = {
        "token": userR['token'],
        "dm_id": dmR["dm_id"]
    }
    qData = urllib.parse.urlencode(inputData)
    dmDetails = requests.get(config.url + funcURL + "?" + qData)
    dmDetailsR = json.loads(dmDetails.text)
    print(dmDetailsR)
    assert dmDetailsR == {
        'name': 'namelastname,namelastname0',
        'members': [
            {
                'u_id': userR["auth_user_id"],
                'email': 'email@gmail.com',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname',
                
            },
            {
                'u_id': user2R["auth_user_id"],
                'email': 'email2@gmail.com',
                'name_first': 'Name',
                'name_last': 'Lastname',
                'handle_str': 'namelastname0',   
            }
        ]
    }