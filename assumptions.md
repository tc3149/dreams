#### Assumptions

**auth.py** 

- auth_login_v1:
    - N/A

- auth_register_v1:
    - Assumption made regarding handle appending in the function auth_register_v1 of auth.py : "The addition of this final number may result in the handle exceeding the 20 character limit." does not specify clearly if an appended handle is allowed to remain over the 20 character limit. Therefore we will make the assumption that when appending a handle, it IS ALLOWED to remain over 20 characters long.



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


**dm.py**

- dm_leave_v1
    - Assumes the owner cannot leave
    - Assumes that the name is deleted from data in dm_name 