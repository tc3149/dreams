import re
from src.database import accData, channelList
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError


def channels_list_v1(auth_user_id):

    return {

    }

def channels_listall_v1(auth_user_id):
    channelsList = []
    for channel in channelList:
        channelsList.append(channel.get("name"))
    return channelsList

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    # Check if length of name is valid
    if len(name) > 20:
        raise InputError("Error: Name is greater than 20 characters")

    if len(name) < 1:
        raise InputError("Error: Name is less than 1 character")

    # Check if valid user id
    id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            id_status = True
            break
    
    if id_status is False:
        raise AccessError("Error: Invalid user id")
    
    channel_id = len(channelList)

    channelData = {
        'name': name,
        'id': channel_id,
        'is_public': is_public,
        'member_ids': [],
        'owner_ids': [],
        'messages': [],
    }

    # Adding user data
    channelData['owner_ids'].append(auth_user_id)
    channelData['member_ids'].append(auth_user_id)

    channelList.append(channelData)


    return {
        'channel_id': channel_id,
    }

if __name__ == "__main__":
    user0 = auth_register_v1("email2@gmail.com", "password1", "1Name", "1Lastname")
    user1 = auth_register_v1("email3@gmail.com", "password3", "3Name", "3Lastname")
    user2 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    
    for user in accData:
        print(user.get("id"))

    print(user2.get("auth_user_id"))
    
    print(channels_create_v1(user2.get("auth_user_id"), "Channel", True))