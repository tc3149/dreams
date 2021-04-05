import pytest
import requests
import json
import jwt
import urllib
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2
from src.message import message_send_v2, message_edit_v2, message_remove_v1
from src.message import message_senddm_v1
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.utils import get_user_id_from_token, make_dm_name, valid_dmid, valid_userid

#test for admin user remove
def test_http_admin_user_remove_u_id_does_not_exist():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)
    # ----------------------------
    #chec admin user remove
    funcURL = "admin/user/remove/v1"
    inputData ={
        "token": userR['token'],
        "u_id": 3
    }
    adminUserRemove = requests.delete(config.url + funcURL, json=inputData)
    adminUserRemoveR = json.loads(adminUserRemove.text)

    assert adminUserRemoveR["code"] == 400

def test_http_admin_user_remove_auth_not_owner():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user.text)
    # ----------------------------

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)
    # ----------------------------------
    #check admin user remove
    funcURL = "admin/user/remove/v1"
    inputData ={
        "token": user2R['token'],
        "u_id": user3R['auth_user_id']
    }
    adminUserRemove = requests.delete(config.url + funcURL, json=inputData)
    adminUserRemoveR = json.loads(adminUserRemove.text)

    assert adminUserRemoveR['code'] == 403

def test_http_admin_user_remove_auth_only_owner():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    #check admin user remove
    funcURL = "admin/user/remove/v1"
    inputData ={
        "token": userR['token'],
        "u_id": userR['auth_user_id']
    }
    adminUserRemove = requests.delete(config.url + funcURL, json=inputData)
    adminUserRemoveR = json.loads(adminUserRemove.text)

    assert adminUserRemoveR['code'] == 400

def test_http_admin_user_remove_successful_removed():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    #admin user remove
    funcURL = "admin/user/remove/v1"
    inputData ={
        "token": userR['token'],
        "u_id": user2R['auth_user_id']
    }
    adminUserRemove = requests.delete(config.url + funcURL, json=inputData)
    _ = json.loads(adminUserRemove.text)
    #---------------------------------
    #check if removed
    assert valid_userid(user2R['auth_user_id']) == False


############################################################################################################################################
# Admin_userpermission_tests

def test_http_admin_userpermission_u_id_does_not_exist():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user2.text)
    # ----------------------------
    #chec admin user permission
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": userR['token'],
        "u_id": 3,
        "permission_id": 1
    }
    adminUserPermission = requests.post(config.url + funcURL, json=inputData)
    adminUserPermissionR = json.loads(adminUserPermission.text)

    assert adminUserPermissionR["code"] == 400

def test_http_admin_userpermission_permission_id_not_valid():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    #check admin user permission
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": userR['token'],
        "u_id": user2R['auth_user_id'],
        "permission_id": 5
    }
    adminUserPermission = requests.post(config.url + funcURL, json=inputData)
    adminUserPermissionR = json.loads(adminUserPermission.text)

    assert adminUserPermissionR["code"] == 400

def test_http_admin_userpermission_auth_not_owner():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    _ = json.loads(user.text)
    # ----------------------------

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test2@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "test3@hotmail.com",
        "password": "password1",
        "name_first": "nameFirst",
        "name_last": "nameLast",
    }
    user3 = requests.post(config.url + funcURL, json=inputData)
    user3R = json.loads(user3.text)
    # ----------------------------------
    #check admin user rpermssion
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": user2R['token'],
        "u_id": user3R['auth_user_id'],
        "permission_id": 1

    }
    adminUserRemove = requests.post(config.url + funcURL, json=inputData)
    adminUserRemoveR = json.loads(adminUserRemove.text)

    assert adminUserRemoveR['code'] == 403

def test_http_admin_userpermission_member_to_owner_permission():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    #check admin user permission
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": userR['token'],
        "u_id": user2R['auth_user_id'],
        "permission_id": 1
    }
    adminUserPermission = requests.post(config.url + funcURL, json=inputData)
    adminUserPermissionR = json.loads(adminUserPermission.text)

    assert adminUserPermissionR == {}

def test_http_admin_userpermission_owner_to_member_permission():
    requests.delete(config.url + "clear/v1")

    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email@gmai.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user = requests.post(config.url + funcURL, json=inputData)
    userR = json.loads(user.text)
    # ----------------------------
    # Register--------------------
    funcURL = "auth/register/v2"
    inputData = {
        "email": "email2@gmail.com",
        "password": "password1",
        "name_first": "Name",
        "name_last": "Lastname",
    }
    user2 = requests.post(config.url + funcURL, json=inputData)
    user2R = json.loads(user2.text)
    # ----------------------------
    #check admin user permission
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": userR['token'],
        "u_id": user2R['auth_user_id'],
        "permission_id": 1
    }
    adminUserPermission = requests.post(config.url + funcURL, json=inputData)
    adminUserPermissionR = json.loads(adminUserPermission.text)

    #old owner to member
    funcURL = "admin/userpermission/change/v1"
    inputData ={
        "token": user2R['token'],
        "u_id": userR['auth_user_id'],
        "permission_id": 2
    }
    adminUserPermission = requests.post(config.url + funcURL, json=inputData)
    adminUserPermissionR = json.loads(adminUserPermission.text)

    assert adminUserPermissionR == {}
