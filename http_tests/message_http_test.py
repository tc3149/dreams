import pytest
import requests
import json
import jwt
import urllib
import src.database as database
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2
from src.message import message_send_v2, message_edit_v2, message_remove_v1
from src.message import message_senddm_v1, message_share_v1
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from datetime import datetime
from time import sleep

# MESSAGE_SEND TESTING

# Empty Message
def testsend_empty_message():
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

    # Message send
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": '',
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    assert messageSendR["code"] == 400


# Invalid Long Message
def testsend_invalid_long_msg():
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

    # Message send
    funcURL = "message/send/v2"
    temp = 'x' * 2000
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": temp,
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    assert messageSendR["code"] == 400

# Invalid Token
def testsend_invalid_token():
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

    # Message send
    funcURL = "message/send/v2"
    invalid_token = jwt.encode({"sessionId": 2954}, database.secretSauce, algorithm = "HS256")

    inputData = {
        "token": invalid_token,
        "channel_id": channelR["channel_id"],
        "message": "This is a message from Thomas Chen",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    assert messageSendR["code"] == 403

# Invalid Channel
def testsend_invalid_channel():
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
    _ = requests.post(config.url + funcURL, json=inputData)

    # Message send
    funcURL = "message/send/v2"
    
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_id",
        "message": "This is a message from Thomas Chen",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    assert messageSendR["code"] == 400

# Person not in channel but sends message
def testsend_sent_not_in_channel():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Message send
    funcURL = "message/send/v2"

    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "message": "This is a message from Thomas Chen",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    assert messageSendR["code"] == 403


# Working Test Case
def testsend_valid_case():
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
        "message": "lol",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)

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

    for msg in channelMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == "lol"
        assert msg["u_id"] == userR["auth_user_id"]   
        

# MESSAGE EDIT TESTING

# Invalid Long Message
def testedit_invalid_long_msg():
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

    # Message Send
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Edit
    funcURL = "message/edit/v2"
    temp = 'x' * 9999

    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "message": temp,
    }
    messageEdit = requests.put(config.url + funcURL, json=inputData)
    messageEditR = json.loads(messageEdit.text)
    assert messageEditR["code"] == 400
    

# Invalid Token
def testedit_invalid_token():
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

    # Message Send
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Edit
    funcURL = "message/edit/v2"
    invalid_token = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    inputData = {
        "token": invalid_token,
        "message_id": messageSendR["message_id"],
        "message": "Change this to Jonathan Qiu",
    }
    messageEdit = requests.put(config.url + funcURL, json=inputData)
    messageEditR = json.loads(messageEdit.text)
    assert messageEditR["code"] == 403

# Invalid Message ID
def testedit_invalid_mID():
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

    # Message Send --------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)
    
    # Message Edit ---------
    funcURL = "message/edit/v2"
    
    inputData = {
        "token": userR["token"],
        "message_id": "invalid_mID",
        "message": "Change this to Jonathan Qiu",
    }
    messageEdit = requests.put(config.url + funcURL, json=inputData)
    messageEditR = json.loads(messageEdit.text)
    assert messageEditR["code"] == 400

# Person editing is not OP/Owner
def testedit_not_authorised():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Message Send
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Edit
    funcURL = "message/edit/v2"

    inputData = {
        "token": user2R["token"],
        "message_id": messageSendR["message_id"],
        "message": "Change this to Jonathan Qiu",
    }

    messageEdit = requests.put(config.url + funcURL, json=inputData)
    messageEditR = json.loads(messageEdit.text)
    assert messageEditR["code"] == 403

# Valid Test Case
def testedit_valid_case():
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
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Edit ----------
    funcURL = "message/edit/v2"

    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "message": "Jonathan",
    }
    messageEdit = requests.put(config.url + funcURL, json=inputData)
    _ = json.loads(messageEdit.text)
    
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

    for msg in channelMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == "Jonathan"
        assert msg["u_id"] == userR["auth_user_id"]   


# A more comprehensive valid case
def testedit_comprehensive_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -----
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Edit ----------
    funcURL = "message/edit/v2"

    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "message": "Jonathan",
    }
    messageEdit = requests.put(config.url + funcURL, json=inputData)
    _ = json.loads(messageEdit.text)
    
    # Channel Message Info -------
    funcURL = "channel/messages/v2"

    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    channelMessages = requests.get(config.url + funcURL + "?" + qData)
    channelMessagesR = json.loads(channelMessages.text)

    for msg in channelMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == "Jonathan"
        assert msg["u_id"] == user2R["auth_user_id"]   


# MESSAGE REMOVE TESTING

# Invalid Token
def testremove_invalid_token_id():
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

    # Message Send ------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Remove ----
    funcURL = "message/remove/v1"
    invalid_token = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    inputData = {
        "token": invalid_token,
        "message_id": messageSendR["message_id"],
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    messageRemoveR = json.loads(messageRemove.text)
    assert messageRemoveR["code"] == 403


# Invalid Message ID
def testremove_invalid_mID():
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

    # Message Send ------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSend.text)
    
    # Message Remove ----
    funcURL = "message/remove/v1"
   
    inputData = {
        "token": userR["token"],
        "message_id": "invalid_id",
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    messageRemoveR = json.loads(messageRemove.text)
    assert messageRemoveR["code"] == 400

# Removing Empty
def testremove_empty():
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
    
    # Message Remove ----
    funcURL = "message/remove/v1"
   
    inputData = {
        "token": userR["token"],
        "message_id": "m_id",
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    messageRemoveR = json.loads(messageRemove.text)
    assert messageRemoveR["code"] == 400

# Not Authorised User Removing
def testremove_unauthorised():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -----
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Remove ----
    funcURL = "message/remove/v1"
   
    inputData = {
        "token": user2R["token"],
        "message_id": messageSendR["message_id"],
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    messageRemoveR = json.loads(messageRemove.text)
    assert messageRemoveR["code"] == 403

# Valid Case
def testeremove_valid():
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
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Remove ----
    funcURL = "message/remove/v1"
   
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    _ = json.loads(messageRemove.text)
    
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

    for msg in channelMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == ""
        assert msg["u_id"] == userR["auth_user_id"]   

# A comprehensive valid case
def testremove_comprehensive_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Channel Join -----
    funcURL = "channel/join/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
    }
    _ = requests.post(config.url + funcURL, json=inputData)

    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas Chen and Jonathan Qiu",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)
    
    # Message Remove ----
    funcURL = "message/remove/v1"
   
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messageRemove = requests.delete(config.url + funcURL, json=inputData)
    _ = json.loads(messageRemove.text)
    
    # Channel Message Info -------
    funcURL = "channel/messages/v2"

    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    channelMessages = requests.get(config.url + funcURL + "?" + qData)
    channelMessagesR = json.loads(channelMessages.text)

    for msg in channelMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == ""
        assert msg["u_id"] == user2R["auth_user_id"]   


# MESSAGE SENDDM TESTING

# Empty Message
def testsenddm_invalid_empty_message():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)
    assert messageSendDMR["code"] == 400


# Invalid Message
def testsenddm_invalid_long_msg():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    temp = 'x' * 2000
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": temp,
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)
    assert messageSendDMR["code"] == 400

# Invalid Token
def testsenddm_invalid_token_ID():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    invalid_token = jwt.encode({"sessionId": "notInt"}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": invalid_token,
        "dm_id": dmR["dm_id"],
        "message": "Jonathan Qiu is such a nice guy",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)
    assert messageSendDMR["code"] == 403

# Invalid DM ID
def testsenddm_invalid_dmID():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(dm.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": "invalid_dmID",
        "message": "Jonathan Qiu is such a nice guy",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)
    assert messageSendDMR["code"] == 400


# User Not in DM
def testsenddm_unauthorised_user():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Register Third Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user3R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jonathan Qiu is such a nice guy",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)
    assert messageSendDMR["code"] == 403

# Valid Test Case
def testsenddm_valid_case():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send DM -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jonathan Qiu is such a nice guy",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSendDM.text)

    # DM Message Info -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    for msg in dmMessagesR["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == "Jonathan Qiu is such a nice guy"
        assert msg["u_id"] == user2R["auth_user_id"]  


    # Message Send DM v2 -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Look at Thomas Chen, so inspirational",
    }
    messageSendDM2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSendDM2.text)

    # Channel Message Info v2 -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages2 = requests.get(config.url + funcURL + "?" + qData)
    dmMessages2R = json.loads(dmMessages2.text)


    for msg in dmMessages2R["messages"]:
        if msg["u_id"] is userR["auth_user_id"]:
            assert msg["message_id"] == 2
            assert msg["message"] == "Look at Thomas Chen, so inspirational"

# ##############################################################################################################
# MESSAGE/SHARE/V1 TESTS
def test_http_message_share_not_member_of_channel_sharing_to():
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
    _ = json.loads(user2.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    
    #checking message_share
    funcURL = "message/share/v1"
    invalidToken = jwt.encode({"sessionId": 8}, database.secretSauce, algorithm="HS256")
    inputData ={
        'token': invalidToken,
        'og_message_id': messageSendR["message_id"],
        'message': "",
        'channel_id': channelR['channel_id'],
        'dm_id': -1,
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR["code"] == 403

def test_http_message_share_not_member_of_dm_sharing_to():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
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
    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Hi",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    invalidToken = jwt.encode({"sessionId": 8}, database.secretSauce, algorithm="HS256")
    #checking message_share
    funcURL = "message/share/v1"
    inputData ={
        'token': invalidToken,
        'og_message_id': messageSendR["message_id"],
        'message': "",
        'channel_id': -1,
        'dm_id': dmR['dm_id'],
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR["code"] == 403

def test_http_message_share_Optional_message_channel():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
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
    _ = json.loads(user2.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Hi",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    
    #checking message_share
    funcURL = "message/share/v1"
    inputData ={
        'token': userR["token"],
        'og_message_id': messageSendR["message_id"],
        'message': "Hello",
        'channel_id': channelR['channel_id'],
        'dm_id': -1,
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR == {"shared_message_id": messageShareR["shared_message_id"]}

def test_http_message_share_no_optional_message():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
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
    _ = json.loads(user2.text)
    # ----------------------------
    # Creating Channel--------------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testChannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)
    # ----------------------------
    # Message Send -------
    funcURL = "message/send/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Hi",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    
    #checking message_share
    funcURL = "message/share/v1"
    inputData ={
        'token': userR["token"],
        'og_message_id': messageSendR["message_id"],
        'message': "",
        'channel_id': channelR['channel_id'],
        'dm_id': -1,
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR == {"shared_message_id": messageShareR["shared_message_id"]}

def test_http_message_share_optional_message_dm():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
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
    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Hi",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    
    #checking message_share
    funcURL = "message/share/v1"
    inputData ={
        'token': userR["token"],
        'og_message_id': messageSendR["message_id"],
        'message': "Hello",
        'channel_id': -1,
        'dm_id': dmR["dm_id"],
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR == {"shared_message_id": messageShareR["shared_message_id"]}

def test_http_message_share_no_optional_message_dm():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
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
    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Hi",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    
    #checking message_share
    funcURL = "message/share/v1"
    inputData ={
        'token': userR["token"],
        'og_message_id': messageSendR["message_id"],
        'message': "",
        'channel_id': -1,
        'dm_id': dmR["dm_id"],
    }
    messageShare = requests.post(config.url + funcURL, json=inputData)
    messageShareR = json.loads(messageShare.text)

    assert messageShareR == {"shared_message_id": messageShareR["shared_message_id"]}


# MESSAGE SENDLATER TESTING -----------------

# Message too long (1k+ characters)
def testsendlater_too_long():
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

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    temp = 'x' * 2354
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": temp,
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 400


# Invalid Token
def testsendlater_token_fail():
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

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    invalid_token = jwt.encode({"sessionId": 9949}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": invalid_token,
        "channel_id": channelR["channel_id"],
        "message": "Jonathan Chen and Thomas Qiu",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 403
    

# Invalid Channel ID
def testsendlater_invalid_channel_id():
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
    _ = json.loads(channel.text)

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "channel_id": "invalid_id",
        "message": "Jonathan Chen and Thomas Qiu",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 400


# Empty Message
def testsendlater_empty_msg():
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

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 400


# User not in channel
def testsendlater_user_not_in_channel():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Channel Create -------
    funcURL = "channels/create/v2"
    inputData = {
        "token": userR["token"],
        "name": "testchannel",
        "is_public": True,
    }
    channel = requests.post(config.url + funcURL, json=inputData)
    channelR = json.loads(channel.text)

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": user2R["token"],
        "channel_id": channelR["channel_id"],
        "message": "Jonathan Chen and Thomas Qiu",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 403


# Message sent in past
def testsendlater_past_time():
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

    # Message sendlater 
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) - 2)
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Chenergy",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterR = json.loads(messageSendlater.text)
    assert messageSendlaterR["code"] == 400


# Valid Case Testing
def testsendlater_valid():
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

    # Message sendlater
    funcURL = "message/sendlater/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "message": "Chenergy",
        "time_sent": time,
    }
    messageSendlater = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageSendlater.text)

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

    assert len(channelMessagesR["messages"]) == 0

    sleep(3)

    # Channel Message Info v2 -------
    funcURL = "channel/messages/v2"
    inputData = {
        "token": userR["token"],
        "channel_id": channelR["channel_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    channelMessages2 = requests.get(config.url + funcURL + "?" + qData)
    channelMessages2R = json.loads(channelMessages2.text)

    for msg in channelMessages2R["messages"]:
        if msg["u_id"] is userR["auth_user_id"]:
            assert msg["message"] == "Chenergy"
            assert msg["time_created"] == time


# MESSAGE SEND LATER DM TESTING --------------------------------

# Message too long (over 1k)
def testsendlaterdm_long_msg():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],  
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    temp = 'x' * 2583
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": temp,
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 400


# Invalid Token ID
def testsendlaterdm_wrong_token():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    invalid_token = jwt.encode({"sessionId": 545999}, database.secretSauce, algorithm = "HS256")
    inputData = {
        "token": invalid_token,
        "dm_id": dmR["dm_id"],
        "message": "Thomas' DLore",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 403


# Invalid dm ID
def testsendlaterdm_wrong_dm_ID():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "dm_id": "invalid_id",
        "message": "Thomas' DLore",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 400


# Empty Message
def testsendlaterdm_empty_msg():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 400


# User not in DM
def testsendlaterdm_user_not_found():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # Register Third Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    } 
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": user3R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Terry Crews",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 403


# Time set in past
def testsendlaterdm_past_time():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) - 2)
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)
    assert messageSendlaterdmR["code"] == 400


# Valid
def testsendlaterdm_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message sendlater
    funcURL = "message/sendlaterdm/v1"
    time = int(datetime.timestamp(datetime.now()) + 2)
    inputData = {
        "token": userR["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
        "time_sent": time,
    }
    messageSendlaterdm = requests.post(config.url + funcURL, json=inputData)
    messageSendlaterdmR = json.loads(messageSendlaterdm.text)

    # DM Message Info -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    assert len(dmMessagesR["messages"]) == 0

    sleep(3)

    # DM Message Info 2 -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages2 = requests.get(config.url + funcURL + "?" + qData)
    dmMessages2R = json.loads(dmMessages2.text)

    for dms in dmMessages2R["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["message"] == "Jake Perolta"
            assert dms["time_created"] == time
            assert dms["message_id"] == messageSendlaterdmR["message_id"]


# MESSAGE REACT TESTING --------------------------------------------------

# Message already reacted
def testreact_reacted_already():
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
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    # Message React ----
    funcURL = "message/react/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "react_id": 1,
    }
    messageReact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageReact.text)


    # Message React 2 ----
    funcURL = "message/react/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "react_id": 1,
    }
    messageReact2 = requests.post(config.url + funcURL, json=inputData)
    messageReact2R = json.loads(messageReact2.text)
    assert messageReact2R["code"] == 400


# Valid DM Message React
def testreact_dm_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)

    # Message React ----
    funcURL = "message/react/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
        "react_id": 1,
    }
    messageReact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageReact.text)

    # DM Message Info -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    for dms in dmMessagesR["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["reacts"] == [{
                "react_id": 1,
                "u_ids": [userR["auth_user_id"]],
                "is_this_user_reacted": True,
            }]


# MESSAGE UNREACT TESTING ----------------------------------------------

# Unreacting a message that has already been unreacted
def testunreact_unreacted_message():
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
        "message": "Thomas",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    # Message React ----
    funcURL = "message/react/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "react_id": 1,
    }
    messageReact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageReact.text)

    # Message Unreact -----
    funcURL = "message/unreact/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "react_id": 1,
    }
    messageUnreact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageUnreact.text)

    # Message Unreact 2 -----
    funcURL = "message/unreact/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
        "react_id": 1,
    }
    messageUnreact2 = requests.post(config.url + funcURL, json=inputData)
    messageUnreact2R = json.loads(messageUnreact2.text)
    assert messageUnreact2R["code"] == 400


# Valid DM Unreact
def testunreact_valid_dm():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)

    # Message React ----
    funcURL = "message/react/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
        "react_id": 1,
    }
    messageReact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageReact.text)

    # DM Message Info -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    for dms in dmMessagesR["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["reacts"] == [{
                "react_id": 1,
                "u_ids": [userR["auth_user_id"]],
                "is_this_user_reacted": True,
            }]

    # Message Unreact 2 -----
    funcURL = "message/unreact/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
        "react_id": 1,
    }
    messageUnreact = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageUnreact.text)

    # DM Message Info 2 -------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages2 = requests.get(config.url + funcURL + "?" + qData)
    dmMessages2R = json.loads(dmMessages2.text)

    for dms in dmMessages2R["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["reacts"] == [{
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": False,
            }]


# MESSAGE PIN TESTING --------------------------------------

# Message Already Pinned
def testpin_pinned_already():
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
        "message": "Amy Santiago",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    # Message Pin --------
    funcURL = "message/pin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messagePin = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messagePin.text)

    # Message Pin --------
    funcURL = "message/pin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messagePin2 = requests.post(config.url + funcURL, json=inputData)
    messagePin2R = json.loads(messagePin2.text)
    assert messagePin2R["code"] == 400


# Valid DM Test
def testpin_dm_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)

    # Message Pin --------
    funcURL = "message/pin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
    }
    messagePin = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messagePin.text)
    
    # DM Message Info -------
    funcURL = "dm/messages/v1"

    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    for dms in dmMessagesR["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["is_pinned"] == True


# MESSAGE UNPIN TESTING ----------------------------------------------
def testunpin_unpinned_already():
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
        "message": "Amy Santiago",
    }
    messageSend = requests.post(config.url + funcURL, json=inputData)
    messageSendR = json.loads(messageSend.text)

    # Message Pin --------
    funcURL = "message/pin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messagePin = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messagePin.text)

    # Message Unpin --------
    funcURL = "message/unpin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messageUnpin = requests.post(config.url + funcURL, json=inputData)
    messageUnpinR = json.loads(messageUnpin.text)

    # Message Unpin --------
    funcURL = "message/unpin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendR["message_id"],
    }
    messageUnpin = requests.post(config.url + funcURL, json=inputData)
    messageUnpinR = json.loads(messageUnpin.text)
    assert messageUnpinR["code"] == 400


# Valid Case for DM
def testunpin_dm_valid():
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

    # Register Second Person --------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)

    # DM Create -------
    funcURL = "dm/create/v1"
    userList = []
    userList.append(user2R["auth_user_id"])
    inputData = {
        "token": userR["token"],
        "u_ids": userList,
    }
    dm = requests.post(config.url + funcURL, json=inputData)
    dmR = json.loads(dm.text)

    # Message Send -------
    funcURL = "message/senddm/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "message": "Jake Perolta",
    }
    messageSendDM = requests.post(config.url + funcURL, json=inputData)
    messageSendDMR = json.loads(messageSendDM.text)

    # Message Pin --------
    funcURL = "message/pin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
    }
    messagePin = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messagePin.text)
    
    # DM Message Info -------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages = requests.get(config.url + funcURL + "?" + qData)
    dmMessagesR = json.loads(dmMessages.text)

    for dms in dmMessagesR["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["is_pinned"] == True


    # Message Unpin --------
    funcURL = "message/unpin/v1"
    inputData = {
        "token": userR["token"],
        "message_id": messageSendDMR["message_id"],
    }
    messageUnpin = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(messageUnpin.text)

    # DM Message Info -------
    funcURL = "dm/messages/v1"
    inputData = {
        "token": user2R["token"],
        "dm_id": dmR["dm_id"],
        "start": 0,
    }
    qData = urllib.parse.urlencode(inputData)
    dmMessages2 = requests.get(config.url + funcURL + "?" + qData)
    dmMessages2R = json.loads(dmMessages2.text)

    for dms in dmMessages2R["messages"]:
        if dms["u_id"] is user2R["auth_user_id"]:
            assert dms["is_pinned"] == False