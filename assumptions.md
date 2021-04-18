#### Assumptions

**auth.py** 

- auth_login_v1:
    - N/A

- auth_register_v1:
    - Assumption made regarding handle appending in the function auth_register_v1 of auth.py : "The addition of this final number may result in the handle exceeding the 20 character limit." does not specify clearly if an appended handle is allowed to remain over the 20 character limit. Therefore we will make the assumption that when appending a handle, it IS ALLOWED to remain over 20 characters long.

- auth_logout_v1:
    - Assumes AccessError is session id doesnt exist


**user.py**

- user_profile_v2
    - Assumes InputError if u_id does not exist

- user_profile_setname_v2
    - Assumes set both accData names and profileData names

- user_profile_setemail_v2
    - Assumes set both accData email and profileData email

- user_profile_sethandle_v1
    - Assumes set both accData handle and profileData handle

- user_all_v1
    - N/A


**channels.py**

- Overall:
    - Owners are automatically joined into channels they create
    - User Ids are input as integers
    - When channel names are less than 1 character, provide an input error

- channels_list_v1:
    - Assume that the list begins with channel ids from smallest to largest
    - If there are no channels, return empty list

- channels_listall_v1:
    - Assume that the list begins with channel ids from smallest to largest
    - If there are no channels, return empty list

- channels_create_v1:
    - Possible to create more than one channel with a single user_id
    - Channel id starts at zero and continues linearly by one.
    - Owners are automatically joined as members into channels they create
    - Channel names are not 'nothing', and as such are greater than 0 characters.


**channel.py**

- channel_invite_v1:
    - Assumes the auth_user_id has to be the owner of the channel in order to invite other users
    - Assumes an invalid (does not exist in database) auth_user_id will raise an InputError

- channel_details_v1:
    - Assumes the auth_user_id has to be the owner of the channel in order to successfully call this function
    - Assumes an invalid (does not exist in database) auth_user_id will raise an InputError
    - If there are no channels, return empty list

- channel_messages_v1:
    - Assumes an invalid (does not exist in database) auth_user_id will raise an AccessError
    - Can only test with an empty list for the time being

- channel_join_v1:
    - Assumes an invalid (does not exist in database) auth_user_id will raise an InputError
    - Assumes a private channel will always return an AccessError as global owner has not been implemented yet

- channel_addowner_v1:
    - Assumes that a user has to be part of the channel in order to become owner
    - Assumes an invalid u_ID produces an InputError

- channel_removeowner_v1:
    - Assumes that removing an owner does not kick them from the channel


**message.py**
- Overall:
    - Assumes that any message that is "" is considered removed, and its message_id would be invalid
    
- message_send_v2:
    - Assumes the message can be of 1000 characters, but no more
    - Assumes a message cannot be empty ('') as this is considered a removed message
    - Assumes an invalid channel ID will produce an InputError

- message_edit_v2:
    - Assume the message can be of 1000 characters, but no more
    - Assumes an invalid channel ID will produce an InputError
    - Assumes an invalid message ID will produce an InputError
    - Only the OP, Owner and Dreams Owner can edit a message

- message_remove_v1:
    - Assumes an invalid channel ID will produce an InputError
    - Assumes an invalid message ID will produce an InputError
    - Only the OP, Owner and Dreams Owner can remove a message
    - When deleting a message, the message will delete, however, the information (e.g. message_id) contents will stay, only the message is deleted

- message_senddm_v1
    - Assumes the message can be of 1000 characters, but no more
    - Assumes a message cannot be empty ('') as this is considered a removed message
    - Assumes an invalid channel ID will produce an InputError

- message_share_v1
    - Assumes a message id can be a channel message or a dm message regardless where shared to
    - Assumes messages can be shared to the same channel
    - The opposite of shared will be searched first for message id
    - Assumes if both dm_id and channel_id are -1 or both not -1 returns InputError

- message_sendlater_v1
    - Assumes an invalid channel ID will produce an InputError
    - Assumes an invalid message ID will produce an InputError
    - Assumes the message_id is assigned to a message at the time the function is called rather than when it is sent when the Timer finishes

- message_sendlaterdm_v1
    - Assumes an invalid dm ID will produce an InputError
    - Assumes an invalid message ID will produce an InputError
    - Assumes the message_id is assigned to a message at the time the function is called rather than when it is sent when the Timer finishes

- message_react_v1
    - Assumes that the only valid react is 1 (as of no challenge exercises)

- message_unreact_v1
    - As the only valid react is 1, then the only valid unreact is 1
    - Assumes that the user has previously reacted to the message

- message_pin_v1
    - 

- message_unpin_v1
    -


**dm.py**

- dm_leave_v1
    - Assumes the owner cannot leave
    - Assumes that the name is deleted from data in dm_name 

- dm_create_v1
    - Assumes the user id of the creator wont be in the u_ids list
    - Possible to create more than one dm with a single user id
    - Dm id starts at zero and continues linearly by one for each dm created
    - A DM id can never be used twice, i.e. if dm_id 0 is deleted, the next dm created is still dm_id = 1

- dm_list_v1
    - Assume that the list begins with dm ids from smallest to largest
    - If there are no dms, return empty list

- dm_invite_v1
    - Owner cannot invite himself into the dm
    - Owner cannot invite members already in the dm into the dm

- dm_details_v1
    - Assumes removed users can be returned


**admin.py**
- admin_user_remove_v1
    - Assumes owner cannot remove themself if they are the only owner
    - Assumes removed user message data is left intact and only the 
        message contents and user name is changed
    - Removes accData but leaves profile data

- admin_userpermission_change_v1
    - Assumes owner cannot change their permission if they are the only owner
    - Assumes you can change permission 1 to 1 and 2 to 2


**other.py**

- search_v1
    - Assumes the query string is case sensitive
    - Assumes search uses ascii characters

