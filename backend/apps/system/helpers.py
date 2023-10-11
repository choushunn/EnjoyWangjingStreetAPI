# -*- coding: utf-8 -*-
"""
Module/Script Name: helpers
Author: Spring
Date: 14/08/2023
Description: 
"""
import json

from .models import Message
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


def send_message(receiver, m_type, content):
    message = Message(
        content=content,
        type=m_type
    )
    message.save()
    message.receiver.add(receiver)


def send_wx_message(message_data):
    access_token = get_weixin_access_token()
    message_data = {
        'touser': 'open_id',
        'template_id': 'template_id',
        'page': 'page',
        'data': {
            'thing1': {
                "value": 'name',
            },
            'date2': {
                "value": 'date',
            }
        }
    }
    url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"
    response = requests.post(url, json=message_data)
    if response.status_code == 200:
        print("订阅消息发送成功")
    else:
        print("订阅消息发送失败")


import requests


def send_subscription_message(openid, template_id, data, page="pages/index/index"):
    access_token = get_weixin_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"

    payload = {
        "touser": openid,
        "template_id": template_id,
        "data": data,
        "page": page,
    }
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        if result.get("errcode") == 0:
            print("订阅消息发送成功")
        else:
            print(f"订阅消息发送失败，错误代码：{result.get('errcode')}")
    else:
        print(f"订阅消息发送失败，HTTP错误代码：{response.status_code}")
