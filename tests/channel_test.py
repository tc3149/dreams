import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1, channel_invite_v1, channel_details_v1, channel_leave_v1
from src.channels import channels_create_v1, channels_list_v1
from src.database import accData, channelList
from src.channel import channel_join_v1

# ------------------------------------------------------------------------------------------------------
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
    invalid_id = 2
    with pytest.raises(AccessError):
        assert channel_messages_v1(invalid_id, channel["channel_id"], 0) == AccessError

def test_channel_messages_invalid_channelid():

    clear_v1()
    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channels_create_v1(user["auth_user_id"], "testchannel", True)
    invalid_channel_id = 2
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
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# TEST JOINING

# VALID CASES

def test_join_correct():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v1("email3@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user1["auth_user_id"], "testchannel", True)

    inner = channelList[0]
    channel_join_v1(user2["auth_user_id"], channel["channel_id"])
    channel_join_v1(user3["auth_user_id"], channel["channel_id"])

    assert inner["member_ids"] == [user1["auth_user_id"], user2["auth_user_id"], user3["auth_user_id"]]

    
# FAIL CASES

# joining empty
def test_joining_nonexistant_channel():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "channel1", True)

    with pytest.raises(InputError):
        channel_join_v1(user2.get("auth_user_id"), 1000)

# invalid user id 
def test_joining_invalid_user():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    new = channels_create_v1(user1.get("auth_user_id"), "channel1", True)
    temp = 21492144
    
    with pytest.raises(InputError):
        channel_join_v1(temp, new.get("channel_id"))


# invalid channel id
def test_joining_invalid_channel():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "channel1", True)

    temp = 312312321321

    with pytest.raises(InputError):
        channel_join_v1(user2.get("auth_user_id"), temp)

def test_joining_user_alrady_joined():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1["auth_user_id"], "testchannel", True)
    channel_join_v1(user2["auth_user_id"], channel1["channel_id"])
    with pytest.raises(AccessError):
        channel_join_v1(user2["auth_user_id"], channel1["channel_id"])

    
# private channel accesserror...?

def test_private_channel():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    new = channels_create_v1(user1.get("auth_user_id"), "channel1", False)

    with pytest.raises(AccessError):
        channel_join_v1(user2["auth_user_id"], new["channel_id"])

# Tested on a private channel
def test_user_already_in_channel():
    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    new = channels_create_v1(user1.get("auth_user_id"), "channel1", False)
    with pytest.raises(AccessError):
        channel_join_v1(user1["auth_user_id"], new["channel_id"])
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
#Channel_invite tests

def test_channel_invite_auth_id_doesnt_exist():
    clear_v1()
    user1 = auth_register_v1("email1@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1["auth_user_id"], "testChannel", True)
    with pytest.raises(InputError):
        channel_invite_v1(3, channel1["channel_id"], user2["auth_user_id"])

def test_channel_invite_user_already_exists():
    clear_v1()
    user1 = auth_register_v1("email1@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1["auth_user_id"], "testChannel", True)
    channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user2["auth_user_id"])
    with pytest.raises(InputError):
        channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user2["auth_user_id"])

def test_channel_does_not_exist():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password2", "Firstname", "Name")
    channels_create_v1(user1.get("auth_user_id"), "testchannel", True)

    with pytest.raises(InputError):
        assert channel_invite_v1(user1["auth_user_id"], 100, user2["auth_user_id"]) == InputError


def test_adding_user_not_created():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    
    with pytest.raises(InputError):
        assert channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], 100) == InputError

def test_user_not_owner_member_of_channel():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password2", "Firstname", "Name")
    user3 = auth_register_v1("email3@gmail.com", "password3", "Fname", "Lname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    
    with pytest.raises(AccessError):
        assert channel_invite_v1(user2["auth_user_id"], channel1["channel_id"], user3["auth_user_id"]) == AccessError

def test_successful_invite():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password2", "Firstname", "Name")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)

    assert channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user2["auth_user_id"]) == {}

def test_multi_add():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password2", "Firstname", "Name")
    user3 = auth_register_v1("email3@gmail.com", "password3", "Fname", "Lname")
    user4 = auth_register_v1("email4@gmail.com", "password4", "First", "Last")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    
    assert channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user2["auth_user_id"]) == {}
    assert channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user3["auth_user_id"]) == {}
    assert channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user4["auth_user_id"]) == {}
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
#channel_details tests

def test_channel_details_not_owner():
    clear_v1()
    user1 = auth_register_v1("email1@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    with pytest.raises(AccessError):
        assert channel_details_v1(user2["auth_user_id"], channel1["channel_id"]) == AccessError

def test_non_existing_channel ():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testchannel", True)

    with pytest.raises(InputError):
        assert channel_details_v1(user1["auth_user_id"], 123456789) == InputError

def test_user_doesnt_exist (): 
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    
    with pytest.raises(AccessError):
        assert channel_details_v1(123, channel1["channel_id"]) == AccessError

def test_valid_input ():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)

    assert channel_details_v1(user1["auth_user_id"], channel1["channel_id"]) == {
                                        'name': 'testchannel',
                                        'owner_members': [
                                            {
                                                'u_id': user1["auth_user_id"],
                                                'email': 'email@gmail.com',
                                                'name_first': 'Name',
                                                'name_last': 'Lastname',
                                                'handle_str': 'namelastname',
                                                
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': user1["auth_user_id"],
                                                'email': 'email@gmail.com',
                                                'name_first': 'Name',
                                                'name_last': 'Lastname',
                                                'handle_str': 'namelastname',
                                                
                                            }
                                        ],
                                        } 

''' Cant pass nothing to a function that requires arguments
def test_empty():
    clear_v1()

    user = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testchannel", True)
    
    with pytest.raises(InputError):
        assert channel_details_v1() == InputError 
'''

def test_identical_handles_details():
    clear_v1()

    user1 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testchannel", True)
    user2 = auth_register_v1("email2@gmail.com", "password2", "Name", "Lastname")
    channel_invite_v1(user1["auth_user_id"], channel1["channel_id"], user2["auth_user_id"])
    assert channel_details_v1(user1["auth_user_id"], channel1["channel_id"]) == {
                                        'name': 'testchannel',
                                        'owner_members': [
                                            {
                                                'u_id': user1["auth_user_id"],
                                                'email': 'email@gmail.com',
                                                'name_first': 'Name',
                                                'name_last': 'Lastname',
                                                'handle_str': 'namelastname',                                             
                                            }
                                        ],
                                        'all_members': [
                                            {
                                                'u_id': user1["auth_user_id"],
                                                'email': 'email@gmail.com',
                                                'name_first': 'Name',
                                                'name_last': 'Lastname',
                                                'handle_str': 'namelastname',                                               
                                            },
                                            {
                                                'u_id': user2["auth_user_id"],
                                                'email':'email2@gmail.com',
                                                'name_first': 'Name',
                                                'name_last': 'Lastname',
                                                'handle_str': 'namelastname0',
                                            }
                                        ],
                                        } 
# ------------------------------------------------------------------------------------------------------
#channel_leave_v1
def test_channel_leave():

    #Testing main implementation

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "testChannel2", True)
    channel_leave_v1(user1.get("auth_user_id"), channel1.get("channel_id"))
    result = channels_list_v1(user1.get("auth_user_id"))
    assert result == {'channels': [{'channel_id': channel2.get("channel_id"), 'name': 'testChannel2'}]}

def test_channel_leave_empty():

    #Testing main implementation

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel_leave_v1(user1.get("auth_user_id"), channel1.get("channel_id"))
    result = channels_list_v1(user1.get("auth_user_id"))
    assert result == {'channels': []}

def test_channel_leave_multiple():

    #Testing main implementation

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    channel2 = channels_create_v1(user1.get("auth_user_id"), "testChannel2", True)
    channel3 = channels_create_v1(user1.get("auth_user_id"), "testChannel3", True)
    channel_leave_v1(user1.get("auth_user_id"), channel1.get("channel_id"))
    channel_leave_v1(user1.get("auth_user_id"), channel2.get("channel_id"))
    result = channels_list_v1(user1.get("auth_user_id"))
    assert result == {'channels': [{'channel_id': channel3.get("channel_id"), 'name': 'testChannel3'}]}

def test_channel_leave_channel_valid():

    #Testing Input Error

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    with pytest.raises(InputError):
        assert channel_leave_v1(user1.get("auth_user_id"), " ") == InputError

def test_channel_leave_user_valid():

    #Testing Access Error

    clear_v1()
    user1 = auth_register_v1("email@gmail.com", "password", "name", "Lastname")
    user2 = auth_register_v1("email2@gmail.com", "password", "name", "Lastname")
    channel1 = channels_create_v1(user1.get("auth_user_id"), "testChannel", True)
    with pytest.raises(AccessError):
        assert channel_leave_v1(user2.get("auth_user_id"), channel1.get("channel_id")) == AccessError

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
#channel_removeowner_v1

# ------------------------------------------------------------------------------------------------------
