import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.database import accData, channelList

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

