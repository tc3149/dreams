Assumptions

auth.py 

auth_login_v1:
- 

auth_register_v1:
- Assumption made regarding handle appending in the function auth_register_v1 of auth.py : "The addition of this final number may result in the handle exceeding the 20 character limit." does not specify clearly if an appended handle is allowed to remain over the 20 character limit. Therefore we will make the assumption that when appending a handle, it IS ALLOWED to remain over 20 characters long.

channels.py 

channels_list_v1:
- Assume that the list begins with channel ids from smallest to largest
- If there are no channels, return empty list

channels_listall_v1:
- Assume that the list begins with channel ids from smallest to largest
- If there are no channels, return empty list

channels_create_v1:
- Possible to create more than one channel with a single user_id
- Channel id starts at zero and continues linearly by one.
- Owners are automatically joined as members into channels they create
- Channel names are not 'nothing', and as such are greater than 0 characters.

