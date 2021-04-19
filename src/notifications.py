import src.database as database
from src.error import AccessError
from src.utils import get_user_id_from_token



'''
Arguments:
    token (string)      - jwt encrypted session id

Exceptions:
    N/A

Return Value:
    {notifications}  - List of dictionaries, where each dictionary contains types { channel_id, dm_id, notification_message } 
                        where channel_id is the id of the channel that the event happened in, and is -1 if it is being sent to a DM. 
                        dm_id is the DM that the event happened in, and is -1 if it is being sent to a channel. The list should be ordered from most to least recent. 
                        Notification_message is a string of the following format for each trigger action:
                        tagged: "{User’s handle} tagged you in {channel/DM name}: {first 20 characters of the message}"
                        reacted message: "{User’s handle} reacted to your message in {channel/DM name}"
                        added to a channel/DM: "{User’s handle} added you to {channel/DM name}"
'''
def notifications_get_v1(token):
    userId = get_user_id_from_token(token)
    for user in database.data["accData"]:
        if user["id"] == userId:
            notificationList = user["notifications"].copy()
            notificationList.reverse()
            return {"notifications": notificationList[:20]}
    raise AccessError(description="User not found")
