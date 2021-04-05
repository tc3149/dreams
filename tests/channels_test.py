import pytest
import jwt
import src.database as database
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2

# ------------------------------------------------------------------------------------------------------
# Channel Create Tests

def test_channels_create():

    # Testing if a channel can be created
    
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "testchannel", True)
    assert channel1 == {'channel_id': channel1["channel_id"]}

def test_channels_create_invalid():

    # Testing if an error is given for invalid user ids

    clear_v1()
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert channels_create_v2(invalid_id, "testchannel", True) == AccessError

def test_channels_create_many():

    # Testing if many channels can be created from a single user

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "channel1", True)
    channel2 = channels_create_v2(user1.get("token"), "channel2", True)
    channel3 = channels_create_v2(user1.get("token"), "channel3", True)
    channel4 = channels_create_v2(user1.get("token"), "channel4", True)
    channel5 = channels_create_v2(user1.get("token"), "channel5", True)
    channel6 = channels_create_v2(user1.get("token"), "channel6", True)
    assert channel1 == {'channel_id': channel1["channel_id"]}
    assert channel2 == {'channel_id': channel2["channel_id"]}
    assert channel3 == {'channel_id': channel3["channel_id"]}
    assert channel4 == {'channel_id': channel4["channel_id"]}
    assert channel5 == {'channel_id': channel5["channel_id"]}
    assert channel6 == {'channel_id': channel6["channel_id"]}

def test_channels_create_longerthan20():

    # Testing if channel names longer than 20 characters result in inputerror

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        assert channels_create_v2(user1["token"], "a" *21, True) == InputError

def test_channels_create_noname():

    # Testing if channel names less than 1 character result in input error

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        assert channels_create_v2(user1["token"], "", True) == InputError

def test_channels_create_private():

    # Testing if channel can be created with private parameter

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v2(user1["token"], "testChannel", False)
    assert channel1 == {"channel_id": channel1["channel_id"]}
    #assert channelList[0]["is_public"] == False
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# Channels_list tests

def test_channels_list():

    # Testing if channels list can be returned from function

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "testChannel", True)
    channel2 = channels_create_v2(user2.get("token"), "testChannel2", True)
    channel_join_v2(user2["token"], channel1["channel_id"])
    result = channels_list_v2(user2["token"]) 
    assert result == {'channels': [{'channel_id': channel1["channel_id"], 'name': 'testChannel'}, {'channel_id': channel2["channel_id"], 'name': 'testChannel2'}]}

def test_channels_list_empty():

    # Testing if no joined channels for a user results in an empty list

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v2(user1.get("token"), "testChannel", True)
    result = channels_list_v2(user2.get("token")) 
    assert result == {'channels': []}


def test_channels_list_invalid():
 
    # Testing if invalid user_id results in accesserror
  
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    auth_register_v2("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v2(user1.get("token"), "testChannel", True)
    invalid_id = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert channels_list_v2(invalid_id)

def test_channels_list_private():
 
    #Testing if channel list can show private channels

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v2(user1.get("token"), "testChannel", True)
    channel2 = channels_create_v2(user2.get("token"), "testChannel2", False)
    result = channels_list_v2(user2.get("token"))
    assert result == {'channels': [{'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_list_private_public():

    #Testing if channel list can show both public and private channels

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v2(user1.get("token"), "testChannel", False)
    channel2 = channels_create_v2(user2.get("token"), "testChannel2", False)
    channel3 = channels_create_v2(user1.get("token"), "testChannel3", True)
    channel_join_v2(user2.get("token"), channel3.get("channel_id"))
    result = channels_list_v2(user2.get("token")) 
    assert result == {'channels': [{'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}, {'channel_id': channel3.get("channel_id"), 'name': 'testChannel3'}]}
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
#Channels_listall tests

def test_channels_listall():
 
    # Testing if channels_listall can return a list of channels

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "testChannel", True)
    channel2 = channels_create_v2(user1.get("token"), "testChannel2", True)
    assert channels_listall_v2(user1.get("token")) == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_listall_invalid():

    # Testing if an error is given from invalid user ids

    clear_v1()
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert channels_listall_v2(invalid_id) == AccessError

def test_channels_listall_no_channels():

    # Testing if no channels results in an empty list

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    result = channels_listall_v2(user1.get("token")) 
    assert result == {'channels': []}

def test_channels_listall_private():
 
    # Testing if private channels function with listall

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "testChannel", False)
    channel2 = channels_create_v2(user1.get("token"), "testChannel2", False)
    result = channels_listall_v2(user1.get("token"))
    assert result == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_listall_public_private():

    # Testing if both private and public channels function with listall

    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v2(user1.get("token"), "testChannel", False)
    channel2 = channels_create_v2(user1.get("token"), "testChannel2",True)
    result = channels_listall_v2(user1.get("token"))
    assert result == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}
