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
from .models import Evaluation, \
    Feedback, Favorite, Consult, Report, ReportImage, ConsultPhone, FeedbackImages, ConsultTime, ServiceList


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


class ConsultTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultTime
        exclude = ('is_active', 'is_deleted', 'updated_at', 'created_at')


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


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceList
        exclude = ('is_active', 'is_deleted', 'updated_at', 'created_at')
