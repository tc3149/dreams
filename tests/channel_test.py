import pytest
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError
from src.channel import channel_messages_v1
from src.channel import channels_create_v1

# TC - channel_messages

def test_invalidChannel_messages():
    #Test 1: Invalid channel
    user = auth.auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels.channels_create_v1(user.get("auth_user_id"), "testchannel", True)
    

    # make user connect to channel (23) that has not been created
    with pytest.raises(InputError):
        channel_messages_v1(user.get("auth_user_id"), 23, 0)
    
def test_startGreaterEnd_messages():
    #Test 2: Start is greater than the total messages



def test_userInvalid_messages():
    #Test 3: User is invalid to check messages

    #make user1 create a channel then user2 try see the messages of their channel

