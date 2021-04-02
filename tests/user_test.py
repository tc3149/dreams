import pytest
from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.user import user_profile_v2
from src.user import user_profile_setname_v2
from src.user import user_profile_sethandle_v1
from src.user import user_profile_setemail_v2
from src.user import users_all_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError


# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_v2 TESTS
def test_user_profile_v2_working():
    clear_v1()
    
    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    dummyData = {
        "user": {
            'u_id': user1["auth_user_id"],
            'email': "testemail@hotmail.com",
            'name_first': "firstName",
            'name_last': "lastName",
            'handle_str': "firstnamelastname",
        }
    }
    assert user_profile_v2(user1["auth_user_id"], user1["auth_user_id"]) == dummyData

def test_user_profile_v2_invalid_u_id():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        assert user_profile_v2(user1, 999) == InputError

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_setname_v2 TESTS
def test_user_profile_setname_v2_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user_profile_setname_v2(user1["auth_user_id"], "newFirst", "newLast")
    dummyData = {
                    "user": {
                        'u_id': user1["auth_user_id"],
                        'email': "testemail@hotmail.com",
                        'name_first': "newFirst",
                        'name_last': "newLast",
                        'handle_str': "firstnamelastname",
                    }
                }
    assert user_profile_v2(user1["auth_user_id"], user1["auth_user_id"]) == dummyData

def test_user_profile_setname_v2_first_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "newFirst" * 11, "newLast")

def test_user_profile_setname_v2_last_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "newFirst", "newLast" * 11)

def test_user_profile_setname_v2_first_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "", "newLast")

def test_user_profile_setname_v2_last_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "newFirst", "")

def test_user_profile_setname_v2_both_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "newFirst" * 11, "newLast" * 11)

def test_user_profile_setname_v2_both_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    with pytest.raises(InputError):
        user_profile_setname_v2(user1["auth_user_id"], "", "")

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_sethandle_v1 TESTS
def test_user_profile_sethandle_v1_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")

    user_profile_sethandle_v1(user1["auth_user_id"], "newHandle")
    dummyData = {
                    "user": {
                        'u_id': user1["auth_user_id"],
                        'email': "testemail@hotmail.com",
                        'name_first': "firstName",
                        'name_last': "lastName",
                        'handle_str': "newHandle",
                    }
                }
    assert user_profile_v2(user1["auth_user_id"], user1["auth_user_id"]) == dummyData


def test_user_profile_sethandle_v1_handle_taken():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    user_profile_sethandle_v1(user1["auth_user_id"], "newHandle")
    dummyData = {
                    "user": {
                        'u_id': user1["auth_user_id"],
                        'email': "testemail@hotmail.com",
                        'name_first': "firstName",
                        'name_last': "lastName",
                        'handle_str': "newHandle",
                    }
                }
    assert user_profile_v2(user1["auth_user_id"], user1["auth_user_id"]) == dummyData

    with pytest.raises(InputError):
        user_profile_sethandle_v1(user2["auth_user_id"], "newHandle")

def test_user_profile_sethandle_v1_handle_short():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
                      
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1["auth_user_id"], "aa")

def test_user_profile_sethandle_v1_handle_long():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
                      
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1["auth_user_id"], "aaa" * 10)

# /////////////////////////////////////////////////////////////////////////////////////////////        
# user_profile_setemail_v2 TESTS
def test_user_profile_setemail_v2_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    user_profile_setemail_v2(user1["auth_user_id"], "newEmail@hotmail.com")

    dummyData = {
                    "user": {
                        'u_id': user1["auth_user_id"],
                        'email': "newEmail@hotmail.com",
                        'name_first': "firstName",
                        'name_last': "lastName",
                        'handle_str': "firstnamelastname",
                    }
                }
    assert user_profile_v2(user1["auth_user_id"], user1["auth_user_id"]) == dummyData


def test_user_profile_setemail_v2_invalid_email():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1["auth_user_id"], "newEmail@hotmail.com.au")

def test_user_profile_setemail_v2_email_taken():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    _ = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    with pytest.raises(InputError):
        user_profile_setemail_v2(user1["auth_user_id"], "testemail2@hotmail.com")


# /////////////////////////////////////////////////////////////////////////////////////////////  
# users_all_v1 TESTS
def test_users_all_v1_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    user2 = auth_register_v2("testemail2@hotmail.com", "password2", "firstName2", "lastName2")

    dummyData = [
        {
            'u_id': user1["auth_user_id"],
            'email': "testemail@hotmail.com",
            'name_first': "firstName",
            'name_last': "lastName",
            'handle_str': "firstnamelastname",
        },
        {
            'u_id': user2["auth_user_id"],
            'email': "testemail2@hotmail.com",
            'name_first': "firstName2",
            'name_last': "lastName2",
            'handle_str': "firstname2lastname2",
        }
    ]
    assert users_all_v1(user1["auth_user_id"]) == dummyData

def test_users_all_v1_invalid_token():
    clear_v1()

    _ = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")

    with pytest.raises(AccessError):
        users_all_v1(999)


# /////////////////////////////////////////////////////////////////////////////////////////////  
