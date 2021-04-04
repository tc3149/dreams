import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2
from src.channels import channels_create_v2
from src.database import data, secretSauce
from src.channel import channel_join_v2
from src.channel import channel_messages_v2
from src.message import message_send_v2
from src.message import message_edit_v2
from src.message import message_remove_v1
from src.message import message_senddm_v1
from src.dm import dm_create_v1, dm_messages_v1

# MESSAGE SEND TESTING

# too long of a message, exceeds 1k words
def testsend_long_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)

    temp = 'x' * 2000

    with pytest.raises(InputError):
        message_send_v2(user["token"], channel["channel_id"], temp)


# invalid  token ID
def testsend_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    invalid_token = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")

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



# MESSAGE EDIT TESTING

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
    invalid_token = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")

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
    print(m_id)


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


# a valid test, a work in progress *************************  COLIN LOOK HERE
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




# MESSAGE REMOVE TESTING

# invalid token ID
def testremove_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    invalid_token = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")

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




# MESSAGE SENDDM TESTING

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

    invalid_token = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm["dm_id"], "Thomas Chen")


# invalid dm_ID
def testsenddm_invalid_token():
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
    message = message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")

    message_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'Jonathan'
        assert msg["u_id"] == user2["auth_user_id"]


