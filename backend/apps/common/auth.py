# -*- coding: utf-8 -*-
"""
Module/Script Name: auth
Author: Spring
Date: 05/08/2023
Description: 
"""

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from apps.community.models import WeChatUser


class OpenidAuthentication(JWTAuthentication):
    """
    继承JWTAuthentication类， 返回自定义User对象
    """

    def get_user(self, validated_token):
        """
        返回用户，重写后在其它地方使用request.user时可以直接得到自定义的小程序用户
        :param validated_token:
        :return:
        """
        try:
            # 此处为自定义的解析token方法， 可以解码token得到其中的信息，重点是拿到user_id 用于后续的获取用户
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken('Token不包含可识别的用户标识')

        try:
            user = WeChatUser.objects.get(**{'id': user_id})
        except WeChatUser.DoesNotExist:
            raise AuthenticationFailed('未找到用户', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed("当前用户未激活", code="user_inactive")

        return user


