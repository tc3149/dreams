import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, checkOwner
from src.channels import channels_create_v2, channels_list_v2
from src.database import data, secretSauce
from src.dm import makedmName, dm_create_v1

#dm create tests

def test_dm_create_single():

    clear_v1()
    user = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user1 = auth_register_v2("one@gmail.com", "password", "One", "Lastname")
    id_list = [user1.get("auth_user_id")]

    dm = dm_create_v1(user["token"], id_list)
    print(dm)

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
    