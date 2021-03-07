import re
from src.error import InputError, AccessError
from src.database import accData, channelList
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    #check if channel exists
   
    if channel_id <= len(channelList)
        #channel does exist
        break
    else:
        #channel does not exist
        raise InputError ("Channel does not exis")
    
    #check if auth_user_id exists
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            break
        else:
            # auth_user_id does not exist
            raise InputError ("Inviting user does not exist")
    
    #check if auth_user_id owner member of channel
    for user in channelList[channel_id][channelData]['owner_ids']:
        
        if user.get("id") is auth_user_id:
            #user is owner member of channel
            break
        else:
            #user does not have access
            raise AccessError ("User does not have access")
    
    #check if u_id exists
    for user2 in accData:
        if user2.get("id") is u_id:
            #u_id exists
            break
        else:
            # u_id does not exist
            raise InputError ("Invited user does not exist")
    
    #check if u_id already member of the channel
    for user2 in channelList[channel_id][channelData]['member_ids']:
        
        if user2.get("id") is auth_user_id:
            #u_id is member of channel
            raise InputError ("User already a member")
            
        else:
            #u_id not a member
            break
    
    #add u_id to channel
    channelData['member_ids'].append(u_id)

    return {

    }

def channel_details_v1(auth_user_id, channel_id):

    #check if channel exists
    for channel in channelList:
        if channel_id <= len(channelList)
            #channel does exist
            break
        else:
            #channel does not exist
            raise InputError ("Channel does not exis")
    
    #check if auth_user_id exists
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            break
        else:
            # auth_user_id does not exist
            raise InputError ("Inviting user does not exist")
    
    #check if auth_user_id member of channel
    for user in channelList[channel_id][channelData]['member_ids']:
        
        if user.get("id") is auth_user_id:
            #user is member of channel
            break
        else:
            #user does not have access
            raise AccessError ("User does not have access")

    return {
        'name': channelList[channel_id][channelData]['name'],
        'owner_members':channelList[channel_id][channelData]['owner_ids'],
        'member_owners':channelList[channel_id][channelData]['member_ids']
    
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
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

if __name__ == "__main__":
    user = auth_register_v1("email2@gmail.com", "password1", "1Name", "1Lastname")
    channel = channels_create_v1(user.get("auth_user_id"), "testchannel", True)
    user2 = auth_register_v1("email@gmail.com", "password", "Name", "Lastname")
    
    for user in accData:
        print(user.get("id"))
    for user2 in accData:
        print(user2.get("id"))
    for channel in channelList:
        print(channel.get("channel_id"))
    
    