import pytest
import requests
import json
import jwt
import time
import urllib
import src.database as database
from src import config

#STANDUP START TEST--------------------------------------

def test_http_standup_working():
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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)
    standupR = json.loads(standup.text)

    # If it is not none therefore a time has been generated for the standup
    # I.e. it is existing
    assert standupR != None

def test_http_standup_invalid():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)
    # Try to start a standup when there is already an active standup
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup2 = requests.post(config.url + funcURL, json=inputData)
    standup2R = json.loads(standup2.text)
    assert standup2R["code"] == 400

#STANDUP ACTIVE TEST--------------------------------------

def test_http_standup_active_working():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)

    # Standup Active
    funcURL = "standup/active/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
    }
    qData = urllib.parse.urlencode(inputData)
    standupActive = requests.get(config.url + funcURL + "?" + qData)
    standupActiveR = json.loads(standupActive.text)

    assert standupActiveR["is_active"] == True

def test_http_standup_active_invalid():

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

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)

    invalid_channelId = 500
    # Standup Active
    funcURL = "standup/active/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": invalid_channelId,
    }
    qData = urllib.parse.urlencode(inputData)
    standupActive = requests.get(config.url + funcURL + "?" + qData)
    standupActiveR = json.loads(standupActive.text)

    assert standupActiveR["code"] == 400

#STANDUP SEND TEST--------------------------------------

def test_http_standup_send_working():

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
        "name_first": "Hayden",
        "name_last": "Smith",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)
    standupR = json.loads(standup.text)

    # If it is not none therefore a time has been generated for the standup
    # I.e. it is existing

    # Message Send -------
    funcURL = "standup/send/v1"
    
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Hello World",
    }
    standupSend = requests.post(config.url + funcURL, json=inputData)
    standupSendR = json.loads(standupSend.text)

    # Message Send -------
    funcURL = "standup/send/v1"
    
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "message": "This is awesome",
    }
    standupSend2 = requests.post(config.url + funcURL, json=inputData)
    standupSend2R = json.loads(standupSend2.text)

    time.sleep(3)

    # Channel Message Info -------
    funcURL = "channel/messages/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    channelMessages = requests.get(config.url + funcURL + "?" + qData)
    channelMessagesR = json.loads(channelMessages.text)

    assert channelMessagesR["messages"][0]["message"] == "namefirstnamelast: Hello World\nnamefirstnamelast: This is awesome"

def test_http_standup_send_invalid():

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
        "name_first": "Hayden",
        "name_last": "Smith",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -------
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    join = requests.post(config.url + funcURL, json=inputData)

    # Start the standup in the channel
    # Standup Start -------
    funcURL = "standup/start/v1"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "length": 2,
    }
    standup = requests.post(config.url + funcURL, json=inputData)
    standupR = json.loads(standup.text)

    # If it is not none therefore a time has been generated for the standup
    # I.e. it is existing

    # Message Send -------
    funcURL = "standup/send/v1"
    
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "a" * 1001,
    }
    standupSend = requests.post(config.url + funcURL, json=inputData)
    standupSendR = json.loads(standupSend.text)

    assert standupSendR["code"] == 400



