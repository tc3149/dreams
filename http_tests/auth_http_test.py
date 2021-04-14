import pytest
import requests
import json
import jwt
import src.database as database
from src import config
from src.other import clear_v1

# ------------------------------------------------------------------------------
# REGISTER TEST FUNCTIONS

def test_http_auth_register_working():
    requests.delete(config.url + "clear/v1")

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

def test_http_auth_register_already_registered_email():
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

def test_http_auth_register_invalid_email():
    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

def test_http_auth_register_short_first():
    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
        "name_first": "",
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

def test_http_auth_register_short_last():
    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

def test_http_auth_register_long_first():
    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
        "name_first": "nameFirst" * 15,
        "name_last": "nameLast",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

def test_http_auth_register_long_last():
    requests.delete(config.url + "clear/v1")

    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast" * 15,
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 400 

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LOGIN TEST FUNCTIONS

def test_http_auth_login_working():
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

    funcURL = "auth/login/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    expectedOutput = {
        "token": respD["token"],
        "auth_user_id": respD["auth_user_id"]
    }
    assert respD == expectedOutput

def test_http_auth_login_invalid_email():
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

    funcURL = "auth/login/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password1",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    testOutput = json.loads(rawResponseData.text)

    assert testOutput["code"] == 400

def test_http_auth_login_unregistered_email():
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

    funcURL = "auth/login/v2"
    inputData = {
        "email": "unregistered@hotmail.com",
        "password": "password1",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    testOutput = json.loads(rawResponseData.text)

    assert testOutput["code"] == 400

def test_http_auth_login_incorrect_password():
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

    funcURL = "auth/login/v2"
    inputData = {
        "email": "test@hotmail.com.au",
        "password": "password",
    }
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    testOutput = json.loads(rawResponseData.text)

    assert testOutput["code"] == 400

# ------------------------------------------------------------------------------
# LOGOUT TEST FUNCTIONS

def test_http_logout_working():
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
    token = jwt.decode(jwtToken, database.secretSauce, algorithms="HS256")
    # ----------------------------

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"sessionId": token["sessionId"]}, database.secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD == {
        "is_success": True
    }

def test_http_logout_invalid_token_key():
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

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"invalidKey": 6}, database.secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 403

def test_http_logout_invalid_token_value():
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

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"sessionId": "notAnInt"}, database.secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 403

def test_http_logout_invalid_token_type():
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

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"invalidKey": 9999}, database.secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 403

def test_http_logout_nonexistant_user():
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

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"sessionId": -99999}, database.secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 403

# ------------------------------------------------------------------------------
# RESET REQUEST TEST FUNCTIONS
def test_http_passwordreset_request_invalid_email():
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
    # Reset--------------------
    funcURL = "auth/passwordreset/request/v1"
    inputData = {
        "email": "invalidemail@hotmail.com",
    }
    rawResponseData  = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 400

# RESET REQUEST TEST FUNCTIONS
def test_http_passwordreset_reset_invalid_code():
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
    # Reset--------------------
    funcURL = "auth/passwordreset/reset/v1"
    inputData = {
        "reset_code": "invalidcode",
        "new_password": "newpassword",
    }
    rawResponseData  = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD["code"] == 400