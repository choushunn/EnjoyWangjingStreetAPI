# -*- coding: utf-8 -*-
"""
Module/Script Name: utils
Author: Spring
Date: 05/08/2023
Description: 
"""

import os
from typing import Any

import requests
from django.core.cache import cache

from backend import settings


def get_weixin_open_id(js_code: str) -> Any:
    print("开始获取OpenID:", js_code)
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': settings.WX_APP_ID,
        'secret': settings.WX_APP_SECRET,
        'js_code': js_code,
        'grant_type': 'authorization_code',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if 'openid' not in data or 'session_key' not in data:
        return None
    return data['openid']


def get_weixin_access_token():
    access_token = cache.get("access_token", False)
    if access_token:
        print("从缓存获取token:", access_token)
        return access_token

    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'appid': settings.WX_APP_ID,
        'secret': settings.WX_APP_SECRET,
        'grant_type': 'client_credential'
    }

    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
        data = response.json()
        access_token = data.get('access_token')
        if access_token:
            cache.set('access_token', access_token, 60 * 60 * 1.5)
            return access_token
    except requests.exceptions.RequestException:
        pass
    return None


def get_weixin_phone(phone_code: str) -> Any:
    url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber'
    access_token = get_weixin_access_token()
    params = {
        'access_token': access_token,
    }
    data = {
        'code': phone_code,
    }
    response = requests.post(url, params=params, json=data)
    data = response.json()
    response.raise_for_status()
    if 'errmsg' in data:
        if data['errmsg'] == 'ok':
            return data['phone_info']['phoneNumber']
    return None
