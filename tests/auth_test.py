import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError


def test_auth_register_v1():
    assert auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe") == {'auth_user_id': 0}
    assert auth_register_v1("newemail@google.co", "Newpassword", "Jane", "Doe") == {'auth_user_id': 1}
    assert auth_register_v1("testemail@hotmail.com", "testpassword", "First", "Last") == {'auth_user_id': 2}



def test_auth_register_v1_except():
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

def test_auth_login_v1():
    # Should work
    assert auth_login_v1("testemail@institute.com", "testPassword") == {'auth_user_id': 0}
    assert auth_login_v1("testemail@hotmail.com", "testpassword") == {'auth_user_id': 2}

def test_auth_login_v1_except():
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
    
