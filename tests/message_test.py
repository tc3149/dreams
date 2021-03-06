import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
import src.database as database
from src.channel import channel_join_v2
from src.channel import channel_messages_v2, channel_leave_v1, channel_addowner_v1
from src.message import message_send_v2, message_edit_v2, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.message import message_senddm_v1, message_share_v1, message_remove_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_leave_v1
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


# original poster not in channel but edits
def testedit_not_in_channel_anymore():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    channel_leave_v1(user2["token"], channel["channel_id"])

    with pytest.raises(AccessError):
        message_edit_v2(user2["token"], message1["message_id"], "Let me edit!")

# original poster not in dm but edits
def testedit_not_in_dm_anymore():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    m_id = message_senddm_v1(user2["token"], dm["dm_id"], "LMFAO LMBAO")

    dm_leave_v1(user2["token"], dm["dm_id"])

    with pytest.raises(AccessError):
            message_edit_v2(user2["token"], m_id["message_id"], "Let me edit!")

# a valid test in channel
def testedit_valid_case_in_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")  
    m_id = message_info.get("message_id")
    message_edit_v2(user2["token"], m_id, "lmfao")
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'lmfao'
        assert msg["u_id"] == user2["auth_user_id"]


# another valid
def testedit_valid2():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user1["token"], channel["channel_id"])

    message_info2 = message_send_v2(user1["token"], channel["channel_id"], "lol")  
    message_edit_v2(user2["token"], message_info2["message_id"], "okay i edit now")

    messages1_later = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1_later["messages"]:
        if msg["u_id"] == user1["auth_user_id"]:
            assert msg["message_id"] == 1
            assert msg["message"] == "okay i edit now"




# a valid case in DM
def testedit_valid_case_in_DM():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user3["token"], [user["auth_user_id"], user2["auth_user_id"]])
    
    m_id = message_senddm_v1(user2["token"], dm["dm_id"], "LMFAO LMBAO")
    message_edit_v2(user3["token"], m_id["message_id"], "hookay bro")

    messages1 = dm_messages_v1(user["token"], dm["dm_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'hookay bro'
        assert msg["u_id"] == user2["auth_user_id"]
    

# more in depth
def testedit_indepth_validtesting():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")
    message_edit_v2(user2["token"], m_id, "lmfao")

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == 'lmfao'
        assert msg["u_id"] == user2["auth_user_id"]


# Empty message ("") should remove the message
def testedit_empty_message():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_edit_v2(user["token"], m_id, '')

    messages1 = channel_messages_v2(user["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == ''
        assert msg["u_id"] == user["auth_user_id"]


# Dream Owner Editing
def testedit_dream_owner():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    
    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user3["token"], channel["channel_id"])
    channel_join_v2(user["token"], channel["channel_id"])

    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")

    message_edit_v2(user["token"], m_id, "RUSSELL WESTBROOK MVP")

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 1
        assert msg["message"] == "RUSSELL WESTBROOK MVP"
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
    channel = channels_create_v2(user["token"], "testchannel", True)
    m_id = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")

    message_remove_v1(user["token"], m_id["message_id"])

    with pytest.raises(InputError):
        message_remove_v1(user["token"], m_id["message_id"])

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

# original poster not in channel but removes
def testremove_not_in_channel_anymore():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    channel_leave_v1(user2["token"], channel["channel_id"])

    with pytest.raises(AccessError):
        message_remove_v1(user2["token"], message1["message_id"])

# original poster not in dm but remove
def testremove_not_in_dm_anymore():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    m_id = message_senddm_v1(user2["token"], dm["dm_id"], "LMFAO LMBAO")

    dm_leave_v1(user2["token"], dm["dm_id"])

    with pytest.raises(AccessError):
        message_remove_v1(user2["token"], m_id["message_id"])


# valid test of removing in  channel
def test_remove_valid_case_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user1["token"], channel["channel_id"])
    channel_join_v2(user3["token"], channel["channel_id"])

    message_info = message_send_v2(user1["token"], channel["channel_id"], "lol")  
    m_id = message_info.get("message_id")

    message_remove_v1(user2["token"], m_id)
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    assert messages1 == {'end': -1, 'messages': [], 'start': 0}
    message_info2 = message_send_v2(user3["token"], channel["channel_id"], "lol")  
    m_id2 = message_info2.get("message_id")

    message_remove_v1(user3["token"], m_id2)
    messages2 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    assert messages2 == {'end': -1, 'messages': [], 'start': 0}

# a valid case in DM
def test_remove_valid_case_in_DM():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user3["token"], [user2["auth_user_id"], user["auth_user_id"]])
    
    m_id = message_senddm_v1(user2["token"], dm["dm_id"], "LMFAO LMBAO")
    message_remove_v1(user3["token"], m_id["message_id"])

    messages1 = dm_messages_v1(user["token"], dm["dm_id"], 0)

    assert messages1 == {'end': -1, 'messages': [], 'start': 0}

# Comprehensive Testing Case
def test_remove_comprehensive():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")
    message_remove_v1(user1["token"], m_id)

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    assert messages1 == {'end': -1, 'messages': [], 'start': 0}

# Dream Owner Removing
def test_remove_dream_owner():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    
    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user3["token"], channel["channel_id"])
    channel_join_v2(user["token"], channel["channel_id"])

    message_info = message_send_v2(user2["token"], channel["channel_id"], "lol")
    m_id = message_info.get("message_id")

    message_remove_v1(user["token"], m_id)

    messages1 = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    assert messages1 == {'end': -1, 'messages': [], 'start': 0}

# MESSAGE SENDDM TESTING ------------------------------------------------------------------------

# Empty Message
def test_senddm_empty_message():
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
def test_senddm_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    invalid_token = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm["dm_id"], "Thomas Chen")


# invalid dm_ID
def test_senddm_invalid_dm_ID():
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
def test_no_channel_or_dm_specified ():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"This is a message")
    message = ""
    channel_id = -1
    dm_id = -1
    with pytest.raises(InputError):
        message_share_v1(user1["token"],og_message_id,message,channel_id,dm_id)

def test_final_message_too_long_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel2 = channels_create_v2(user1["token"], "testchannel2", True)
    og_message_id = message_send_v2(user1["token"],channel['channel_id'],'x')
    message = 'x' * 1000
    dm_id = -1
    
    with pytest.raises(InputError):
        message_share_v1(user1["token"], og_message_id["message_id"], message,channel2['channel_id'], dm_id)

def test_final_message_too_long_dm ():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)

    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])

    og_message_id = message_send_v2(user1["token"],channel['channel_id'],"x")
    message = 'x' * 1000
    channel_id = -1

    with pytest.raises(InputError):
        message_share_v1(user1["token"],og_message_id["message_id"],message,channel_id,dm["dm_id"])

def test_final_message_is_empty_channel ():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    og_message_id = 3
    message = ''
    dm_id = -1
    
    with pytest.raises(InputError):
        message_share_v1(user1["token"], og_message_id, message,channel['channel_id'], dm_id)


def test_final_message_is_empty_dm():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    og_message_id = 3
    message = ''
    channel_id = -1

    with pytest.raises(InputError):
        message_share_v1(user1["token"],og_message_id,message,channel_id,dm["dm_id"])

def test_dm_to_dm():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    dm2 = dm_create_v1(user1["token"], [user3["auth_user_id"]])

    og_message_id = message_senddm_v1(user1["token"],dm['dm_id'],'This is a message')
    message = ''
    channel_id = -1

    message_share_v1(user1["token"],og_message_id["message_id"],message,channel_id,dm2["dm_id"])
    messages1 = dm_messages_v1(user1["token"], dm2["dm_id"], 0)

    assert messages1["messages"][0]["message_id"] == 2
    assert messages1["messages"][0]["message"] == '\n\n"""\nThis is a message\n"""'
    assert messages1["messages"][0]["u_id"] == user1["auth_user_id"]

def test_dm_to_channel():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    channel = channels_create_v2(user1["token"], "testchannel", True)

    og_message_id = message_senddm_v1(user1["token"],dm['dm_id'],'This is a message')
    message = ''
    dm_id = -1

    message_share_v1(user1["token"],og_message_id["message_id"],message,channel['channel_id'],dm_id)
    messages1 = channel_messages_v2(user1["token"], channel["channel_id"], 0)

    for msg in messages1["messages"]:
        assert msg["message_id"] == 2
        assert msg["message"] == '\n\n"""\nThis is a message\n"""'
        assert msg["u_id"] == user1["auth_user_id"]


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

    m_id = message_sendlater_v1(user1["token"], channel["channel_id"], "i'll see you in the future", time_set)
    
    message_info = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    assert len(message_info["messages"]) == 0

    sleep(3)

    message_info_later = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    
    for messages1 in message_info_later["messages"]:
        if messages1["u_id"] is user1["auth_user_id"]:
            assert messages1["message"] == "i'll see you in the future"
            assert messages1["time_created"] == time_set
            assert messages1["message_id"] == m_id["message_id"]


# Comprehensive Testing
def testsendlater_valid_case_comprehensive():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    time_set = int(datetime.timestamp(datetime.now()) + 2)

    m_id = message_sendlater_v1(user1["token"], channel["channel_id"], "i'll see you in the future", time_set)
    assert m_id["message_id"] == 1

    message_send_v2(user2["token"], channel["channel_id"], "lol i'll see you now")
    
    message_info = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    assert len(message_info["messages"]) == 1

    sleep(3)

    message_info_later = channel_messages_v2(user1["token"], channel["channel_id"], 0)
    
    for messages1 in message_info_later["messages"]:
        if messages1["u_id"] is user1["auth_user_id"]:
            assert messages1["message"] == "i'll see you in the future"
            assert messages1["time_created"] == time_set
            assert messages1["message_id"] == m_id["message_id"]
        
        if messages1["u_id"] is user2["auth_user_id"]:
            assert messages1["message"] == "lol i'll see you now"
            assert messages1["message_id"] == 2


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
    _ = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user["token"], "invalid_id", "Imagine Trump saying Jonathan", time)


# Empty Message
def testsendlaterdm_empty_message():
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
def testsendlaterdm_time_in_past():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) - 2)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user["token"], dm["dm_id"], "Imagine Trump saying Jonathan", time)


# Valid Case Testing
def testsendlaterdm_valid_case():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    time = int(datetime.timestamp(datetime.now()) + 2)

    m_id = message_sendlaterdm_v1(user2["token"], dm["dm_id"], "Imagine Trump saying Jonathan", time)

    dm_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)
    
    assert len(dm_info["messages"]) == 0
    
    sleep(3)

    dm_info_later = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for dms in dm_info_later["messages"]:
        if dms["u_id"] is user2["auth_user_id"]:
            assert dms["message"] == "Imagine Trump saying Jonathan"
            assert dms["time_created"] == time
            assert dms["message_id"] == m_id["message_id"]


# Comprehensive Case Testing
def testsendlaterdm_valid_case_comprehensive():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])

    time_set = int(datetime.timestamp(datetime.now()) + 2)

    m_id = message_sendlaterdm_v1(user1["token"], dm["dm_id"], "i'll see you in the future", time_set)
    assert m_id["message_id"] == 1

    message_senddm_v1(user2["token"], dm["dm_id"], "lol i'll see you now")
    
    dm_info = dm_messages_v1(user2["token"], dm["dm_id"], 0) 
    assert len(dm_info["messages"]) == 1

    sleep(3)

    dm_info_later = dm_messages_v1(user2["token"], dm["dm_id"], 0) 
    
    for messages1 in dm_info_later["messages"]:
        if messages1["u_id"] is user1["auth_user_id"]:
            assert messages1["message"] == "i'll see you in the future"
            assert messages1["time_created"] == time_set
            assert messages1["message_id"] == m_id["message_id"]
        
        if messages1["u_id"] is user2["auth_user_id"]:
            assert messages1["message"] == "lol i'll see you now"
            assert messages1["message_id"] == 2
        

# MESSAGE REACT TESTING -----------------

# Invalid Token
def testreact_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    invalid_token = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_react_v1(invalid_token, m_id, 1)


# Invalid Message ID
def testreact_invalid_message_ID():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    _ = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")

    with pytest.raises(InputError):
        message_react_v1(user["token"], "invalid_mid", 1)


# Invalid React ID
def testreact_invalid_react_ID():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(InputError):
        message_react_v1(user["token"], m_id, "invalid_reactID")


# User not in channel
def testreact_not_in_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_react_v1(user2["token"], m_id, 1)


# User not in DM
def testreact_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user["token"], dm["dm_id"], "Jonathan Chen")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_react_v1(user3["token"], m_id, 1)


# Message already reacted
def testreact_already_reacted():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1)    

    with pytest.raises(InputError):
        message_react_v1(user["token"], m_id, 1)    


# Valid Case for Channel Message React
def testreact_valid_case_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1)    

    message_info = channel_messages_v2(user["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [user["auth_user_id"]],
                "is_this_user_reacted": True,
            }]

# Valid Case for DM Message React
def testreact_valid_case_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")
    message_react_v1(user["token"], message1["message_id"], 1)

    message_info = dm_messages_v1(user["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [user["auth_user_id"]],
                "is_this_user_reacted": True,
            }]


# MESSAGE UNREACT TESTING -----------------

# Invalid Token
def testunreact_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1) 
    invalid_token = jwt.encode({"sessionId": 32132}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_unreact_v1(invalid_token, m_id, 1)


# Invalid Message ID
def testunreact_message_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1) 

    with pytest.raises(InputError):
        message_unreact_v1(user["token"], "invalid_mID", 1)


# Invalid React ID
def testunreact_react_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1) 

    with pytest.raises(InputError):
        message_unreact_v1(user["token"], m_id, "invalid_reactID")


# Message does not contain an active react
def testunreact_no_reacts_unreact():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(InputError):
        message_unreact_v1(user["token"], m_id, 1)


# Unreacting an already unreacted message
def testunreact_unreacting_unreacted_msg():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1) 
    message_unreact_v1(user["token"], m_id, 1)

    with pytest.raises(InputError):
        message_unreact_v1(user["token"], m_id, 1)


# User not in channel to unreact
def testunreact_user_not_in_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)

    channel_join_v2(user2["token"], channel["channel_id"])
 
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')
    message_react_v1(user2["token"], m_id, 1) 

    channel_leave_v1(user2["token"], channel["channel_id"])

    with pytest.raises(AccessError):
        message_unreact_v1(user2["token"], m_id, 1)


# User not in dm to unreact
def testunreact_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    message1 = message_senddm_v1(user["token"], dm["dm_id"], "omg it's thomas chen")
    m_id = message1.get('message_id')
    message_react_v1(user3["token"], m_id, 1) 

    dm_leave_v1(user3["token"], dm["dm_id"])

    with pytest.raises(AccessError):
        message_unreact_v1(user3["token"], m_id, 1)


# Valid case for Channel
def testunreact_valid_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_react_v1(user["token"], m_id, 1)    

    message_info = channel_messages_v2(user["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [user["auth_user_id"]],
                "is_this_user_reacted": True,
            }]

    message_unreact_v1(user["token"], m_id, 1)

    message_info_later = channel_messages_v2(user["token"], channel["channel_id"], 0)

    for msg in message_info_later["messages"]:
        if msg["u_id"] is user["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": False,
            }]


# Valid Case for DM
def testunreact_valid_case_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")
    message_react_v1(user["token"], message1["message_id"], 1)

    message_info = dm_messages_v1(user["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [user["auth_user_id"]],
                "is_this_user_reacted": True,
            }]

    message_unreact_v1(user["token"], message1["message_id"], 1)

    message_info_later = dm_messages_v1(user["token"], dm["dm_id"], 0)

    for msg in message_info_later["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["reacts"] == [{
                "react_id": 1,
                "u_ids": [],
                "is_this_user_reacted": False,
            }]



# MESSAGE PIN TESTING -----------------

# Invalid Token
def testpin_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    invalid_token = jwt.encode({"sessionId": 32132}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_pin_v1(invalid_token, m_id)


# Invalid Message ID
def testpin_invalid_message_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    _ = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")

    with pytest.raises(InputError):
        message_pin_v1(user["token"], "invalid_mID")


# Message already pinned
def testpin_already_pinned():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    with pytest.raises(InputError):
        message_pin_v1(user["token"], m_id)


# User not in channel
def testpin_user_not_in_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)

    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_pin_v1(user2["token"], m_id)


# User not in dm
def testpin_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "omg it's jonathan qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_pin_v1(user3["token"], m_id)


# User is not an owner of the channel
def testpin_user_not_owner_of_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_pin_v1(user2["token"], m_id)


# User not owner of dm
def testpin_user_not_owner_of_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "omg it's jonathan qiu")
    m_id = message1.get('message_id')

    with pytest.raises(AccessError):
        message_pin_v1(user3["token"], m_id)


# Valid Case for Channel
def testpin_valid_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    message_info = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True


# Valid Case for DM
def testpin_valid_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")
    message_pin_v1(user["token"], message1["message_id"])

    message_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True


# Dream Owner Check
def testpin_dream_owner():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user3["token"], channel["channel_id"])
    channel_join_v2(user["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)
    
    message_info = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True



# MESSAGE UNPIN TESTING -----------------

# Invalid Token
def testunpin_invalid_token():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    invalid_token = jwt.encode({"sessionId": 32132}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        message_unpin_v1(invalid_token, m_id)


# Invalid Message ID
def testunpin_invalid_message_id():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")

    message_pin_v1(user["token"], message1["message_id"])

    with pytest.raises(InputError):
        message_unpin_v1(user["token"], "invalid_mID")


# Message already unpinned
def testunpin_already_unpinned():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    message_unpin_v1(user["token"], m_id)

    with pytest.raises(InputError):
        message_unpin_v1(user["token"], m_id)


# User not in channel
def testunpin_user_not_in_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])
    channel_addowner_v1(user["token"], channel["channel_id"], user2["auth_user_id"])

    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user2["token"], m_id)

    channel_leave_v1(user2["token"], channel["channel_id"])

    with pytest.raises(AccessError):
        message_unpin_v1(user2["token"], m_id)
  

# User not in dm
def testunpin_user_not_in_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "omg it's jonathan qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    with pytest.raises(AccessError):
        message_unpin_v1(user3["token"], m_id)


# User is not an owner of the channel
def testunpin_user_not_owner_of_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)
    
    with pytest.raises(AccessError):
        message_unpin_v1(user2["token"], m_id)


# User not owner of dm
def testunpin_user_not_owner_of_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "omg it's jonathan qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    with pytest.raises(AccessError):
        message_unpin_v1(user2["token"], m_id)


# Valid Case for Channel
def testunpin_valid_channel():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user["token"], m_id)

    message_info = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True

    message_unpin_v1(user["token"], m_id)

    message_info_later = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info_later["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == False


# Valid Case for DM
def testunpin_valid_dm():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    dm = dm_create_v1(user["token"], [user2["auth_user_id"]])

    message1 = message_senddm_v1(user2["token"], dm["dm_id"], "Jonathan")
    message_pin_v1(user["token"], message1["message_id"])

    message_info = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True

    message_unpin_v1(user["token"], message1["message_id"])

    message_info_later = dm_messages_v1(user2["token"], dm["dm_id"], 0)

    for msg in message_info_later["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == False


# Dream Owner Check
def testunpin_dream_owner():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    channel = channels_create_v2(user2["token"], "testchannel", True)
    channel_join_v2(user3["token"], channel["channel_id"])
    channel_join_v2(user["token"], channel["channel_id"])

    message1 = message_send_v2(user2["token"], channel["channel_id"], "Thomas Qiu")
    m_id = message1.get('message_id')

    message_pin_v1(user2["token"], m_id)
    
    message_info = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == True

    message_unpin_v1(user["token"], m_id)

    message_info_later = channel_messages_v2(user2["token"], channel["channel_id"], 0)

    for msg in message_info_later["messages"]:
        if msg["u_id"] is user2["auth_user_id"]:
            assert msg["is_pinned"] == False
    
