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
'''
data = {
    "accData": [],
    "channelList": [],
    "message_ids": [],
    "dmList": [],
    "userProfiles": [],
    "standupList": [],
}

idData = {
    "userId": 0, 
    "sessionId": 0,
    "dmId": 0,
    "messageId": 0, # starts from 1
}

secretSauce = "placeholder"

