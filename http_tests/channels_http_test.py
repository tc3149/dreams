import pytest
import requests
import json
import jwt
import urllib
from src import config
from src.other import clear_v1
import src.database as database

# CHANNELS CREATE HTTP TESTING ###################

def test_http_channels_create_working():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------

    assert channelR["channel_id"] == 0

def test_http_channels_create_multiple():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "Channel2",
        "is_public": True,
    }
    channel2 = requests.post(config.url + funcURL, json=inputData)
    channel2R = json.loads(channel2.text)
    # ----------------------------

    assert channelR["channel_id"] == 0
    assert channel2R["channel_id"] == 1

def test_http_channels_create_invalid_token():

    requests.delete(config.url + "clear/v1")
    temp = jwt.encode({"sessionId": 7}, database.secretSauce, algorithm = "HS256")

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": temp,
        "name": "TestChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    assert channelR["code"] == 403
    # ----------------------------

def test_http_channels_create_longer_than_twenty_char():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "a" * 21,
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    assert channelR["code"] == 400