import pytest
import re
from src.database import data
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.utils import saveData, get_user_id_from_token
from src.channels import channels_create_v2
from src.other import clear_v1, search_v1
from src.message import message_send_v2, message_senddm_v1
from src.dm import dm_create_v1, dm_messages_v1

# ------------------------------------------------------------------------------------------------------
#Other clear_v1() tests

def test_clear_register():

    clear_v1()
    auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    clear_v1()
    assert data == {'accData': [], 'channelList': [], 'message_ids': [], 'dmList': [], 'userProfiles': []}

def test_clear_channel():

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channels_create_v2(user1["token"], "testchannel", True)
    clear_v1()
    assert data == {'accData': [], 'channelList': [], 'message_ids': [], 'dmList': [], 'userProfiles': []}

def test_clear_dm():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]
    dm_create_v1(user["token"], id_list)
    clear_v1()
    assert data == {'accData': [], 'channelList': [], 'message_ids': [], 'dmList': [], 'userProfiles': []}

# ------------------------------------------------------------------------------------------------------
# Search_v1 tests

def test_search_single_channel():

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1["token"], "testchannel", True)
    message_send_v2(user1["token"], channel1["channel_id"], "testtest")
    user2 = auth_register_v2("user2@gmail.com", "password", "Firstname", "Lastname")
    channel2 = channels_create_v2(user2["token"], "channel2", True)
    message_send_v2(user2["token"], channel2["channel_id"], "testing")
    search = search_v1(user1["token"], "test")
    search_list = search["messages"]

    assert search_list[0].get('message_id') == 1
    assert search_list[0].get('message') == "testtest"
    assert search_list[0].get('u_id') == 0


def test_search_multiple_channel():

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1["token"], "testchannel", True)
    message_send_v2(user1["token"], channel1["channel_id"], "testtest")
    user2 = auth_register_v2("user2@gmail.com", "password", "Firstname", "Lastname")
    channel2 = channels_create_v2(user2["token"], "channel2", True)
    message_send_v2(user2["token"], channel2["channel_id"], "testing")
    message_send_v2(user1["token"], channel1["channel_id"], "testtttt")
    search = search_v1(user1["token"], "test")
    search_list = search["messages"]

    assert search_list[0].get('message_id') == 1
    assert search_list[0].get('message') == "testtest"
    assert search_list[0].get('u_id') == 0

    assert search_list[1].get('message_id') == 3
    assert search_list[1].get('message') == "testtttt"
    assert search_list[1].get('u_id') == 0

def test_search_single_dm():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])
    message_senddm_v1(user2["token"], dm["dm_id"], "TestingDmFirst")
    message_senddm_v1(user2["token"], dm["dm_id"], "Shouldnt Match")
    dm_messages_v1(user2["token"], dm["dm_id"], 0)
    message_senddm_v1(user["token"], dm["dm_id"], "TestingDmSecond")
    dm_messages_v1(user["token"], dm["dm_id"], 0)
    search = search_v1(user["token"], "Shouldnt")
    search_list = search["messages"]

    assert search_list[0].get('message_id') == 2
    assert search_list[0].get('message') == "Shouldnt Match"
    assert search_list[0].get('u_id') == 1

def test_search_multiple_dm():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])
    message_senddm_v1(user2["token"], dm["dm_id"], "TestingDmFirst")
    message_senddm_v1(user2["token"], dm["dm_id"], "Shouldnt Match")
    dm_messages_v1(user2["token"], dm["dm_id"], 0)
    message_senddm_v1(user["token"], dm["dm_id"], "TestingDmSecond")
    dm_messages_v1(user["token"], dm["dm_id"], 0)
    search = search_v1(user["token"], "Test")
    search_list = search["messages"]

    assert search_list[0].get('message_id') == 1
    assert search_list[0].get('message') == "TestingDmFirst"
    assert search_list[0].get('u_id') == 1

    assert search_list[1].get('message_id') == 3
    assert search_list[1].get('message') == "TestingDmSecond"
    assert search_list[1].get('u_id') == 0

def test_search_thousand_char():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        search_v1(user["token"], "a" * 1001)

def test_search_dm_and_channel():

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1["token"], "testchannel", True)
    message_send_v2(user1["token"], channel1["channel_id"], "testtest")
    user2 = auth_register_v2("user2@gmail.com", "password", "Firstname", "Lastname")
    channel2 = channels_create_v2(user2["token"], "channel2", True)
    message_send_v2(user2["token"], channel2["channel_id"], "testing")
    message_send_v2(user1["token"], channel1["channel_id"], "testtttt")

    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    message_senddm_v1(user2["token"], dm["dm_id"], "testingDmFirst")
    message_senddm_v1(user2["token"], dm["dm_id"], "Shouldnt Match")
    dm_messages_v1(user2["token"], dm["dm_id"], 0)
    message_senddm_v1(user1["token"], dm["dm_id"], "testingDmSecond")
    dm_messages_v1(user1["token"], dm["dm_id"], 0)

    search = search_v1(user1["token"], "test")
    search_list = search["messages"]
    
    assert search_list[0].get('message_id') == 1
    assert search_list[0].get('message') == "testtest"
    assert search_list[0].get('u_id') == 0

    assert search_list[1].get('message_id') == 3
    assert search_list[1].get('message') == "testtttt"
    assert search_list[1].get('u_id') == 0

    assert search_list[2].get('message_id') == 4
    assert search_list[2].get('message') == "testingDmFirst"
    assert search_list[2].get('u_id') == 1

    assert search_list[3].get('message_id') == 6
    assert search_list[3].get('message') == "testingDmSecond"
    assert search_list[3].get('u_id') == 0
