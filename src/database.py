'''
userData = {
    "name_first": name_first,
    "name_last": name_last,
    "email": email,
    "password": sha256(password.encode()).hexdigest(),
    "id": userID,
    "handle": userHandle, 
    "sessions": [],
    "permission": (1 if userID == 0 else 2),
}
accData is list of userData of above format

channelData = {
    'name': name,
    'id': channel_id,
    'is_public': is_public,
    'member_ids': [],
    'owner_ids': [],
    'messages': [],
}
channelList is list of channelData of the above format

dmData = {
    'dm_name': dm_name,
    'id': dm_id,
    'messages': [],
    'member_ids': [],
    'owner_ids': [],
}
dmList is list of dmData of the above format

userProfile = {
                "u_id": userID,
                "email": email,
                "name_first": name_first,
                "name_last": name_last,
                "handle_str": userHandle,
                "profile_img_url": url + "src/static/default.jpg"
            }
userProfiles is list of userProfile of the above format
'''
data = {
    "accData": [],
    "channelList": [],
    "message_ids": [],
    "dmList": [],
    "resetdataList": [],
    "userProfiles": [],
    "standupList": [],
}

idData = {
    "userId": 0,        # starts from 0
    "sessionId": 0,     # starts from 1
    "dmId": 0,          # ???
    "messageId": 0,     # starts from 1
}

userAnalytics = {
    "channels_joined": [],
    "dms_joined": [],
    "messages_sent": [],
    "involvement_rate": 0,
}

dreamsAnalytics = {
    "channels_exist": [],
    "dms_exist": [],
    "messages_exist": [],
    "utilization_rate": 0,
}

secretSauce = "placeholder"

onlineURL = ""
