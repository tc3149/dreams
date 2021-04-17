from src.auth import auth_register_v2
from src.other import clear_v1
from src.notifications import notifications_get_v1
from src.error import AccessError
import pytest
import jwt


def test_notifications_working():
    clear_v1()

    user1 = auth_register_v2("testemail@hotmail.com", "password1", "firstName", "lastName")
    returnData = notifications_get_v1(user1["token"])

    assert returnData["notifications"] == []

def test_notifications_invalid_token():
    clear_v1()

    invalidToken = jwt.encode({"sessionId": 6}, "test", algorithm="HS256")

    with pytest.raises(AccessError):
        notifications_get_v1(invalidToken)

