import pytest
import requests
import json
import jwt
from src.database import data, secretSauce
from src import config
from src.other import clear_v1

def test_http_auth_register_working1():
    #requests.delete(config.url + "clear/v1")

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