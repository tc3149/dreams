import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.database import accData, channelList
import channels.py

# Channel 

def test_no_channels():
    clear_v1():
    user1 = auth_register_v1("gordonl1@gmail.com", "gordonisverygood", "Gordon", "Liang")
    assert channels_list_v1(user1.get("auth_user_id")) == []

def test_channels_valid():
    clear_v1():
    user1 = auth_register_v1("visejoy@gmail.com", "sikk", "Jonathan", "Qiu")

    newchannel1 = channels_create_v1(user1.get("auth_user_id"), "channel1", True)
    newchannel2 = channels_create_v1(user1.get("auth_user_id"), "channel2", True)
    newchannel3 = channels_create_v1(user1.get("auth_user_id"), "channel3", True)

    listchannel = channels_list_v1(user1.get("auth_user_id"))

    assert listchannel.get('channels')[0]["channel_id"] == channel1.get("channel_id")
    assert listchannel.get('channels')[1]["channel_id"] == channel2.get("channel_id")
    assert listchannel.get('channels')[2]["channel_id"] == channel3.get("channel_id")
    assert len(channel_list.get('channels')) == 3


def test_both_priv_pub():
    clear_v1():
    user1 = auth_register_v1("visejoy@gmail.com", "sikk", "Jonathan", "Qiu") 
    user2 = auth_register_v1("thomaschen@gmail.com", "rak", "Thomas", "Chen")

    newchannel1 = channels_create_v1(user1.get("auth_user_id"), "channel1", True)
    newchannel2 = channels_create_v1(user1.get("auth_user_id"), "channel2", False)
    newchannel3 = channels_create_v1(user1.get("auth_user_id"), "channel3", True)

    user1_id = user1.get("auth_user_id")

    listchannel = channels_list_v1(user1_id.get('channels'))

    assert listchannel.get('channels')[0]["channel_id"] == channel1.get("channel_id")
    assert listchannel.get('channels')[1]["channel_id"] == channel2.get("channel_id")
    assert listchannel.get('channels')[2]["channel_id"] == channel3.get("channel_id")
    assert len(channel_list.get('channels')) == 3



# Channel Messages Tests

def test_channel_messages():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    messages = channel_messages_v1(user["auth_user_id"], channel["channel_id"], 0)
    assert messages == {'messages': [], 'start': 0, 'end': -1}

def test_channel_messages_invalid_userid():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    invalid_id = 1
    with pytest.raises(AccessError):
        assert channel_messages_v1(invalid_id, channel["channel_id"], 0) == AccessError

def test_channel_messages_invalid_channelid():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    invalid_channel_id = 1
    with pytest.raises(AccessError):
        assert channel_messages_v1(user["auth_user_id"], invalid_channel_id, 0) == AccessError

def test_channel_messages_unauthorised_user():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    
    with pytest.raises(AccessError):
        assert channel_messages_v1(user2["auth_user_id"], channel["channel_id"], 0) == AccessError
    
def test_channel_messages_startgreater():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    
    with pytest.raises(InputError):
        assert channel_messages_v1(user["auth_user_id"], channel["channel_id"], 1) == InputError

def test_channel_messages_endnegativeone():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user["auth_user_id"], "testchannel", True)
    messages = channel_messages_v1(user["auth_user_id"], channel["channel_id"], 0)
    assert messages["end"] == -1

