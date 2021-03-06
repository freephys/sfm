#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: user_service.py
@time: 16/10/13 下午1:58
"""

from service.base_service import BaseService
import hashlib
import json
import sms
from utility import aes
from settings import CONFIG
import random
import time

AESKEY = CONFIG['AESKEY']


class UserService(BaseService):

    def __init__(self, services):
        super(UserService, self).__init__(services)

    @classmethod
    def _encrypt(cls, data):
        data = json.dumps(data)
        return aes.encrypt(data, AESKEY)

    @classmethod
    def _decrypt(cls, data):
        try:
            data = aes.decrypt(data, AESKEY)
            return json.loads(data)
        except Exception as e:
            return None

    def get_user_info(self, user_id):
        user_info = self.context_repos.user_repo.select_by_user_id(user_id)
        user_info.pop('pwd_md5')
        return user_info

    def send_verify_code(self, mobile):
        user_info = self.context_repos.user_repo.select_by_mobile(mobile)
        if user_info is not None:
            return {'code': 117, 'msg': '该手机号码已经注册'}

        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verify_code = "".join(x)
        # self.set_cookie('sfm_sms_verify', verifyCode, httponly=True, expires=time.time() + 60 * 15)
        success = sms.send_sms("您好，您的验证码是:%s，验证码在3分钟内有效，如不是本人操作，请忽略。" % verify_code, mobile)
        if success:
            res = self.context_repos.sms_redis.set(mobile, verify_code, ex=300)
            if res is True:
                return {'code': 0, 'msg': '验证码发送成功'}
            else:
                return {'code': 0, 'msg': '验证码发送异常, redis失联'}
        else:
            return {'code': success, 'msg': '验证码发送失败,具体原因参见云通讯官网'}

    def signup(self, mobile, pwd, sms_verify):
        sms_verify_old = self.context_repos.sms_redis.get(mobile)
        if sms_verify_old != sms_verify:
            return {'code': 117, 'msg': '验证码错误'}

        user = self.context_repos.user_repo.select_by_mobile(mobile)
        if user is not None:
            return {'code': 110, 'msg': '该号码已经注册,请联系客服'}

        pwd_md5 = hashlib.md5(pwd).hexdigest()
        last_row_id = self.context_repos.user_repo.insert(mobile, pwd_md5)
        if last_row_id > 0:
            user = self.context_repos.user_repo.select_by_mobile(mobile)
            user_id = user['id']
            self.services.credit_card_service.create_credit_card(user_id)

            return {'code': 0, 'msg': '注册成功'}
        else:
            return {'code': 111, 'msg': '注册失败,请重试'}

    def signin(self, mobile_user_name, pwd):
	user_info = self.context_repos.user_repo.select_by_mobile(mobile_user_name)
        if user_info is None:
            return {'code': 121, 'msg': '该手机号码未注册'}, None
        pwd_md5 = hashlib.md5(pwd).hexdigest()
        user = self.context_repos.user_repo.select_by_mobile_pwd_md5(mobile_user_name, pwd_md5)
        if user is None:
            user = self.context_repos.user_repo.select_by_user_name_pwd_md5(mobile_user_name, pwd_md5)
            if user is None:
                return {'code': 112, 'msg': '用户名或者密码不匹配'}, None

        user_token_dic = {'user_id': user['id'], 'user_name': user['user_name'], "mobile": user['mobile'],
                          "token_secret_key": CONFIG['token_secret_key']}
        user_token = self._encrypt(user_token_dic)
        card_id = self.context_repos.credit_card_repo.select(user['id'])['card_id']
        return {'code': 0, 'msg': '登录成功', 'user_name': user['user_name'], 'user_id': user['id'], 'card_id': card_id}, user_token

    def modify_pwd(self, user_id, old_pwd, new_pwd):
        old_pwd_md5 = hashlib.md5(old_pwd).hexdigest()
        user = self.context_repos.user_repo.select_by_user_id_pwd_md5(user_id, old_pwd_md5)
        if user is None:
            return {'code': 113, 'msg': '原始密码错误'}

        new_pwd_md5 = hashlib.md5(new_pwd).hexdigest()
        last_row_id = self.context_repos.user_repo.update_pwd(user_id, new_pwd_md5)
        if last_row_id > 0:
            return {'code': 0, 'msg': '密码修改成功'}
        else:
            return {'code': 114, 'msg': '密码修改发生异常'}

    def modify_user_name(self, user_id, new_user_name, sex):
        user_old = self.context_repos.user_repo.select_by_user_id(user_id)
        if user_old['user_name'] == new_user_name:
            pass
        else:
            user = self.context_repos.user_repo.select_by_user_name(new_user_name)
            if user is not None:
                return {'code': 115, 'msg': '用户名已存在,修改用户名失败'}

        last_row_id = self.context_repos.user_repo.update_user_name(user_id, new_user_name, sex)
        if last_row_id > 0:
            return {'code': 0, 'msg': '用户名修改成功'}
        else:
            return {'code': 116, 'msg': '用户名修改失败,数据库错误'}

    def request_auth(self, user_id, real_name , id_code, id_card_up, id_card_down):
        res = self.context_repos.auth_repo.insert(user_id, real_name, id_code, id_card_up, id_card_down)
        return res

    def get_auth(self, user_id):
        res = self.context_repos.auth_repo.select_by_user_id(user_id)
        return res

    """-------------后台--------------"""

    def set_auth(self, user_id, is_pass, note):
        res = self.context_repos.auth_repo.update_by_user_id(user_id, is_pass, note)
        return res
