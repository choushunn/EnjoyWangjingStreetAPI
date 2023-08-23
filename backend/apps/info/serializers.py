# -*- coding: utf-8 -*-
"""
Module/Script Name: serializers
Author: Spring
Date: 29/07/2023
Description: 
"""
from django.utils import timezone
from rest_framework import serializers
from .models import TelephoneDirectory, Notification, News, Activity, NewsTags


class TelephoneDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TelephoneDirectory
        fields = ('id', 'title', 'number', 'address', 'type')


class NewsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTags
        exclude = ('is_active', 'is_deleted', 'updated_at', 'created_at', 'id')


# class WeChatRichTextField(serializers.Field):
#     def to_representation(self, value):
#         return richtextfilter(value)
#
#     def to_internal_value(self, data):
#         return data


class NewsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日", allow_null=True, label='发布时间', )
    tags = NewsTagsSerializer(many=True)

    class Meta:
        model = News
        exclude = ('is_active', 'is_deleted', 'updated_at', 'creator')


class ActivitySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日", allow_null=True, label='时间',
                                           default=timezone.now)

    class Meta:
        model = Activity
        exclude = ('is_active', 'is_deleted', 'creator')


class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='时间',
                                           default=timezone.now)

    class Meta:
        model = Notification
        fields = ('id', 'title', 'summary', 'content', 'attachment', 'created_at')
