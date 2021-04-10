import src.database as database
from src.error import InputError
from src.utils import get_user_id_from_token


def notifications_get_v1(token):
    userId = get_user_id_from_token(token)
    for user in database.data["accData"]:
        if user["id"] == userId:
            notificationList = user["notifications"].copy()
            notificationList.reverse()
            return {"notifications": notificationList[:20]}
    raise InputError(description="User not found")
