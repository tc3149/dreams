import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, checkOwner
from src.channels import channels_create_v2, channels_list_v2
from src.database import data, secretSauce
from src.dm import make_dm_name, dm_create_v1, dm_leave_v1, dm_list_v1, dm_remove_v1

# ------------------------------------------------------------------------------------------------------
#dm create tests

def test_dm_create_single():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]

    dm = dm_create_v1(user["token"], id_list)
    assert dm == {'dm_id': 0, 'dm_name': 'namelastname,onelastname'}

def test_dm_create_multiple():

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

def test_dm_invalid_token():

    clear_v1()

    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]
    invalid_id = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")
    with pytest.raises(AccessError):
        assert dm_create_v1(invalid_id, id_list) == AccessError


# def test_dm_invalid_token():
# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_messages_v1 tests:
    # Main Implementation
#def test_dm_messages():

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_leave_v1 tests:
    # Main Implementation
def test_dm_leave():
    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    id_list = []
    id_list.append(user["auth_user_id"])
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
    id_list.append(user["auth_user_id"])
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

    # DM ID is not a valid channel

def test_dm_leave_invalid_dm():

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user["auth_user_id"])
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    with pytest.raises(InputError):
        dm_leave_v1(user2["token"], "invalid_dm_id")
 

    # Authorised user is not a member of channel with channel_id

    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user["auth_user_id"])
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    temp = jwt.encode({"sessionId": 2}, secretSauce, algorithm = "HS256")

    with pytest.raises(AccessError):
        dm_leave_v1(temp, dm["dm_id"])

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# dm_remove_v1 tests:
    # Main Implementation
    
def test_dm_remove():
    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user["auth_user_id"])
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    dm_remove_v1(user["token"], dm["dm_id"])

    assert dm_list_v1(user["token"]) == {'dms': []}
    assert dm_list_v1(user2["token"]) == {'dms': []}

    # Muyltiple main Implementations
def test_dm_remove_multiple():
    clear_v1()

    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    id_list = []
    id_list.append(user["auth_user_id"])
    id_list.append(user2["auth_user_id"])

    dm = dm_create_v1(user["token"], id_list)

    dm2 = dm_create_v1(user2["token"], id_list)

    dm_remove_v1(user["token"], dm["dm_id"])
    dm_remove_v1(user2["token"], dm2["dm_id"])

    assert dm_list_v1(user["token"]) == {'dms': []}
    assert dm_list_v1(user2["token"]) == {'dms': []}

# ------------------------------------------------------------------------------------------------------