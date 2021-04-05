import pytest
import jwt
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, checkOwner
from src.channels import channels_create_v2, channels_list_v2
import src.database as database
from src.dm import make_dm_name, dm_create_v1, dm_leave_v1, dm_list_v1, dm_remove_v1, dm_messages_v1, dm_invite_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.utils import get_user_id_from_token, make_dm_name, valid_userid, valid_dmid
from src.message import message_send_v2

# #################################################################################################################
# admin user remove tests

def test_u_id_does_not_exist():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    _ = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], 3)
def test_auth_user_not_an_owner():
    clear_v1()
    _ = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], user3['auth_user_id'])

def test_auth_user_only_owner():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], user1['auth_user_id'])

def test_successful_removed():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")

    admin_user_remove_v1(user1['token'],user2['auth_user_id'])
    assert valid_userid(user2['auth_user_id']) == False
'''
def test_message_change_removed_user():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    channel = channels_create_v2(user1.get("token"), "testchannel", True)
    channel_invite_v2(user1["token"], channel["channel_id"], user2["auth_user_id"])
    message_send_v2(user2['token'],channelList['channel_id'],'hello channel')
    id_list = []
    id_list.append(user.get("auth_user_id"))
    id_list.append(user2.get("auth_user_id"))
    dm = dm_create_v1(user1["token"], id_list)
    message_senddm_v1(user2["token"],dmList['dm_id'],'hello user1')

    admin_user_remove_v1(user1['token'],user2['auth_user_id'])
'''
    

    


# #################################################################################################################
# admin user permission change tests

def test_user_does_not_exist ():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    _ = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'],3,1)

def test_non_valid_permission_id():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'],user2['auth_user_id'],123)

def test_auth_user_not_owner():
    clear_v1()
    _ = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    user3 = auth_register_v2("email3@gmail.com", "password", "Name", "Lastname")

    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'],user3['auth_user_id'],1)

def test_member_to_owner_permission():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    
    #add user2 as server owner

    admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 1)
    
    assert database.data['accData'][user2['auth_user_id']]['permission'] == 1


def test_owner_to_member_permission():
    clear_v1()
    user1 = auth_register_v2("email@gmail.com", "password", "Name", "Lastname")
    user2 = auth_register_v2("email2@gmail.com", "password", "Name", "Lastname")
    
    #add user2 as server owner

    admin_userpermission_change_v1(user1['token'],user2['auth_user_id'],1)

    admin_userpermission_change_v1(user2['token'],user1['auth_user_id'],2)
   

    assert database.data['accData'][user1['auth_user_id']]['permission'] == 2



