import re
import pytest
import datetime
import threading
import time
import jwt
from src.other import clear_v1
import src.database as database
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_list_v2
from src.channel import channel_messages_v2, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, channel_join_v2
from src.utils import get_user_id_from_token, make_dm_name, valid_dmid, valid_userid, getUserProfileData
from src.error import InputError, AccessError
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1, standup_collection_send

# STANDUP START TESTING ---------------------------------------------------------

# Test 1: Invalid token
def test_standup_invalid_token():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    with pytest.raises(AccessError):
        standup_start_v1(invalid_id, channel["channel_id"], 1)

# Test 2: Standup already active yet calling for another one
def test_standup_already_active():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    with pytest.raises(InputError):
        standup_start_v1(user.get("token"), channel["channel_id"], 1)

# Test 3: User is not authorised to call standup
def test_standup_not_authorised():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "User2", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    with pytest.raises(AccessError):
        standup_start_v1(user2.get("token"), channel["channel_id"], 1)

# Test 4: Standup is properly working for one channel
def test_standup_working():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    auth_register_v2("email2@gmail.com", "password", "Hayden", "Smith")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup = standup_start_v1(user.get("token"), channel["channel_id"], 1)
    # The current time is not a strict value (changes), therefore to test if standup by
    # itself is working, ensure that there IS a time, i.e. not NONE
    assert standup != None

# Test 5: Standups in different channels. I.e. not only one standup can be called
# in entirety of Dreams
def test_standup_multiple():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Hayden", "Smith")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    channel2 = channels_create_v2(user2.get("token"), "Channel2", True)
    standup = standup_start_v1(user.get("token"), channel["channel_id"], 1)
    standup2 = standup_start_v1(user2.get("token"), channel2["channel_id"], 1)
    time.sleep(2)
    assert standup != None
    assert standup2 != None

# STANDUP ACTIVE TESTING ---------------------------------------------------------

def test_standup_active_invalid_token():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    with pytest.raises(AccessError):
        standup_active_v1(invalid_id, channel["channel_id"])

def test_standup_active_not_active():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)

    active = standup_active_v1(user["token"], channel["channel_id"])
    assert active["is_active"] == False
    assert active["time_finish"] == None

def test_standup_active_is_active():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    active = standup_active_v1(user["token"], channel["channel_id"])
    assert active["is_active"] == True
    assert active["time_finish"] != None


# STANDUP SEND TESTING ---------------------------------------------------------

def test_standup_send_invalid_token():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    with pytest.raises(AccessError):
        standup_send_v1(invalid_id, channel["channel_id"], "Hello")

def test_standup_send_invalid_channel():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    invalid_channel = 50
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), invalid_channel, "Hello")
        
def test_standup_send_thousand_char():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), channel["channel_id"], "a" * 1001)
        
def test_standup_send_not_authorised():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "User", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    with pytest.raises(AccessError):
        standup_send_v1(user2.get("token"), channel["channel_id"], "Hello")
        
def test_standup_send_no_active_standup():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), channel["channel_id"], "Hello")

def test_standup_send_working():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Hayden", "Smith")
    channel = channels_create_v2(user.get("token"), "testchannel", True)
    channel_join_v2(user2.get("token"), channel["channel_id"])
    standup_start_v1(user.get("token"), channel["channel_id"], 1)
    standup_send_v1(user.get("token"), channel["channel_id"], "Hello World")
    standup_send_v1(user2.get("token"), channel["channel_id"], "This is Awesome")
    time.sleep(2)

    msg0 = channel_messages_v2(user["token"], channel["channel_id"], 0)
    assert msg0["messages"][0]["message"] == 'namelastname: Hello World\nhaydensmith: This is Awesome'

