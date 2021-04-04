import sys
from json import dumps, loads
from flask import Flask, request, abort
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.database import data, secretSauce
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.user import user_profile_v2, user_profile_setemail_v2, users_all_v1
from src.user import user_profile_setname_v2, user_profile_sethandle_v1
from src.channel import channel_addowner_v1
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_senddm_v1
from src.utils import saveData
from src.other import clear_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# ##############################################################################
# DATABASE FUNCTIONS

# Load database

with open("serverDatabase.json", "r") as dataFile:
    data = loads(dataFile.read())


# ##############################################################################
# AUTH FUNCTIONS

@APP.route("/auth/register/v2", methods=["POST"])
def authRegister():
    inputData = request.get_json()
    returnData = auth_register_v2(
            inputData["email"], inputData["password"], inputData["name_first"], inputData["name_last"])
    saveData()

    return dumps(returnData)

@APP.route("/auth/login/v2", methods=["POST"])
def authLogin():
    inputData = request.get_json()
    returnData = auth_login_v2(inputData["email"], inputData["password"])
    saveData()
    return dumps(returnData)

@APP.route("/auth/logout/v1", methods=["POST"])
def authLogout():
    inputData = request.get_json()
    returnData = auth_logout_v1(inputData)
    saveData()
    return dumps(returnData)
# ##############################################################################
# USER FUNCTIONS
@APP.route("/user/profile/v2", methods=["GET"])
def userProfile():
    inputToken = request.args.get("token")
    inputId = int(request.args.get("u_id"))
    returnData = user_profile_v2(inputToken, inputId)
    saveData()
    return dumps(returnData)

@APP.route("/user/profile/setname/v2", methods=["PUT"])
def userSetName():
    inputData = request.get_json()
    returnData = user_profile_setname_v2(
            inputData["token"], inputData["name_first"], inputData["name_last"])
    saveData()
    return dumps(returnData)

@APP.route("/user/profile/setemail/v2", methods=["PUT"])
def userSetEmail():
    inputData = request.get_json()
    returnData = user_profile_setemail_v2(inputData["token"], inputData["email"])
    saveData()
    return dumps(returnData)

@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def userSetHandle():
    inputData = request.get_json()
    returnData = user_profile_sethandle_v1(inputData["token"], inputData["handle_str"])
    saveData()
    return dumps(returnData)

@APP.route("/users/all/v1", methods=["GET"])
def usersAll():
    inputToken = request.args.get("token")
    returnData = users_all_v1(inputToken)
    saveData()
    return dumps(returnData)

# COLINS CODE BELOW:
"""

# #############################################################################
#                                                                             #
#                           MESSAGE FUNCTIONS                                 #
#                                                                             #
# #############################################################################

@APP.route("/message/send/v2", methods=["POST"])
def messageSend():
    inputData = request.get_json()
    returnData = message_send_v2(inputData["token"], inputData["channel_id"], inputData["message"])
    saveData()
    return dumps(returnData)

@APP.route("/message/edit/v2", methods=["PUT"])
def messageEdit():
    inputData = request.get_json()
    returnData = message_edit_v2(inputData["token"], inputData["message_id"], inputData["message"])
    saveData()
    return dumps(returnData)

@APP.route("/message/remove/v1", methods=["DELETE"])
def messageRemove():
    inputData = request.get_json()
    returnData = message_remove_v1(inputdata["token"], inputData["message_id"])
    saveData()
    return dumps(returnData)
    
@APP.route("/message/senddm/v1", methods=["POST"])
def messageRemove():
    inputData = request.get_json()
    returnData = message_senddm_v1(inputdata["token"], inputData["dm_id"], inputdata["message"])
    saveData()
    return dumps(returnData)



# #############################################################################
#                                                                             #
#                           CHANNEL FUNCTIONS                                 #
#                                                                             #
# #############################################################################

@APP.route("/channel/addowner/v1", methods=["POST"])
def channelAddowner():
    inputData = request.get_json()
    returnData = channel_addowner_v1(inputData["token"], inputData["channel_id"], inputData["u_id"])
    saveData()
    return dumps(returnData)

"""

# ##############################################################################

@APP.route("/clear/v1", methods=["DELETE"])
def clearAll():
    clear_v1()
    return {}

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
