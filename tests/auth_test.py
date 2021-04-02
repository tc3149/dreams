import jwt
import pytest
import re
from src.database import accData, secretSauce
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1

# ------------------------------------------------------------------------------------------------------
# auth_register_v1 tests
def test_auth_register_v1():
    # Testing if register works
    clear_v1()

    user1 = auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    user2 = auth_register_v1("newemail@google.co", "Newpassword", "Jane", "Doe")
    user3 = auth_register_v1("testemail@hotmail.com", "testpassword", "First", "Last")
    user1JWT = jwt.encode({'auth_user_id': user1["auth_user_id"]}, secretSauce, algorithm="HS256")
    user2JWT = jwt.encode({'auth_user_id': user2["auth_user_id"]}, secretSauce, algorithm="HS256")
    user3JWT = jwt.encode({'auth_user_id': user3["auth_user_id"]}, secretSauce, algorithm="HS256")

    assert user1 == {'token': user1JWT, "auth_user_id": user1["auth_user_id"]}
    assert user2 == {'token': user2JWT, "auth_user_id": user2["auth_user_id"]}
    assert user3 == {'token': user3JWT, "auth_user_id": user3["auth_user_id"]}




def test_auth_register_v1_invalid_email():
    # Testing cases where register should not work
    clear_v1()

    # Email not valid
    with pytest.raises(InputError):
        assert auth_register_v1("error@becauseofau.com.au", "testPassword", "John", "Doe") == InputError
    
def test_auth_register_v1_short_password():
    clear_v1()

    # Password < 6 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "error", "John", "Doe") == InputError

def test_auth_register_v1_long_first():
    clear_v1()

    # First name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "Error"*11, "Doe") == InputError

def test_auth_register_v1_long_last():
    clear_v1()

    # Last name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "John", "Error"*11) == InputError

def test_auth_register_v1_short_first():
    clear_v1()

    # First name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "", "Doe") == InputError

def test_auth_register_v1_short_last():
    clear_v1()

    # Last name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "John", "") == InputError

def test_auth_register_v1_email_taken():
    clear_v1()

    # Email already registered
    auth_register_v1("taken@email.com", "testPassword", "John", "Doe")
    with pytest.raises(InputError):
        assert auth_register_v1("taken@email.com", "testPassword", "John", "Doe") == InputError

def test_auth_register_handle_limit():
    # Checking handles
    clear_v1()

    user1 = auth_register_v1("email@hotmail.com", "testpassword", "ReallyReallyReally", "LongName")
    user2 = auth_register_v1("email2@hotmail.com", "testpassword", "ReallyReally", "LongName")
    channel1 = channels_create_v1(user1["auth_user_id"], "testchannel", True)
    channel_join_v1(user2["auth_user_id"], channel1["channel_id"])
    channelDetailsHandle = channel_details_v1(user1["auth_user_id"], channel1["channel_id"])
    
    assert channelDetailsHandle["all_members"][0]["handle_str"] == "reallyreallyreallylo"
    assert channelDetailsHandle["all_members"][1]["handle_str"] == "reallyreallylongname"
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# auth_login_v1 tests
def test_auth_login_v1():
    # Testing if login works
    clear_v1()

    user1 = auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    user2 = auth_register_v1("newemail@google.co", "Newpassword", "Jane", "Doe")

    dummy1 = jwt.encode({'auth_user_id': user1["auth_user_id"]}, secretSauce, algorithm="HS256")
    dummy2 = jwt.encode({'auth_user_id': user2["auth_user_id"]}, secretSauce, algorithm="HS256")
    # Should work
    assert auth_login_v1("testemail@institute.com", "testPassword") == {"token": dummy1,
                                                                        'auth_user_id': user1["auth_user_id"]}
    assert auth_login_v1("newemail@google.co", "Newpassword") == {"token": dummy2,
                                                                  'auth_user_id': user2["auth_user_id"]}

def test_auth_login_v1_except():
    # Testing cases where login that should not work
    clear_v1()

    auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    auth_register_v1("testemail@hotmail.com", "testpassword", "First", "Last")

    # Wrong password, using another registered password
    with pytest.raises(InputError):
        auth_login_v1("testemail@institute.com", "testpassword")

def test_auth_login_v1_not_registered():
    clear_v1()

    # Not registered
    with pytest.raises(InputError):
        auth_login_v1("notregistered@hotmail.com", "newpassword")
    
def test_auth_login_v1_unregistered_email():
    clear_v1()

    auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    # Typo in email
    with pytest.raises(InputError):
        auth_login_v1("testmails@institute.com", "testPassword")
    
def test_auth_login_v1_invalid_email():
    clear_v1()

    auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    # Invalid email
    with pytest.raises(InputError):
        auth_login_v1("testmail@hotmail.com.au", "testPassword")
    
def test_auth_login_v1_invalid_password():
    clear_v1()

    auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    # Wrong password
    with pytest.raises(InputError):
        auth_login_v1("testemail@institute.com", "wrongpassword")
# ------------------------------------------------------------------------------------------------------
