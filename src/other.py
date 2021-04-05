import pytest
from json import dumps
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v2
from src.channels import channels_create_v2
import src.database as database
from json import dumps, loads
from src.utils import saveData

def clear_v1():
    '''
    Reset Everything to default state
    '''
    database.idData["sessionId"] = 0
    database.idData["userId"] = 0

    database.data["accData"].clear() 
    database.data["channelList"].clear() 
    database.data["message_ids"].clear()
    database.data["dmList"].clear()
    database.data["userProfiles"].clear()

    with open("serverDatabase.json", "w") as dataFile:
        dataFile.write(dumps(database.data))



def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
