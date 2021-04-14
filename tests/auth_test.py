import jwt
import pytest
import re
import src.database as database
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channel import channel_details_v2, channel_join_v2
from src.channels import channels_create_v2

# ------------------------------------------------------------------------------------------------------
# auth_register_v2 tests
def test_auth_register_v2():
    # Testing if register works
    clear_v1()

    user1 = auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    user2 = auth_register_v2("newemail@google.co", "Newpassword", "Jane", "Doe")
    user3 = auth_register_v2("testemail@hotmail.com", "testpassword", "First", "Last")

    assert user1 == {'token': user1["token"], "auth_user_id": user1["auth_user_id"]}
    assert user2 == {'token': user2["token"], "auth_user_id": user2["auth_user_id"]}
    assert user3 == {'token': user3["token"], "auth_user_id": user3["auth_user_id"]}

def test_auth_register_v2_invalid_email():
    # Testing cases where register should not work
    clear_v1()

    # Email not valid
    with pytest.raises(InputError):
        assert auth_register_v2("error@becauseofau.com.au", "testPassword", "John", "Doe") == InputError
    
def test_auth_register_v2_short_password():
    clear_v1()

    # Password < 6 characters
    with pytest.raises(InputError):
        assert auth_register_v2("testemail@institute.com", "error", "John", "Doe") == InputError

def test_auth_register_v2_long_first():
    clear_v1()

    # First name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v2("testemail@institute.com", "testPassword", "Error"*11, "Doe") == InputError

def test_auth_register_v2_long_last():
    clear_v1()

    # Last name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v2("testemail@institute.com", "testPassword", "John", "Error"*11) == InputError

def test_auth_register_v2_short_first():
    clear_v1()

    # First name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v2("testemail@institute.com", "testPassword", "", "Doe") == InputError

def test_auth_register_v2_short_last():
    clear_v1()

    # Last name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v2("testemail@institute.com", "testPassword", "John", "") == InputError

def test_auth_register_v2_email_taken():
    clear_v1()

    # Email already registered
    auth_register_v2("taken@email.com", "testPassword", "John", "Doe")
    with pytest.raises(InputError):
        assert auth_register_v2("taken@email.com", "testPassword", "John", "Doe") == InputError

def test_auth_register_handle_limit():
    # Checking handles
    clear_v1()

    user1 = auth_register_v2("email@hotmail.com", "testpassword", "ReallyReallyReally", "LongName")
    user2 = auth_register_v2("email2@hotmail.com", "testpassword", "ReallyReally", "LongName")
    channel1 = channels_create_v2(user1["token"], "testchannel", True)
    channel_join_v2(user2["token"], channel1["channel_id"])
    channelDetailsHandle = channel_details_v2(user1["token"], channel1["channel_id"])
    
    assert channelDetailsHandle["all_members"][0]["handle_str"] == "reallyreallyreallylo"
    assert channelDetailsHandle["all_members"][1]["handle_str"] == "reallyreallylongname"
# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------
# auth_login_v2 tests
def test_auth_login_v2():
    # Testing if login works
    clear_v1()

    user1 = auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    user2 = auth_register_v2("newemail@google.co", "Newpassword", "Jane", "Doe")

    # Should work
    login1 = auth_login_v2("testemail@institute.com", "testPassword")
    login2 = auth_login_v2("newemail@google.co", "Newpassword")

    assert login1 == {
        "token": login1["token"],
        'auth_user_id': user1["auth_user_id"]
    }
    assert login2 == {
        "token": login2["token"],
        'auth_user_id': user2["auth_user_id"]
    }

def test_auth_login_v2_except():
    # Testing cases where login that should not work
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    auth_register_v2("testemail@hotmail.com", "testpassword", "First", "Last")

    # Wrong password, using another registered password
    with pytest.raises(InputError):
        auth_login_v2("testemail@institute.com", "testpassword")

def test_auth_login_v2_not_registered():
    clear_v1()

    # Not registered
    with pytest.raises(InputError):
        auth_login_v2("notregistered@hotmail.com", "newpassword")
    
def test_auth_login_v2_unregistered_email():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    # Typo in email
    with pytest.raises(InputError):
        auth_login_v2("testmails@institute.com", "testPassword")
    
def test_auth_login_v2_invalid_email():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    # Invalid email
    with pytest.raises(InputError):
        auth_login_v2("testmail@hotmail.com.au", "testPassword")
    
def test_auth_login_v2_invalid_password():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    # Wrong password
    with pytest.raises(InputError):
        auth_login_v2("testemail@institute.com", "wrongpassword")
# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# auth_logout_v1
def test_auth_logout_v1_working():
    clear_v1()

    user1 = auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    expectedOutput = {
        "is_success": True
    }
    testOutput = auth_logout_v1(user1["token"])
    assert testOutput == expectedOutput

def test_auth_logout_v1_invalid_token():
    clear_v1()

    invalidToken = jwt.encode({"invalidKey": 0}, database.secretSauce, algorithm="HS256")
    with pytest.raises(AccessError):
        auth_logout_v1(invalidToken)

def test_auth_logout_v1_inactive_token():
    clear_v1()

    inactiveToken = jwt.encode({"sessionId": 999}, database.secretSauce, algorithm="HS256")
    _ = auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")

    with pytest.raises(AccessError):
        auth_logout_v1(inactiveToken)

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# auth_passwordreset_request_v1
def test_auth_passwordreset_request_v1_working():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    output = auth_passwordreset_request_v1("testemail@institute.com")
    assert output == {}

def test_auth_passwordreset_request_invalid_email():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    with pytest.raises(InputError):
        auth_passwordreset_request_v1("invalid@institute.com")
# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------
# auth_passwordreset_reset_v1
def test_auth_passwordreset_reset_v1_not_working():
    clear_v1()

    auth_register_v2("testemail@institute.com", "testPassword", "John", "Doe")
    auth_passwordreset_request_v1("testemail@institute.com")
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1("invalidcode", "newpassword")
# ------------------------------------------------------------------------------------------------------
