import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.channels import channels_listall_v1
from src.channels import channels_list_v1

# ------------------------------------------------------------------------------------------------------
# Channel Create Tests

def test_channels_create():

    # Testing if a channel can be created
    
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    assert channel1 == {'channel_id': channel1["channel_id"]}

def test_channels_create_invalid():

    # Testing if an error is given for invalid user ids

    clear_v1()
    invalid_user = 0
    with pytest.raises(AccessError):
        assert channels_create_v1(invalid_user, "testchannel", True) == AccessError

def test_channels_create_many():

    # Testing if many channels can be created from a single user

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "channel1", True)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "channel2", True)
    channel3 = channels_create_v1(user1.get("auth_user_id"), "channel3", True)
    channel4 = channels_create_v1(user1.get("auth_user_id"), "channel4", True)
    channel5 = channels_create_v1(user1.get("auth_user_id"), "channel5", True)
    channel6 = channels_create_v1(user1.get("auth_user_id"), "channel6", True)
    assert channel1 == {'channel_id': channel1["channel_id"]}
    assert channel2 == {'channel_id': channel2["channel_id"]}
    assert channel3 == {'channel_id': channel3["channel_id"]}
    assert channel4 == {'channel_id': channel4["channel_id"]}
    assert channel5 == {'channel_id': channel5["channel_id"]}
    assert channel6 == {'channel_id': channel6["channel_id"]}

def test_channels_create_longerthan20():

    # Testing if channel names longer than 20 characters result in inputerror

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        assert channels_create_v1(user1["auth_user_id"], "a" *21, True) == InputError

def test_channels_create_noname():

    # Testing if channel names less than 1 character result in input error

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        assert channels_create_v1(user1["auth_user_id"], "", True) == InputError

def test_channels_create_private():

    # Testing if channel can be created with private parameter

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1["auth_user_id"], "testChannel", False)
    assert channel1 == {"channel_id": channel1["channel_id"]}
    #assert channelList[0]["is_public"] == False
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# Channels_list tests

def test_channels_list():

    # Testing if channels list can be returned from function

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", True)
    channel_join_v1(user2["auth_user_id"], channel1["channel_id"])
    result = channels_list_v1(user2["auth_user_id"]) 
    assert result == {'channels': [{'channel_id': channel1["channel_id"], 'name': 'testChannel'}, {'channel_id': channel2["channel_id"], 'name': 'testChannel2'}]}

def test_channels_list_empty():

    # Testing if no joined channels for a user results in an empty list

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    result = channels_list_v1(user2.get("auth_user_id")) 
    assert result == {'channels': []}

def test_channels_list_invalid():
 
    # Testing if invalid user_id results in accesserror
  
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    invalid_id = 5
    with pytest.raises(AccessError):
        assert channels_list_v1(invalid_id) == AccessError

def test_channels_list_private():
 
    #Testing if channel list can show private channels

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", False)
    result = channels_list_v1(user2.get("auth_user_id"))
    assert result == {'channels': [{'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_list_private_public():

    #Testing if channel list can show both public and private channels

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", False)
    channel3 = channels_create_v1(user1.get("auth_user_id"), "testChannel3", True)
    channel_join_v1(user2.get("auth_user_id"), channel3.get("channel_id"))
    result = channels_list_v1(user2.get("auth_user_id")) 
    assert result == {'channels': [{'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}, {'channel_id': channel3.get("channel_id"), 'name': 'testChannel3'}]}
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
#Channels_listall tests

def test_channels_listall():
 
    # Testing if channels_listall can return a list of channels

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "testChannel2", True)
    assert channels_listall_v1(user1.get("auth_user_id")) == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_listall_invalid():

    # Testing if an error is given from invalid user ids

    clear_v1()
    invalid_user_id = 0
    with pytest.raises(AccessError):
        assert channels_listall_v1(invalid_user_id) == AccessError

def test_channels_listall_no_channels():

    # Testing if no channels results in an empty list

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    result = channels_listall_v1(user1.get("auth_user_id")) 
    assert result == {'channels': []}

def test_channels_listall_private():
 
    # Testing if private channels function with listall

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "testChannel2", False)
    result = channels_listall_v1(user1.get("auth_user_id"))
    assert result == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channels_listall_public_private():

    # Testing if both private and public channels function with listall

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "testChannel2",True)
    result = channels_listall_v1(user1.get("auth_user_id"))
    assert result == {'channels': [{'channel_id': channel1.get("channel_id"), 'name': 'testChannel'}, {'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}
# ------------------------------------------------------------------------------------------------------
