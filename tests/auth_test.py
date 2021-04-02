import pytest
import re
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
    assert user1 == {'auth_user_id': user1["auth_user_id"]}
    assert user2 == {'auth_user_id': user2["auth_user_id"]}
    assert user3 == {'auth_user_id': user3["auth_user_id"]}



def test_auth_register_v1_except():
    # Testing cases where register should not work
    clear_v1()

    # Email not valid
    with pytest.raises(InputError):
        assert auth_register_v1("error@becauseofau.com.au", "testPassword", "John", "Doe") == InputError
    
    # Password < 6 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "error", "John", "Doe") == InputError

    # First name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "Error"*11, "Doe") == InputError

    # Last name > 50 characters
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "John", "Error"*11) == InputError

    # First name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "", "Doe") == InputError

    # Last name < 1 character
    with pytest.raises(InputError):
        assert auth_register_v1("testemail@institute.com", "testPassword", "John", "") == InputError

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

    # Should work
    assert auth_login_v1("testemail@institute.com", "testPassword") == {'auth_user_id': user1["auth_user_id"]}
    assert auth_login_v1("newemail@google.co", "Newpassword") == {'auth_user_id': user2["auth_user_id"]}

def test_auth_login_v1_except():
    # Testing cases where login that should not work
    clear_v1()

    auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe")
    auth_register_v1("newemail@google.co", "Newpassword", "Jane", "Doe")
    auth_register_v1("testemail@hotmail.com", "testpassword", "First", "Last")

    # Wrong password, using another registered password
    with pytest.raises(InputError):
        auth_login_v1("testemail@institute.com", "testpassword")

    # Not registered
    with pytest.raises(InputError):
        auth_login_v1("notregistered@hotmail.com", "newpassword")
    
    # Typo in email
    with pytest.raises(InputError):
        auth_login_v1("testmail@institute.com", "testpassword")
    
    # Invalid email
    with pytest.raises(InputError):
        auth_login_v1("testmail@hotmail.com.au", "testpassword")
    
    # Wrong password
    with pytest.raises(InputError):
        auth_login_v1("notregistered@hotmail.com", "wrongpassword")
# ------------------------------------------------------------------------------------------------------
