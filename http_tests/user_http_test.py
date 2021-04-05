import pytest
import requests
import json
import jwt
import urllib
import src.database as database
from src import config
from src.other import clear_v1

# ------------------------------------------------------------------------------
# USER PROFILE TEST FUNCTIONS

def test_http_user_profile_working():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    u_id = respD["auth_user_id"]
    # ----------------------------

    funcURL = "user/profile/v2"
    inputData = {
        "token": jwtToken,
        "u_id": u_id
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)
    expectedOutput = {
        'u_id': u_id,
        'email': "test@hotmail.com",
        'name_first': "nameFirst",
        'name_last': "nameLast",
        'handle_str': "namefirstnamelast",
    }
    assert respD == expectedOutput

def test_http_user_profile_v2_nonexistant_user():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    funcURL = "user/profile/v2"
    inputData = {
        "token": jwtToken,
        "u_id": 999
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# USER PROFILE SETNAME TEST FUNCTIONS

def test_user_profile_setname_working():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    u_id = respD["auth_user_id"]
    # ----------------------------

    # Set name -------------------
    funcURL = "user/profile/setname/v2"
    inputData = {
        "token": jwtToken,
        "name_first": "newFirst",
        "name_last": "newLast",
    }
    _ = requests.put(config.url + funcURL, json=inputData)
    # ----------------------------

    # Profile --------------------
    funcURL = "user/profile/v2"
    inputData = {
        "token": jwtToken,
        "u_id": u_id
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)
    expectedOutput = {
        'u_id': u_id,
        'email': "test@hotmail.com",
        'name_first': "newFirst",
        'name_last': "newLast",
        'handle_str': "namefirstnamelast",
    }

    assert respD == expectedOutput
    # ----------------------------
def test_http_user_profile_setname_short_first():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set name -------------------
    funcURL = "user/profile/setname/v2"
    inputData = {
        "token": jwtToken,
        "name_first": "",
        "name_last": "newLast",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_setname_short_last():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set name -------------------
    funcURL = "user/profile/setname/v2"
    inputData = {
        "token": jwtToken,
        "name_first": "newFirst",
        "name_last": "",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_setname_long_first():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set name -------------------
    funcURL = "user/profile/setname/v2"
    inputData = {
        "token": jwtToken,
        "name_first": "newFirst" * 15,
        "name_last": "newLast",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_setname_long_last():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set name -------------------
    funcURL = "user/profile/setname/v2"
    inputData = {
        "token": jwtToken,
        "name_first": "newFirst",
        "name_last": "newLast" * 15,
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

# ------------------------------------------------------------------------------
#  USER PROFILE SET EMAIL FUNCTION TESTS

def test_http_user_profile_setemail_working():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    u_id = respD["auth_user_id"]
    # ----------------------------

    # Set email-------------------
    funcURL = "user/profile/setemail/v2"
    inputData = {
        "token": jwtToken,
        "email": "newEmail@hotmail.com",
    }
    _ = requests.put(config.url + funcURL, json=inputData)
    # ----------------------------

    # Profile --------------------
    funcURL = "user/profile/v2"
    inputData = {
        "token": jwtToken,
        "u_id": u_id
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)
    expectedOutput = {
        'u_id': u_id,
        'email': "newEmail@hotmail.com",
        'name_first': "nameFirst",
        'name_last': "nameLast",
        'handle_str': "namefirstnamelast",
    }
    # ----------------------------

    assert respD == expectedOutput

def test_http_user_profile_setemail_invalid_email():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set email-------------------
    funcURL = "user/profile/setemail/v2"
    inputData = {
        "token": jwtToken,
        "email": "invalid@hotmail.com.au",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_setemail_email_taken():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password2",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set email-------------------
    funcURL = "user/profile/setemail/v2"
    inputData = {
        "token": jwtToken,
        "email": "test@hotmail.com",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

# ------------------------------------------------------------------------------
# USER PROFILE SET HANDLE FUNCTION TESTS

def test_http_user_profile_sethandle_working():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    u_id = respD["auth_user_id"]
    # ----------------------------

    # Set handle -----------------
    funcURL = "user/profile/sethandle/v1"
    inputData = {
        "token": jwtToken,
        "handle_str": "newHandle",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD == {}
    # ----------------------------

    # Profile --------------------
    funcURL = "user/profile/v2"
    inputData = {
        "token": jwtToken,
        "u_id": u_id
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)
    expectedOutput = {
        'u_id': u_id,
        'email': "test@hotmail.com",
        'name_first': "nameFirst",
        'name_last': "nameLast",
        'handle_str': "newHandle",
    }
    # ----------------------------

    assert respD == expectedOutput

def test_http_user_profile_sethandle_short_handle():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set handle -----------------
    funcURL = "user/profile/sethandle/v1"
    inputData = {
        "token": jwtToken,
        "handle_str": "",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_sethandle_long_handle():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set handle -----------------
    funcURL = "user/profile/sethandle/v1"
    inputData = {
        "token": jwtToken,
        "handle_str": "reallylonghandle" * 5,
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400

def test_http_user_profile_sethandle_handle_taken():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    _ = requests.post(config.url + funcURL, json=inputData)
    # ----------------------------

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password2",
        "name_first": "name2First",
        "name_last": "name2Last",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    # Set handle -----------------
    funcURL = "user/profile/sethandle/v1"
    inputData = {
        "token": jwtToken,
        "handle_str": "namefirstnamelast",
    }
    rawResponseData = requests.put(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    # ----------------------------

    assert respD["code"] == 400
# ------------------------------------------------------------------------------
# USERS ALL FUNCTION TESTS

def test_http_users_all_working():
    requests.delete(config.url + "clear/v1")
    
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    u_id1 = respD["auth_user_id"]
    # ----------------------------

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password2",
        "name_first": "name2First",
        "name_last": "name2Last",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    jwtToken = respD["token"]
    _ = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    u_id2 = respD["auth_user_id"]
    # ----------------------------

    funcURL = "users/all/v1"
    inputData = {
        "token": jwtToken,
    }
    qToken = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qToken)
    respD = json.loads(rawResponseData.text)
    expectedOutput = [
        {
            'u_id': u_id1,
            'email': "test@hotmail.com",
            'name_first': "nameFirst",
            'name_last': "nameLast",
            'handle_str': "namefirstnamelast",
        },
        {
            'u_id': u_id2,
            'email': "test2@hotmail.com",
            'name_first': "name2First",
            'name_last': "name2Last",
            'handle_str': "name2firstname2last",
        }
    ]

    assert respD == expectedOutput
 
# ------------------------------------------------------------------------------
