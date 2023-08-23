# -*- coding: utf-8 -*-
"""
Module/Script Name: serializers
Author: Spring
Date: 29/07/2023
Description: 
"""
import os

from rest_framework import serializers

from .helpers import get_weixin_open_id, get_weixin_phone
from .models import Carousel, SystemParams, MenuItem, MenuCategory, Pages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message
from ..community.models import WeChatUser
from backend import settings


class CarouselSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Carousel
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class SystemParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemParams
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = MenuCategory
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class PagesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日", allow_null=True, label='时间',
                                           default=timezone.now)
    class Meta:
        model = Pages
        exclude = ('is_active', 'is_deleted', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='时间',
                                           default=timezone.now)

    class Meta:
        model = Message
        exclude = ('is_active', 'is_deleted', 'updated_at')


class AvatarField(serializers.ImageField):
    def to_internal_value(self, data):
        file = super().to_internal_value(data)
        file.path = settings.AVATAR_ROOT + file.name
        return file

    def to_representation(self, value):
        if not value:
            return None

        return settings.AVATAR_URL + value.name


class WeChatUserCreateSerializer(serializers.Serializer):
    open_id = serializers.SerializerMethodField(label='open_id')
    phone = serializers.SerializerMethodField(label='phone')
    nickname = serializers.CharField(max_length=100, required=False, label='昵称')
    avatar = AvatarField(required=False, label='头像')

    def get_open_id(self, obj):
        js_code = self.context['request'].data.get('js_code')
        # 在这里进行open_id的处理逻辑，例如调用get_weixin_open_id函数
        if js_code:
            open_id = get_weixin_open_id(js_code)
            self.context['request'].data['open_id'] = open_id
            return open_id
        else:
            return None

    def get_phone(self, obj):
        phone_code = self.context['request'].data.get('phone_code')
        if phone_code:
            # 在这里进行phone的处理逻辑
            phone = get_weixin_phone(phone_code)
            self.context['request'].data['phone'] = phone
            return phone
        else:
            return None

    def is_valid(self, raise_exception=False):
        validated = super().is_valid(raise_exception=raise_exception)

        if validated:
            # 将 open_id 和 phone 添加到 validated_data
            self.validated_data['open_id'] = self.get_open_id(None)
            self.validated_data['phone'] = self.get_phone(None)

        return validated

    def create(self, validated_data):
        if not validated_data['open_id']:
            return False
        _, ext = os.path.splitext(validated_data['avatar'].name)
        validated_data['avatar'].name = validated_data['open_id'] + ext
        created_object = WeChatUser.objects.create(
            nickname=validated_data['nickname'],
            avatar=validated_data['avatar'],
            open_id=validated_data['open_id'],
            phone=validated_data['phone']
        )
        return created_object


class WeChatUserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display', label="性别", required=False)
    role = serializers.CharField(source='get_role_display', label="角色", required=False)
    avatar = serializers.ImageField(label="头像", required=False)
    nickname = serializers.CharField(label="昵称", required=False)

    class Meta:
        model = WeChatUser
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at', 'open_id')

    readonly_fields = ('role', 'open_id')


class WeChatUserAvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatUser
        fields = ['avatar', ]

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance


class WeChatUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatUser
        fields = ['nickname', 'name', 'gender', 'address']


# class WeChatUserCreatePhoneSerializer(serializers.Serializer):
#     open_id = serializers.SerializerMethodField(label='open_id')
#     phone = serializers.SerializerMethodField(label='phone')
#
#     def get_open_id(self, obj):
#         # pass
#         # print(self.context['request'].data)
#         js_code = self.context['request'].data.get('js_code') or None
#         # 在这里进行open_id的处理逻辑，例如调用get_weixin_open_id函数
#         if js_code:
#             open_id = get_weixin_open_id(js_code)
#             self.context['request'].data['open_id'] = open_id
#             return open_id
#         else:
#             return None
#
#     def get_phone(self, obj):
#         # pass
#         phone_code = self.context['request'].data.get('phone_code')
#         if phone_code:
#             # 在这里进行phone的处理逻辑
#             phone = get_weixin_phone(phone_code)
#             self.context['request'].data['phone'] = phone
#             return phone
#         else:
#             return None
#
#     def is_valid(self, raise_exception=False):
#         validated = super().is_valid(raise_exception=raise_exception)
#
#         if validated:
#             # 将 open_id 和 phone 添加到 validated_data
#             self.validated_data['open_id'] = self.get_open_id(None)
#             self.validated_data['phone'] = self.get_phone(None)
#
#         return validated
#
#


class WeChatUserCreatePhoneSerializer:
    def __init__(self, data, *args, **kwargs):
        print(data)
        self.js_code = data['js_code']
        self.phone_code = data['phone_code']

    def get_open_id(self):
        if self.js_code:
            open_id = get_weixin_open_id(self.js_code)
            return open_id
        else:
            return None

    def get_phone(self):
        # pass
        phone_code = self.phone_code
        if phone_code:
            # 在这里进行phone的处理逻辑
            phone = get_weixin_phone(phone_code)
            return phone
        else:
            return None
