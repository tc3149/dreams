import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
import src.database as database
from src.channel import channel_join_v2
from src.channel import channel_messages_v2
from src.message import message_send_v2, message_edit_v2
from src.message import message_senddm_v1, message_share_v1, message_remove_v1, message_sendlater_v1, message_sendlaterdm_v1
from src.dm import dm_create_v1, dm_messages_v1
from datetime import datetime
from time import sleep

# MESSAGE SEND TESTING ---------------------------------------------------------

# empty message
def testsend_empty_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)

    with pytest.raises(InputError):
        message_send_v2(user["token"], channel["channel_id"], '')

# too long of a message, exceeds 1k words
def testsend_long_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)

    temp = 'x' * 2000

    with pytest.raises(InputError):
        message_send_v2(user["token"], channel["channel_id"], temp)


# invalid token ID
def testsend_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    invalid_token = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):    
        message_send_v2(invalid_token, channel["channel_id"], "This is a messsage from Thomas Chen")   


# invalid channel id
def testsend_invalid_channel_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channels_create_v2(user["token"], "testchannel", True)

    with pytest.raises(InputError):
        message_send_v2(user["token"], "wrong_id", "This is a messsage from Thomas Chen")    

# not in channel but sends message
def testsend_message_not_in_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    with pytest.raises(AccessError):
        message_send_v2(user2["token"], channel["channel_id"], "This is a messsage from Thomas Chen")   


# a valid test, a work in progress
def testsend_if_valid():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    message_send_v2(user1["token"], channel["channel_id"], "lol")  
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'lol'
        assert msg["u_id"] == user1["auth_user_id"]



# MESSAGE EDIT TESTING --------------------------------------------------------------------

# empty message

def testedit_empty_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(InputError):
        message_edit_v2(user["token"], m_id, '')


# edited message over 1k words

def testedit_long_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    long_message = 'x' * 9999

    with pytest.raises(InputError):
        message_edit_v2(user["token"], m_id, long_message)


# invalid token ID

def testedit_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    invalid_token = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_edit_v2(invalid_token, m_id, 'Jonathan Chen')

# invalid message id

def testedit_invalid_message_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")

    with pytest.raises(InputError):
        message_edit_v2(user["token"], "wrong_id", 'Jonathan Chen')

# whether the message id is user-based

def testedit_edited_from_another():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_edit_v2(user2["token"], m_id, 'Russell Westbrook')


# someone else edits the comment not by owner
def testedit_notedited_by_owner():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_edit_v2(user2["token"], m_id, 'Russell Westbrook')


# a valid test
def testedit_valid_case():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    message_info = message_send_v2(user1["token"], channel["channel_id"], "lol")  
    m_id = message_info.get("message_id")
    message_edit_v2(user1["token"], m_id, "lmfao")
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'lmfao'
        assert msg["u_id"] == user1["auth_user_id"]


# more in depth
def testedit_indepth_validtesting():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")
    message_edit_v2(user1["token"], m_id, "lmfao")

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'lmfao'
        assert msg["u_id"] == user2["auth_user_id"]




# MESSAGE REMOVE TESTING ------------------------------------------------------------------

# invalid token ID
def testremove_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    invalid_token = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_remove_v1(invalid_token, m_id)


# invalid message id
def testremove_invalid_message_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")


    with pytest.raises(InputError):
        message_remove_v1(user["token"], "wrong_id")


# removing already removed message
def testremove_removed_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        message_remove_v1(user["token"], "m_id")

# another user that is not owner/OP trying to remove
def testremove_not_authorised():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_remove_v1(user2["token"], m_id)

# valid test of removing
def testremove_valid_case():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    message_info = message_send_v2(user1["token"], channel["channel_id"], "lol")  
    m_id = message_info.get("message_id")
    message_remove_v1(user1["token"], m_id)
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == ''
        assert msg["u_id"] == user1["auth_user_id"]


# Comprehensive Testing Case
def testremove_comprehensive():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")
    message_remove_v1(user1["token"], m_id)

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == ""
        assert msg["u_id"] == user2["auth_user_id"]    



# MESSAGE SENDDM TESTING ------------------------------------------------------------------------

# Empty Message
def testsenddm_empty_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    with pytest.raises(InputError):
        message_senddm_v1(user["token"], dm["dm_id"], "")

# too long of a message, exceeds 1k words
def testsenddm_long_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    temp = 'x' * 2000

    with pytest.raises(InputError):
        message_senddm_v1(user["token"], dm["dm_id"], temp)

# invalid token ID
def testsenddm_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    invalid_token = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm["dm_id"], "Thomas Chen")


# invalid dm_ID
def testsenddm_invalid_dm_ID():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm_create_v1(user["token"], [user2["auth_user_id"]])

    with pytest.raises(InputError):
        message_senddm_v1(user["token"], "invalid_dmID", "Thomas Chen")


# user not in DM
def testsenddm_user_notin_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])  

    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(AccessError):
        message_senddm_v1(user3["token"], dm["dm_id"], "Jonathan Qiu")


# valid testing
def testsenddm_valid():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])
    message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")

    message_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'Jonathan'
        assert msg["u_id"] == user2["auth_user_id"]

    message_senddm_v1(user["token"], dm["dm_id"], "Thomas")
    
    message_info2 = dm_messages_v1(user["token"], dm["dm_id"], 0)

    for second in message_info2["messages"]:
        if second["u_id"] is user["auth_user_id"]:
            assert second["message_id"] == 2
            assert second["message"] == 'Thomas'


# MESSAGE SHARE TESTING ------------------------------------------------------------------------------------

def test_user_not_member_of_channel_they_sharing_to():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = ""
    dm_id = -1
    
    with pytest.raises(AccessError):
        message_share_v1(user2["token"],og_message_id,message,channel['channel_id'],dm_id)
    

def test_user_not_member_of_dm_they_sharing_to():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    id_list = []
    id_list.append(user1["auth_user_id"])
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user1["token"], id_list)

    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = ""
    channel_id = -1
    with pytest.raises(AccessError):
        message_share_v1(user3["token"],og_message_id,message,channel_id,dm["dm_id"])


def test_optional_message_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel2 = channels_create_v2(user1["token"], "testchannel2", True)
    og_message_id = message_send_v2(user1["token"],channel['channel_id'],'This is a message')
    message = "from manu"
    dm_id = -1
    message_share_v1(user1["token"], og_message_id["message_id"], message,channel2['channel_id'], dm_id)
    messages1 = channel_messages_v2(user1["token"], channel2["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 2
        assert msg["message"] == 'from manu\n\n"""\nThis is a message\n"""'
        assert msg["u_id"] == user1["auth_user_id"]




def test_no_optional_message_valid_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel2 = channels_create_v2(user1["token"], "testchannel2", True)
    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = ""
    dm_id = -1 

    message_share_v1(user1["token"],og_message_id["message_id"],message,channel2['channel_id'],dm_id)
    messages1 = channel_messages_v2(user1["token"], channel2["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 2
        assert msg["message"] == '\n\n"""\nThis is a message\n"""'
        assert msg["u_id"] == user1["auth_user_id"]

def test_with_optional_message_dm():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])

    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = "from manu"
    channel_id = -1

    message_share_v1(user1["token"],og_message_id["message_id"],message,channel_id,dm["dm_id"])
    messages1 = dm_messages_v1(user1["token"], dm["dm_id"], 0)

    assert messages1["messages"][0]["message_id"] == 2
    assert messages1["messages"][0]["message"] == 'from manu\n\n"""\nThis is a message\n"""'
    assert messages1["messages"][0]["u_id"] == user1["auth_user_id"]


def test_without_optional_message_dm():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])

    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = ""
    channel_id = -1

    message_share_v1(user1["token"],og_message_id["message_id"],message,channel_id,dm["dm_id"])
    messages1 = dm_messages_v1(user1["token"], dm["dm_id"], 0)

    assert messages1["messages"][0]["message_id"] == 2
    assert messages1["messages"][0]["message"] == '\n\n"""\nThis is a message\n"""'
    assert messages1["messages"][0]["u_id"] == user1["auth_user_id"]


# MESSAGE SEND LATER TESTING -------------------------------------------------------

# Message too long (over 1k)
def testsendlater_invalid_message():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time = int(datetime.timestamp(datetime.now()) + 2)
    temp = 'x' * 2354

    with pytest.raises(InputError):
        message_sendlater_v1(user1["token"], channel["channel_id"], temp, time)


# Invalid Token ID
def testsendlater_invalid_token():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time = int(datetime.timestamp(datetime.now()) + 2)
    invalid_token = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_sendlater_v1(invalid_token, channel["channel_id"], "Thomas Chen lmfao", time)


# Invalid Channel ID
def testsendlater_invalid_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channels_create_v2(user1["token"], "testchannel", True)

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(InputError):
        message_sendlater_v1(user1["token"], "invalid_id", "Thomas Chen lmfao", time)


# Empty Message
def testsendlater_empty_message():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(InputError):
        message_sendlater_v1(user1["token"], channel["channel_id"], "", time)


# User not in channel
def testsendlater_user_not_in_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(AccessError):
        message_sendlater_v1(user2["token"], channel["channel_id"], "Thomas Chen lmfao", time)


# Message sent in past
def testsendlater_invalid_time():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time_set = int(datetime.timestamp(datetime.now()) - 2)

    with pytest.raises(InputError):
        message_sendlater_v1(user1["token"], channel["channel_id"], "Thomas Chen lmfao", time_set)


# Valid Case Testing
def testsendlater_valid_case():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    time_set = int(datetime.timestamp(datetime.now()) + 2)

    message_sendlater_v1(user1["token"], channel["channel_id"], "i'll see you in the future", time_set)
    
    message_info = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    assert len(message_info["messages"]) == 0

    sleep(3)

    message_info_later = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    
    for messages1 in message_info_later["messages"]:
        if messages1["u_id"] is user1["auth_user_id"]:
            assert messages1["message"] == "i'll see you in the future"
            assert messages1["time_created"] == time_set


# MESSAGE SEND LATER DM TESTING -------------------------------------------------------

# Message too long (over 1k)
def testsendlaterdm_invalid_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)
    temp = 'x' * 2354

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user["token"], dm["dm_id"], temp, time)


# Invalid Token ID
def testsendlaterdm_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)
    invalid_token = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_sendlaterdm_v1(invalid_token, dm["dm_id"], "Imagine Trump saying Jonathan", time)


# Invalid dm ID
def testsendlaterdm_invalid_DM():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user["token"], "invalid_id", "Imagine Trump saying Jonathan", time)


# Empty Message
def testsendlaterdm_invalid_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user["token"], dm["dm_id"], "", time)


# User not in DM
def testsendlaterdm_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user3["token"], dm["dm_id"], "Imagine Trump saying Jonathan", time)


# Time set in the past
def testsendlaterdm_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) - 2)

    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user["token"], dm["dm_id"], "Imagine Trump saying Jonathan", time)


# Valid Case Testing
def testsendlaterdm_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    message_sendlaterdm_v1(user2["token"], dm["dm_id"], "Imagine Trump saying Jonathan", time)

    dm_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)
    assert len(dm_info["messages"]) == 0

    sleep(3)

    dm_info_later = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for dms in dm_info_later["messages"]:
        if dms["u_id"] is user["auth_user_id"]:
            assert dms["message"] == "Imagine Trump saying Jonathan"
            assert dms["time_created"] == time
        