# -*- coding: utf-8 -*-
"""
Module/Script Name: serializers
Author: Spring
Date: 29/07/2023
Description: 
"""
import os

from django.utils import timezone
from rest_framework import serializers
from .models import Message, WeChatUser, Evaluation, \
    Feedback, Favorite, Consult, Report, ReportImage, ConsultPhone, FeedbackImages
from .utils import get_weixin_open_id, get_weixin_phone
from backend import settings


class WeChatUserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display', label="性别", required=False)
    role = serializers.CharField(source='get_role_display', label="角色", required=False)
    avatar = serializers.ImageField(label="头像", required=False)
    # open_id = serializers.CharField(label="open_id", required=False)
    nickname = serializers.CharField(label="昵称", required=False)
    class Meta:
        model = WeChatUser
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at', 'open_id')

    readonly_fields = ('role', 'open_id')


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class FeedbackImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImages
        fields = ('id', 'image', 'feedback')


class FeedbackSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='预约时间',
                                           default=timezone.now)
    feedback_images = FeedbackImagesSerializer(many=True, label='图片', allow_null=True, read_only=True)

    class Meta:
        model = Feedback
        exclude = ('is_active', 'is_deleted', 'updated_at')


class ConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consult
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class ConsultPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultPhone
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='时间',
                                           default=timezone.now)

    class Meta:
        model = Message
        exclude = ('is_active', 'is_deleted', 'updated_at')


class ReportSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='预约时间',
                                           default=timezone.now)

    class Meta:
        model = Report
        exclude = ('is_active', 'is_deleted', 'updated_at')


class ReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = ('id', 'image', 'report')


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
