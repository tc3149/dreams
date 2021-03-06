import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.channels import channels_listall_v1
from src.channels import channels_list_v1
from src.database import accData, channelList

# Channel Create Tests

def test_channels_create():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testchannel", True)
    assert channel == {'channel_id': 0}

def test_channels_create_invalid():

    clear_v1()
    invalid_token = 0
    with pytest.raises(AccessError):
        assert channels_create_v1(invalid_token, "testchannel", True) == AccessError

def test_channels_create_many():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user.get("auth_user_id"), "channel1", True)
    channel2 = channels_create_v1(user.get("auth_user_id"), "channel2", True)
    channel3 = channels_create_v1(user.get("auth_user_id"), "channel3", True)
    channel4 = channels_create_v1(user.get("auth_user_id"), "channel4", True)
    channel5 = channels_create_v1(user.get("auth_user_id"), "channel5", True)
    channel6 = channels_create_v1(user.get("auth_user_id"), "channel6", True)
    assert channel1 == {'channel_id': 0}
    assert channel2 == {'channel_id': 1}
    assert channel3 == {'channel_id': 2}
    assert channel4 == {'channel_id': 3}
    assert channel5 == {'channel_id': 4}
    assert channel6 == {'channel_id': 5}

def test_channels_create_longerthan20():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user_id = user.get("auth_user_id")
    with pytest.raises(InputError):
        assert channels_create_v1(user_id, "a" *21, True) == InputError

def test_channels_create_noname():
    
    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email3@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v1("email33@gmail.com", "password", "Name", "Lastname")
    user_id = user.get("auth_user_id")
    with pytest.raises(InputError):
        assert channels_create_v1(user_id, "", True) == InputError

def test_channels_create_private():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user_id = user.get("auth_user_id")
    channel = channels_create_v1(user_id, "testChannel", False)
    assert channelList[0].get("is_public") == False

#Channels_list
def test_channels_list():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", True)
    result = channels_list_v1(user2.get("auth_user_id")) 

    assert result == {'channels': [{'channel_id': 1, 'name': 'testChannel2'}]}

def test_channels_list_empty():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", True)
    result = channels_list_v1(user2.get("auth_user_id")) 

    assert result == {'channels': []}

def test_channels_list_invalid():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", True)
    result = channels_list_v1(user2.get("auth_user_id")) 

    assert result == {'channels': []}

def test_channels_list_private():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", False)
    result = channels_list_v1(user2.get("auth_user_id")) 

    assert result == {'channels': [{'channel_id': 1, 'name': 'testChannel2'}]}

def test_channels_list_private_public():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user2.get("auth_user_id"), "testChannel2", False)
    channel3 = channels_create_v1(user2.get("auth_user_id"), "testChannel3", True)
    result = channels_list_v1(user2.get("auth_user_id")) 

    assert result == {'channels': [{'channel_id': 1, 'name': 'testChannel2'}, {'channel_id': 2, 'name': 'testChannel3'}]}

#Channels_listall

def test_channels_listall():
    
    clear_v1()

    invalid_user_id = 0

    with pytest.raises(AccessError):
        assert channels_listall_v1(invalid_user_id) == AccessError

def test_channels_listall_invalid():

    clear_v1()

    invalid_user_id = 0

    with pytest.raises(AccessError):
        assert channels_listall_v1(invalid_user_id) == AccessError

def test_channels_listall_no_users():
    
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    result = channels_listall_v1(user.get("auth_user_id")) 

    assert result == {'channels': []}

def test_channels_listall_private():

    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user.get("auth_user_id"), "testChannel2", False)
    result = channels_listall_v1(user.get("auth_user_id"))

    assert result == {'channels': [{'channel_id': 0, 'name': 'testChannel'}, {'channel_id': 1, 'name': 'testChannel2'}]}

def test_channels_listall_public_private():

    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testChannel", False)
    channel2 = channels_create_v1(user.get("auth_user_id"), "testChannel2",True)
    result = channels_listall_v1(user.get("auth_user_id"))
    
    assert result == {'channels': [{'channel_id': 0, 'name': 'testChannel'}, {'channel_id': 1, 'name': 'testChannel2'}]}


#def test_invalidChannel_messages():
    #Test 1: Invalid channel
    #user = auth.auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    #channel = channels.channels_create_v1(user.get("auth_user_id"), "testchannel", True)
    

    # make user connect to channel (23) that has not been created
    #with pytest.raises(InputError):
        #channel_messages_v1(user.get("auth_user_id"), 23, 0)
    
#def test_startGreaterEnd_messages():
    #Test 2: Start is greater than the total messages



#def test_userInvalid_messages():
    #Test 3: User is invalid to check messages

    #make user1 create a channel then user2 try see the messages of their channel
