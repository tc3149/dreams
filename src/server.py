import sys
from json import dumps, loads
from flask import Flask, request, abort, send_from_directory
from flask_mail import Mail, Message
from flask_cors import CORS
from src.error import InputError, AccessError
import src.config as config
import src.database as database
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_reset_v1, auth_passwordreset_request_v1
from src.user import user_profile_v2, user_profile_setemail_v2, users_all_v1, user_stats_v1, users_stats_v1
from src.user import user_profile_setname_v2, user_profile_sethandle_v1, user_profile_uploadphoto_v1
from src.channel import channel_addowner_v1, channel_removeowner_v1
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_senddm_v1, message_share_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.utils import saveData
from src.other import clear_v1, search_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.channel import channel_messages_v2, channel_join_v2, channel_leave_v1, channel_details_v2, channel_invite_v2
from src.dm import dm_leave_v1, dm_remove_v1, dm_messages_v1, dm_create_v1, dm_list_v1, dm_invite_v1, dm_details_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.notifications import notifications_get_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1


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

APP = Flask(__name__, static_url_path="/static/")
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Mail Flask
APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config["MAIL_USE_TLS"] = False
APP.config['MAIL_USE_SSL'] = True
APP.config['MAIL_USERNAME'] = 'projectecho1531@gmail.com'
APP.config['MAIL_PASSWORD'] = '!echo1531'
APP.config['MAIL_DEFAULT_SENDER'] = 'projectecho1531@gmail.com'

mail = Mail(APP)


# ##############################################################################
# DATABASE FUNCTIONS

# Load database

with open("src/serverDatabase.json", "r") as dataFile:
    database.data = loads(dataFile.read())


# #############################################################################
#                                                                             #
#                           AUTH FUNCTIONS                                    #
#                                                                             #
# #############################################################################

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
    returnData = auth_logout_v1(inputData["token"])
    saveData()
    return dumps(returnData)


@APP.route("/auth/passwordreset/request/v1", methods=["POST"])
def authpasswordRequest():
    inputData = request.get_json()
    returnData = auth_passwordreset_request_v1(inputData['email'])
    mail.send(returnData)
    saveData()
    return {}

@APP.route("/auth/passwordreset/reset/v1", methods=["POST"])
def authpasswordReset():
    inputData = request.get_json()
    returnData = auth_passwordreset_reset_v1(inputData["reset_code"], inputData["new_password"])
    saveData()
    return dumps(returnData)


# #############################################################################
#                                                                             #
#                           USER FUNCTIONS                                    #
#                                                                             #
# #############################################################################

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

@APP.route("/user/profile/uploadphoto/v1", methods=["POST"])
def uploadPhoto():
    inputData = request.get_json()
    returnData = user_profile_uploadphoto_v1(inputData["token"], inputData["img_url"], \
            inputData["x_start"], inputData["y_start"], inputData["x_end"], inputData["y_end"])
    return dumps(returnData)

@APP.route("/user/stats/v1", methods=["GET"])
def userStats():
    inputData = request.args.get("token")
    returnData = user_stats_v1(inputData)
    return dumps(returnData)

@APP.route("/users/stats/v1", methods=["GET"])
def usersStats():
    inputData = request.args.get("token")
    returnData = users_stats_v1(inputData)
    return dumps(returnData)


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
    returnData = message_remove_v1(inputData["token"], inputData["message_id"])
    saveData()
    return dumps(returnData)
    
@APP.route("/message/senddm/v1", methods=["POST"])
def messageSendDM():
    inputData = request.get_json()
    returnData = message_senddm_v1(inputData["token"], inputData["dm_id"], inputData["message"])
    saveData()
    return dumps(returnData)

@APP.route("/message/share/v1", methods=["POST"])
def messageShare():
    inputData = request.get_json()
    returnData = message_share_v1(inputData["token"], inputData["og_message_id"], inputData["message"],inputData["channel_id"],inputData["dm_id"])
    saveData()
    return dumps(returnData)

@APP.route("/message/sendlater/v1", methods=["POST"])
def messageSendlater():
    inputData = request.get_json()
    returnData = message_sendlater_v1(inputData["token"], inputData["channel_id"], inputData["message"], inputData["time_sent"])
    saveData()
    return dumps(returnData)

@APP.route("/message/sendlaterdm/v1", methods=["POST"])
def messageSendlaterDM():
    inputData = request.get_json()
    returnData = message_sendlaterdm_v1(inputData["token"], inputData["dm_id"], inputData["message"], inputData["time_sent"])
    saveData()
    return dumps(returnData)

@APP.route("/message/react/v1", methods=["POST"])
def messageReact():
    inputData = request.get_json()
    returnData = message_react_v1(inputData["token"], inputData["message_id"], inputData["react_id"])
    saveData()
    return dumps(returnData)

@APP.route("/message/unreact/v1", methods=["POST"])
def messageUnreact():
    inputData = request.get_json()
    returnData = message_unreact_v1(inputData["token"], inputData["message_id"], inputData["react_id"])
    saveData()
    return dumps(returnData)

@APP.route("/message/pin/v1", methods=["POST"])
def messagePin():
    inputData = request.get_json()
    returnData = message_pin_v1(inputData["token"], inputData["message_id"])
    saveData()
    return dumps(returnData)

@APP.route("/message/unpin/v1", methods=["POST"])
def messageUnpin():
    inputData = request.get_json()
    returnData = message_unpin_v1(inputData["token"], inputData["message_id"])
    saveData()
    return dumps(returnData)



# #############################################################################
#                                                                             #
#                           CHANNEL FUNCTIONS                                 #
#                                                                             #
# #############################################################################

@APP.route("/channel/messages/v2", methods=["GET"])
def channelMessages():
    inputToken = request.args.get("token")
    inputchannelID = int(request.args.get("channel_id"))
    inputStart = int(request.args.get("start"))
    returnData = channel_messages_v2(inputToken, inputchannelID, inputStart)
    saveData()
    return dumps(returnData)

@APP.route("/channel/join/v2", methods=["POST"])
def channelJoin():
    inputData = request.get_json()
    returnData = channel_join_v2(inputData["token"], inputData["channel_id"])
    saveData()
    return dumps(returnData)

@APP.route("/channel/addowner/v1", methods=["POST"])
def channelAddowner():
    inputData = request.get_json()
    returnData = channel_addowner_v1(inputData["token"], inputData["channel_id"], inputData["u_id"])
    saveData()
    return dumps(returnData)

@APP.route("/channel/removeowner/v1", methods=["POST"])
def channelRemoveowner():
    inputData = request.get_json()
    returnData = channel_removeowner_v1(inputData["token"], inputData["channel_id"], inputData["u_id"])
    saveData()
    return dumps(returnData)

@APP.route("/channel/details/v2", methods=["GET"])
def channelDetails():
    inputToken = request.args.get("token")
    inputchannelID = int(request.args.get("channel_id"))
    returnData = channel_details_v2(inputToken, inputchannelID)
    saveData()
    return dumps(returnData)

@APP.route("/channel/leave/v1", methods=["POST"])
def channelLeave():
    inputData = request.get_json()
    returnData = channel_leave_v1(inputData["token"], inputData["channel_id"])
    saveData()
    return dumps(returnData)

@APP.route("/channel/invite/v2", methods = ["POST"])
def channelInvite():
    inputData = request.get_json()
    returnData = channel_invite_v2(inputData["token"],inputData["channel_id"],inputData["u_id"])
    saveData()
    return dumps(returnData)



# #############################################################################
#                                                                             #
#                           CHANNELS FUNCTIONS                                #
#                                                                             #
# #############################################################################

@APP.route("/channels/create/v2", methods=["POST"])
def channelsCreate():
    inputData = request.get_json()
    returnData = channels_create_v2(inputData["token"], inputData["name"], inputData["is_public"])
    saveData()
    return dumps(returnData)

@APP.route("/channels/list/v2", methods=["GET"])
def channelList():
    inputToken = request.args.get("token")
    returnData = channels_list_v2(inputToken)
    saveData()
    return dumps(returnData)

@APP.route("/channels/listall/v2", methods=["GET"])
def channelListall():
    inputToken = request.args.get("token")
    returnData = channels_listall_v2(inputToken)
    saveData()
    return dumps(returnData)

# #############################################################################
#                                                                             #
#                           DM FUNCTIONS                                      #
#                                                                             #
# #############################################################################

@APP.route("/dm/create/v1", methods=["POST"])
def dmCreate():
    inputData = request.get_json()
    returnData = dm_create_v1(inputData["token"], inputData["u_ids"])
    saveData()
    return dumps(returnData)

@APP.route("/dm/messages/v1", methods=["GET"])
def dmMessages():
    inputToken = request.args.get("token")
    inputdmID = int(request.args.get("dm_id"))
    inputStart = int(request.args.get("start"))
    returnData = dm_messages_v1(inputToken, inputdmID, inputStart)
    saveData()
    return dumps(returnData)

@APP.route("/dm/list/v1", methods=["GET"])
def dmList():
    inputToken = request.args.get("token")
    returnData = dm_list_v1(inputToken)
    saveData()
    return dumps(returnData)

@APP.route("/dm/invite/v1", methods=["POST"])
def dmInvite():
    inputData = request.get_json()
    returnData = dm_invite_v1(inputData["token"], inputData["dm_id"], inputData["u_id"])
    saveData()
    return dumps(returnData)

@APP.route("/dm/leave/v1", methods=["POST"])
def dmLeave():
    inputData = request.get_json()
    returnData = dm_leave_v1(inputData["token"], inputData["dm_id"])
    saveData()
    return dumps(returnData)

@APP.route("/dm/remove/v1", methods=["DELETE"])
def dmRemove():
    inputData = request.get_json()
    returnData = dm_remove_v1(inputData["token"], inputData["dm_id"])
    saveData()
    return dumps(returnData)

@APP.route("/dm/details/v1", methods=["GET"])
def dmDetails():
    inputToken = request.args.get("token")
    inputdmID = int(request.args.get("dm_id"))
    returnData = dm_details_v1(inputToken, inputdmID)
    saveData()
    return dumps(returnData)

# #############################################################################
#                                                                             #
#                           ADMIN FUNCTIONS                                   #
#                                                                             #
# #############################################################################

@APP.route("/admin/user/remove/v1", methods = ["DELETE"])
def adminUserRemove():
    inputData = request.get_json()
    returnData = admin_user_remove_v1(inputData["token"], inputData["u_id"])
    saveData()
    return dumps(returnData)

@APP.route("/admin/userpermission/change/v1", methods = ["POST"])
def adminUserpermissionChange():
    inputData = request.get_json()
    returnData = admin_userpermission_change_v1(inputData["token"], inputData["u_id"], inputData["permission_id"])
    saveData()
    return dumps(returnData)

@APP.route("/notifications/get/v1", methods=["GET"])
def getNotifications():
    inputToken = request.args.get("token")
    returnData = notifications_get_v1(inputToken)
    saveData()
    return dumps(returnData)


# #############################################################################
#                                                                             #
#                           OTHER FUNCTIONS                                   #
#                                                                             #
# #############################################################################

@APP.route("/clear/v1", methods=["DELETE"])
def clearAll():
    clear_v1()
    return {}

@APP.route("/search/v2", methods=["GET"])
def searchv2():
    inputToken = request.args.get("token")
    inputQuery = request.args.get("query_str")
    returnData = search_v1(inputToken, inputQuery)
    return dumps(returnData)

@APP.route("/static/<path:filename>")
def uploadImage(filename):
    return send_from_directory("", filename)

@APP.before_first_request
def getURL():
    config.url = request.url_root

# #############################################################################
#                                                                             #
#                           STANDUP FUNCTIONS                                 #
#                                                                             #
# #############################################################################

@APP.route("/standup/start/v1", methods=["POST"])
def standupStart():
    inputData = request.get_json()
    returnData = standup_start_v1(inputData["token"], inputData["channel_id"], inputData["length"])
    saveData()
    return dumps(returnData)

@APP.route("/standup/active/v1", methods=["GET"])
def standupActive():
    inputToken = request.args.get("token")
    inputchannelID = int(request.args.get("channel_id"))
    returnData = standup_active_v1(inputToken, inputChannelID)
    saveData()
    return dumps(returnData)

@APP.route("/standup/send/v1", methods=["POST"])
def standupSend():
    inputData = request.get_json()
    returnData = standup_send_v1(inputData["token"], inputData["channel_id"], inputData["message"])
    saveData()
    return dumps(returnData)

# ########################################################################

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
