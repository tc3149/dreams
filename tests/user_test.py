import pytest
import src.config as config
from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.user import user_profile_v2, users_stats_v1
from src.user import user_profile_setname_v2, user_profile_uploadphoto_v1
from src.user import user_profile_sethandle_v1
from src.user import user_profile_setemail_v2, user_stats_v1
from src.message import message_send_v2, message_senddm_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.user import users_all_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
import src.database as database
import jwt


# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_v2 TESTS
def test_user_profile_v2_working():
    clear_v1()
    
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")

    expectedOutput = {
        'u_id': user1["auth_user_id"],
        'email': "testemail@hotmail.com",
        'name_first': "firstName",
        'name_last': "lastName",
        'profile_img_url': config.url + 'static/default.jpg',
        'handle_str': "firstnamelastname",
    }
    assert user_profile_v2(user1["token"], user1["auth_user_id"]) == {"user": expectedOutput}

def test_user_profile_v2_invalid_u_id():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_v2(user1["token"], 999)

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_setname_v2 TESTS
def test_user_profile_setname_v2_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = user_profile_setname_v2(user1["token"], "newFirst", "newLast")

    expectedOutput = {
        'u_id': user1["auth_user_id"],
        'email': "testemail@hotmail.com",
        'name_first': "newFirst",
        'name_last': "newLast",
        'profile_img_url': config.url + 'static/default.jpg',
        'handle_str': "firstnamelastname",
    }
    assert user_profile_v2(user1["token"], user1["auth_user_id"]) == {"user": expectedOutput}

def test_user_profile_setname_v2_first_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "newFirst" * 11, "newLast")

def test_user_profile_setname_v2_last_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "newFirst", "newLast" * 11)

def test_user_profile_setname_v2_first_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "", "newLast")

def test_user_profile_setname_v2_last_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "newFirst", "")

def test_user_profile_setname_v2_both_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "newFirst" * 11, "newLast" * 11)

def test_user_profile_setname_v2_both_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["token"], "", "")

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_sethandle_v1 TESTS
def test_user_profile_sethandle_v1_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")

    _ = user_profile_sethandle_v1(user1["token"], "newHandle")

    expectedOutput = {
        'u_id': user1["auth_user_id"],
        'email': "testemail@hotmail.com",
        'name_first': "firstName",
        'name_last': "lastName",
        'profile_img_url': config.url + 'static/default.jpg',
        'handle_str': "newHandle",
    }
    assert user_profile_v2(user1["token"], user1["auth_user_id"]) == {"user": expectedOutput}


def test_user_profile_sethandle_v1_handle_taken():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    _ = user_profile_sethandle_v1(user1["token"], "newHandle")

    expectedOutput = {
        'u_id': user1["auth_user_id"],
        'email': "testemail@hotmail.com",
        'name_first': "firstName",
        'name_last': "lastName",
        'profile_img_url': config.url + 'static/default.jpg',
        'handle_str': "newHandle",
    }
    assert user_profile_v2(user1["token"], user1["auth_user_id"]) == {"user": expectedOutput}

    with pytest.raises(InputError):
        user_profile_sethandle_v1(user2["token"], "newHandle")

def test_user_profile_sethandle_v1_handle_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
                      
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1["token"], "aa")

def test_user_profile_sethandle_v1_handle_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
                      
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1["token"], "aaa" * 10)

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_setemail_v2 TESTS
def test_user_profile_setemail_v2_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    user_profile_setemail_v2(user1["token"], "newEmail@hotmail.com")

    expectedOutput = {
        'u_id': user1["auth_user_id"],
        'email': "newEmail@hotmail.com",
        'name_first': "firstName",
        'name_last': "lastName",
        'profile_img_url': config.url + 'static/default.jpg',
        'handle_str': "firstnamelastname",
    }
    assert user_profile_v2(user1["token"], user1["auth_user_id"]) == {"user": expectedOutput}


def test_user_profile_setemail_v2_invalid_email():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1["token"], "newEmail@hotmail.com.au")

def test_user_profile_setemail_v2_email_taken():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1["token"], "testemail2@hotmail.com")


# /////////////////////////////////////////////////////////////////////////////////////////////  
# users_all_v1 TESTS
def test_users_all_v1_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")


    expectedOutput = [
        {
            'u_id': user1["auth_user_id"],
            'email': "testemail@hotmail.com",
            'name_first': "firstName",
            'name_last': "lastName",
            'profile_img_url': config.url + 'static/default.jpg',
            'handle_str': "firstnamelastname",
        },
        {
            'u_id': user2["auth_user_id"],
            'email': "testemail2@hotmail.com",
            'name_first': "firstName2",
            'name_last': "lastName2",
            'profile_img_url': config.url + 'static/default.jpg',
            'handle_str': "firstname2lastname2",
        }
    ]
    assert users_all_v1(user1["token"]) == {"users": expectedOutput}

def test_users_all_v1_invalid_token():
    clear_v1()

    _ = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    invalidToken = jwt.encode({"invalidKey": "invalidValue"}, database.secretSauce, algorithm="HS256")

    with pytest.raises(AccessError):
        users_all_v1(invalidToken)


# /////////////////////////////////////////////////////////////////////////////////////////////  
# user_stats_v1 TESTS
def test_user_stats_no_channel_no_dm():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    userStats = user_stats_v1(user1["token"])
    expectedOutput = {
        "channels_joined": [{
            "num_channels_joined": 0,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "dms_joined": [{
            "num_dms_joined": 0,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "messages_sent": [{
            "num_messages_sent": 0,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "involvement_rate": 0,
    }
    assert userStats["user_stats"] == expectedOutput

def test_user_stats_channel_dm():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName", "lastName")
    channel1 = channels_create_v2(user1["token"], "NewChannel", True)
    dm1 = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    _ = message_send_v2(user1["token"], channel1["channel_id"], "Test")
    _ = message_senddm_v1(user1["token"], dm1["dm_id"], "Test")

    userStats = user_stats_v1(user1["token"])
    expectedOutput = {
        "channels_joined": [{
            "num_channels_joined": 1,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "dms_joined": [{
            "num_dms_joined": 1,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "messages_sent": [{
            "num_messages_sent": 2,
            "time_stamp": userStats["user_stats"]["channels_joined"][0]["time_stamp"],
        }],
        "involvement_rate": 1.0,
    }
    assert userStats["user_stats"] == expectedOutput

# /////////////////////////////////////////////////////////////////////////////////////////////  
# users_stats_v1
def test_users_stats_no_channel_no_dm():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    dreamsStats = users_stats_v1(user1["token"])
    expectedOutput = {
        "channels_exist": [{
            "num_channels_exist": 0,
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "dms_exist": [{
            "num_dms_exist": 0, 
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "messages_exist": [{
            "num_messages_exist": 0, 
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "utilization_rate": 0,
    }

    assert dreamsStats["dreams_stats"] == expectedOutput

def test_users_stats_channel_dm():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName", "lastName")
    channel1 = channels_create_v2(user1["token"], "NewChannel", True)
    dm1 = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    _ = message_send_v2(user1["token"], channel1["channel_id"], "Test")
    _ = message_senddm_v1(user1["token"], dm1["dm_id"], "Test")
    dreamsStats = users_stats_v1(user1["token"])
    expectedOutput = {
        "channels_exist": [{
            "num_channels_exist": 1,
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "dms_exist": [{
            "num_dms_exist": 1, 
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "messages_exist": [{
            "num_messages_exist": 2, 
            "time_stamp": dreamsStats["dreams_stats"]["channels_exist"][0]["time_stamp"],
            }],
        "utilization_rate": 1.0,
    }

    assert dreamsStats["dreams_stats"] == expectedOutput

# /////////////////////////////////////////////////////////////////////////////////////////////  
# user_profile_uploadphoto_v1 TESTS
# Test requires http connection

def test_user_profile_uploadphoto_working():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    profileURL = "http://personal.psu.edu/xqz5228/jpg.jpg"
    user1Profile = user_profile_v2(user1["token"], user1["auth_user_id"])

    expectedOutput = {
        "u_id": user1["auth_user_id"],
        "email": "testemail@hotmail.com",
        "name_first": "firstName",
        "name_last": "lastName",
        "handle_str": "firstnamelastname",
        "profile_img_url": config.url + "static/default.jpg"
    }
    assert user1Profile["user"] == expectedOutput
    _ = user_profile_uploadphoto_v1(user1["token"], profileURL, 0, 0, 300, 300)

    expectedOutput = {
        "u_id": user1["auth_user_id"],
        "email": "testemail@hotmail.com",
        "name_first": "firstName",
        "name_last": "lastName",
        "handle_str": "firstnamelastname",
        "profile_img_url": user1Profile["user"]["profile_img_url"],
    }
    assert user1Profile["user"] == expectedOutput

def test_user_profile_uploadphoto_crop_out_of_bounds():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    profileURL = "http://personal.psu.edu/xqz5228/jpg.jpg"

    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1["token"], profileURL, 0, 0, 1000, 1000)

def test_user_profile_uploadphoto_not_jpg():
    clear_v1()
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    profileURL = "https://preview.redd.it/an871k4o1sn51.png?width=440&format=png&auto=webp&s=85dcd6cb73b8760802e254ee14dfa3c7ab444591"

    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user1["token"], profileURL, 0, 0, 50, 50)
    clear_v1()
