import src.config as config
import requests
import json
import urllib
import jwt

def test_http_notifications_working():
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

    funcURL = "notifications/get/v1"
    inputData = {
        "token": userR["token"]
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)

    assert respD["notifications"] == []


def test_http_notifications_invalid_token():
    requests.delete(config.url + "clear/v1")

    invalidToken = jwt.encode({"sessionId": 7}, "test", algorithm="HS256")

    funcURL = "notifications/get/v1"
    inputData = {
        "token": invalidToken
    }
    qData = urllib.parse.urlencode(inputData)
    rawResponseData = requests.get(config.url + funcURL + "?" + qData)
    respD = json.loads(rawResponseData.text)

    assert respD["code"] == 403