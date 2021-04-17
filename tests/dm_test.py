import pytest
import jwt
import src.config as config
from flask import request
from src.other import clear_v1
from src.dm import dm_create_v1, dm_invite_v1, dm_leave_v1, dm_list_v1, dm_messages_v1, dm_remove_v1, dm_details_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, checkOwner
from src.channels import channels_create_v2, channels_list_v2
import src.database as database
from src.dm import make_dm_name, dm_create_v1

# ------------------------------------------------------------------------------------------------------
#dm create tests

def test_dm_create_single():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]
    dm = dm_create_v1(user["token"], id_list)
    assert dm == {'dm_id': 0, 'dm_name': 'namelastname,onelastname'}

def test_dm_create_multiple_dms():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "awo", "Lastname")
    id_list = []
    id_list.append(user.get("auth_user_id"))
    id_list.append(user2.get("auth_user_id"))
    id_list2 = [user1.get("auth_user_id")]
    test = dm_create_v1(user1["token"], id_list)
    dm = dm_create_v1(user["token"], id_list2)

    assert test == {'dm_id': 0, 'dm_name': 'awolastname,namelastname,onelastname'}
    assert dm == {'dm_id': 1, 'dm_name': 'namelastname,onelastname'}
   
def test_dm_create_invalid_token():

    clear_v1()

    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert dm_create_v1(invalid_id, id_list) == AccessError

def test_dm_create_invalid_user():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id"), 67]
    with pytest.raises(InputError):
        dm_create_v1(user["token"], id_list)
    
# ------------------------------------------------------------------------------------------------------
# DM List Tests
    
def test_dm_list_once():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "awo", "Lastname")
    id_list = []
    id_list.append(user.get("auth_user_id"))
    id_list.append(user2.get("auth_user_id"))
    dm_create_v1(user1["token"], id_list)
    list1 = dm_list_v1(user["token"])
    assert list1 == {'dms': [{'dm_id': 0, 'dm_name': 'awolastname,namelastname,onelastname'}]}
   

def test_dm_list_multiple():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "awo", "Lastname")
    id_list = []
    id_list.append(user.get("auth_user_id"))
    id_list.append(user2.get("auth_user_id"))
    id_list2 = [user1.get("auth_user_id")]
    dm_create_v1(user1["token"], id_list)
    list1 = dm_list_v1(user["token"])
    assert list1 == {'dms': [{'dm_id': 0, 'dm_name': 'awolastname,namelastname,onelastname'}]}
    dm_create_v1(user["token"], id_list2)
    list2 = dm_list_v1(user["token"])
    assert list2 == {'dms': [{'dm_id': 0, 'dm_name': 'awolastname,namelastname,onelastname'}, {'dm_id': 1, 'dm_name': 'namelastname,onelastname'}]}

def test_dm_list_invalidtoken():

    clear_v1()
    invalid_id = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert dm_list_v1(invalid_id) == AccessError

# ------------------------------------------------------------------------------------------------------
# DM Invite Tests

def test_dm_invite_one():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "awo", "Lastname")
    id_list = [user1.get("auth_user_id")]
    dm_create_v1(user["token"], id_list)
    assert database.data["dmList"][0]["member_ids"] == [0, 1]

    dm_invite_v1(user["token"], 0, user2.get("auth_user_id"))
    assert database.data["dmList"][0]["member_ids"] == [0, 1, 2]

def test_dm_invite_multiple():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "awo", "Lastname")
    id_list = [user1.get("auth_user_id")]
    dm_create_v1(user["token"], id_list)
    assert database.data["dmList"][0]["member_ids"] == [0, 1]

    dm_invite_v1(user["token"], 0, user2.get("auth_user_id"))
    assert database.data["dmList"][0]["member_ids"] == [0, 1, 2]

    user3 = auth_register_v2("three@gmail.com", "password", "three", "Lastname")
    dm_invite_v1(user1["token"], 0, user3.get("auth_user_id"))
    assert database.data["dmList"][0]["member_ids"] == [0, 1, 2, 3]

    user4 = auth_register_v2("four@gmail.com", "password", "four", "Lastname")
    user5 = auth_register_v2("five@gmail.com", "password", "five", "Lastname")
    dm_invite_v1(user3["token"], 0, user5.get("auth_user_id"))
    dm_invite_v1(user3["token"], 0, user4.get("auth_user_id"))
    assert database.data["dmList"][0]["member_ids"] == [0, 1, 2, 3, 5, 4]

def test_dm_invite_invalid_dm():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user1_id = user1.get("auth_user_id")
    invalid_dm_id = 4
    with pytest.raises(InputError):
        assert dm_invite_v1(user["token"], invalid_dm_id, user1_id) == InputError

def test_dm_invite_invalid_uid():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]
    dm_create_v1(user["token"], id_list)

    invalid_id = 8
    with pytest.raises(InputError):
        assert dm_invite_v1(user["token"], 0, invalid_id) == InputError
  
def test_dm_inviter_not_in_dm():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    user2 = auth_register_v2("two@gmail.com", "password", "Two", "Lastname")
    user3 = auth_register_v2("three@gmail.com", "password", "Three", "Lastname")
    user3_id = user3.get("auth_user_id")
    id_list = [user1.get("auth_user_id")]
    dm_create_v1(user["token"], id_list)

    with pytest.raises(AccessError):
        assert dm_invite_v1(user2["token"], 0, user3_id) == AccessError
# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_messages_v1 tests:
    # Main Implementation
def test_dm_messages():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)

    messages = dm_messages_v1(user["token"], dm["dm_id"], 0)
    
    assert messages == {'messages': [], 'start': 0, 'end': -1}

def test_dm_messages_invalid_userid():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)
    
    temp = jwt.encode({"sessionId": "notInt"}, database.secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        dm_messages_v1(temp, dm["dm_id"], 0)

def test_dm_messages_invalid_dmid():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm_create_v1(user["token"], id_list)
    
    with pytest.raises(InputError):
        dm_messages_v1(user["token"], "invalid_dm_id", 0)

def test_dm_messages_unauthorised_user():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)
    
    with pytest.raises(AccessError):
        dm_messages_v1(user3["token"], dm["dm_id"], 0)
    
def test_dm_messages_startgreater():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)

    with pytest.raises(InputError):
        assert dm_messages_v1(user["token"], dm["dm_id"], 1)

def test_dm_messages_endnegativeone():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)

    messages = dm_messages_v1(user["token"], dm["dm_id"], 0)
    assert messages["end"] == -1

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_leave_v1 tests:
    # Main Implementation
def test_dm_leave():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)

    dm_leave_v1(user2["token"], dm["dm_id"])

    assert dm_list_v1(user2["token"]) == {'dms': []}
    

    # Main Multiple Implementation
 
def test_dm_leave_multiple():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")
    user4 = auth_register_v2("email4@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user2["auth_user_id"])
    id_list.append(user3["auth_user_id"])
    id_list.append(user4["auth_user_id"])
    dm = dm_create_v1(user["token"], id_list)

    dm_leave_v1(user2["token"], dm["dm_id"])
    assert dm_list_v1(user2["token"]) == {'dms': []}

    dm_leave_v1(user3["token"], dm["dm_id"])
    assert dm_list_v1(user2["token"]) == {'dms': []}

    dm_leave_v1(user4["token"], dm["dm_id"])
    assert dm_list_v1(user2["token"]) == {'dms': []}

    # DM ID is not a valid dm

def test_dm_leave_invalid_dm():

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    with pytest.raises(InputError):
        dm_leave_v1(user2["token"], "invalid_dm_id")
 

    # Authorised user is not a member of dm with dm_id

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    with pytest.raises(AccessError):
        dm_leave_v1(user3["token"], dm["dm_id"])

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_remove_v1 tests:
    # Main Implementation
    
def test_dm_remove():
    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    dm_remove_v1(user["token"], dm["dm_id"])

    assert dm_list_v1(user["token"]) == {'dms': []}
    assert dm_list_v1(user2["token"]) == {'dms': []}

    # Multiple main Implementations
def test_dm_remove_multiple():
    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    dm2 = dm_create_v1(user2["token"], id_list)

    dm_remove_v1(user["token"], dm["dm_id"])
    dm_remove_v1(user2["token"], dm2["dm_id"])

    assert dm_list_v1(user["token"]) == {'dms': []}
    assert dm_list_v1(user2["token"]) == {'dms': []}

    # The user is not the original DM creator
def test_dm_remove_not_owner():

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    with pytest.raises(AccessError):
         dm_remove_v1(user2["token"], dm["dm_id"])

    # Dm_id does not refer to a valid DM

def test_dm_remove_invalid_dm():

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm_create_v1(user["token"], id_list)

    with pytest.raises(InputError):
         dm_remove_v1(user2["token"], "invalid_dm_id")

    # Invalid token is used
def test_dm_remove_invalid_token():

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    temp = jwt.encode({"sessionId": 2}, database.secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
         dm_remove_v1(temp, dm["dm_id"])

# ------------------------------------------------------------------------------------------------------
#dm details tests

def test_dm_does_not_exist():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    _ = dm_create_v1(user1["token"], id_list)

    with pytest.raises(InputError):
        dm_details_v1(user1['token'],21423431)

def test_user_not_member_of_dm():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user1["token"], id_list)
    

    with pytest.raises(AccessError):
        dm_details_v1(user3['token'],dm['dm_id'])


def test_valid_input():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    dm = dm_create_v1(user1["token"], [user2["auth_user_id"]])    

    assert dm_details_v1(user1['token'], dm['dm_id']) == {
                                            'name': 'namelastname,namelastname0',
                                            'members': [
                                                {
                                                    'u_id': user1["auth_user_id"],
                                                    'email': 'email@gmail.com',
                                                    'name_first': 'Name',
                                                    'name_last': 'Lastname',
                                                    'profile_img_url': f"{config.url}static/default.jpg",
                                                    'handle_str': 'namelastname',
                                                    
                                                },
                                                {
                                                    'u_id': user2["auth_user_id"],
                                                    'email': 'email2@gmail.com',
                                                    'name_first': 'Name',
                                                    'name_last': 'Lastname',
                                                    'profile_img_url': f"{config.url}static/default.jpg",
                                                    'handle_str': 'namelastname0',   
                                                }
                                            ],
                                           }