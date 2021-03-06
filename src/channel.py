import auth
import database
import error
import channels
from database import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    # check whether id is valid
    if check_id(auth_user_id).get('status'):
        raise error.InputError("User ID invalid")

    # check whether channel is invalid
    channel_id_status = False
    for channel in database.channelList
        if channel.get("id") is channel_id:
            channel_id_status = True
            break
    if channel_id_status is False:
        raise AccessError("Error: Invalid channel")

    iduser = check_id(auth_user_id).get("u_id")

    channels = data['channelList']

    for channel1 in channels:
        if channel_id is channel1['channel_id']:
            if channel1['is public']:
                if iduser not in channel1['all_members']:
                    channel1['all_members'].append(iduser)

                else:
                    raise AccessError("User already in channel")

            else:
                raise AccessError("Private Channel")

    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }


# helpers
def check_id(auth_user_id):
    status = True

    for users in database.accData:
        if users.get('id') is auth_user_id:
            status = False
            user_id = users.get('u_id')

            return {'status': status, 'u_id': user_id}
    
    return {'status': status, 'u_id': None}

