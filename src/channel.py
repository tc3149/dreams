import re
from src.error import InputError, AccessError
from src.database import accData, channelList, allMembers, ownMembers
from src.channels import channels_create_v1
from src.auth import auth_register_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    #check if channel exists
    for channel in channelList:
        if channel_id <= len(channelList):
            #channel does exist
            break
        else:
            #channel does not exist
            raise InputError ("Channel does not exis")
    
    #check if auth_user_id exists 
    auth_id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            auth_id_status = True
            break
   
    if auth_id_status is False:
        # auth_user_id does not exist
        raise InputError ("Inviting user does not exist")
            
    
    #check if auth_user_id owner member of channel
    owner_status = False
    for user in channelList[channel_id]['owner_ids']:   
        if auth_user_id in channelList[channel_id]['owner_ids']:
            #user is owner member of channel
            owner_status = True
            break
               
    if owner_status is False:
        #user does not have access
        raise AccessError ("User does not have access")

    #check if u_id exists
    u_id_status = False
    for user2 in accData:
        if user2.get("id") is u_id:
            #u_id exists
            u_id_status = True
            break
            
    if u_id_status is False:
        # u_id does not exist
        raise InputError ("Invited user does not exist")
    
    #check if u_id already member of the channel
    for user2 in channelList[channel_id]['member_ids']:
        
        if u_id in channelList[channel_id]['member_ids']:
            #u_id is member of channel
            raise InputError ("User already a member")    

            
    
    #add u_id to channel
    
    channelList[channel_id]['member_ids'].append(u_id)
    
    return {

    }

def channel_details_v1(auth_user_id, channel_id):

    #check if channel exists
    for channel in channelList:
        if channel_id <= len(channelList):
            #channel does exist
            break
        else:
            #channel does not exist
            raise InputError ("Channel does not exis")
    #check if auth_user_id exists 
    auth_id_status = False
    for user in accData:
        if user.get("id") is auth_user_id:
            #auth_user_id exists
            auth_id_status = True
            break
   
    if auth_id_status is False:
        # auth_user_id does not exist
        raise AccessError ("User does not exist")
            
    
    #check if auth_user_id owner member of channel
    member_status = False
    for user in channelList[channel_id]['member_ids']:
        
        if auth_user_id in channelList[channel_id]['member_ids']:
            #user is owner member of channel
            member_status = True
            break
               
    if member_status is False:
        #user does not have access
        raise AccessError ("User does not have access")
    
    #loop to add member details
    for memberID in channelList[channel_id]['member_ids']:
        for mem in accData:
            if memberID is mem['id']:
                new_member = {
                'u_id':memberID,
                'email': accData[memberID]['email'],
                'name_first': accData[memberID]['name_first'],
                'name_last': accData[memberID]['name_last']
            }
            allMembers.append(new_member)
    #loop to add owner details
    for ownerID in channelList[channel_id]['owner_ids']:
        for own in accData:
            if ownerID is own['id']:
                owner = {
                'u_id':ownerID,
                'email': accData[ownerID]['email'],
                'name_first': accData[ownerID]['name_first'],
                'name_last': accData[ownerID]['name_last']
            }
            ownMembers.append(new_member)
    
    return {
        'name': channelList[channel_id]['name'],
        'owner_members':ownMembers,
        'all_members':allMembers
    
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
    
    