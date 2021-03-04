import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError


def test_auth_register_v1():
    assert auth_register_v1("testemail@institute.com", "testPassword", "John", "Doe") == {'auth_user_id': 1}
    assert auth_register_v1("newemail@google.co", "Newpassword", "Jane", "Doe") == {'auth_user_id': 2}



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
