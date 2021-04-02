import pytest
import requests
import json
import jwt
from src.database import data, secretSauce
from src import config
from src.other import clear_v1
from src.auth import auth_logout_v1

def test_http_auth_register():
    clear_v1()

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

def test_http_auth_login():
    clear_v1()

    funcURL = "auth/login/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
    }
    rawTestOutput = requests.post(config.url + funcURL, json=inputData)
    testOutput = json.loads(rawTestOutput.text)
    expectedOutput = {
        "token": testOutput["token"],
        "auth_user_id": testOutput["auth_user_id"]
    }
    assert testOutput == expectedOutput

def test_http_logout():
    clear_v1()

    funcURL = "auth/logout/v1"
    inputData = jwt.encode({"sessionId": 1}, secretSauce, algorithm="HS256")
    rawResponseData = requests.post(config.url + funcURL, json=inputData)
    respD = json.loads(rawResponseData.text)
    assert respD == {
        "is_success": True
    }

if __name__ == "__main__":
    test_http_auth_register()
    test_http_auth_register()