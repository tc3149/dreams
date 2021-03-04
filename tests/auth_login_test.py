import pytest
import re
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError

def test_auth_login():
    # Register test users
    auth_register_v1("testemail@hotmail.com", "testpassword", "First", "Last")
    auth_register_v1("testemail2@hotmail.com", "testpassword", "First", "Last")
    # Should work
    assert auth_login_v1("testemail@hotmail.com", "testpassword") == {'auth_user_id': 0}
    assert auth_login_v1("testemail2@hotmail.com", "testpassword") == {'auth_user_id': 1}

    # Not registered
    with pytest.raises(InputError):
        auth_login_v1("notregistered@hotmail.com", "newpassword")
    
    # Typo in email
    with pytest.raises(InputError):
        auth_login_v1("testmail@hotmail.com", "testpassword")
    
    # Invalid email
    with pytest.raises(InputError):
        auth_login_v1("testmail@hotmail.com.au", "testpassword")
    
    # Wrong password
    with pytest.raises(InputError):
        auth_login_v1("notregistered@hotmail.com", "wrongpassword")
    
