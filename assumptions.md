Assumptions

auth.py 

- Assumption made regarding handle appending in the function auth_register_v1 of auth.py : "The addition of this final number may result in the handle exceeding the 20 character limit." does not specify clearly if an appended handle is allowed to remain over the 20 character limit. Therefore we will make the assumption that when appending a handle, it IS ALLOWED to remain over 20 characters long.

channels.py 

- Owners are automatically joined into channels they create
- User Ids are input as integers
- When channel names are less than 1 character, provide an input error