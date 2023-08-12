# -*- coding: utf-8 -*-
"""
Module/Script Name: serializers
Author: Spring
Date: 29/07/2023
Description: 
"""
from django.utils import timezone
from rest_framework import serializers
from .models import Appointment, Ticket, TicketType, AppointmentType, AppointmentTime, TicketImage, TicketReview


class AppointmentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTime
        exclude = ('is_active', 'is_deleted', 'updated_at', 'created_at')


class AppointmentTypeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='预约时间',
                                           default=timezone.now)

    class Meta:
        model = AppointmentType
        exclude = ('is_active', 'is_deleted', 'updated_at')


class AppointmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='预约时间',
                                           default=timezone.now)
    type_name = serializers.SerializerMethodField()
    type_time = serializers.SerializerMethodField()

    def get_type_time(self, obj):
        if obj.time:
            return obj.time.time
        return None

    def get_type_name(self, obj):
        if obj.type:
            return obj.type.name
        return None

    class Meta:
        model = Appointment
        exclude = ('is_active', 'is_deleted', 'updated_at')


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('id', 'name')


class TicketImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketImage
        fields = ('id', 'image', 'ticket')


class TicketReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReview
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ('is_active', 'is_deleted')


class TicketListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y年%m月%d日 %H:%M", allow_null=True, label='创建时间',
                                           default=timezone.now)
    ticket_type_name = serializers.SerializerMethodField()
    ticket_images = TicketImageSerializer(many=True, label='图片', allow_null=True, read_only=True)
    ticket_reviews = TicketReviewSerializer(many=True, label='评论', allow_null=True)

    def get_ticket_type_name(self, obj):
        if obj.ticket_type:
            return obj.ticket_type.name
        return None

    class Meta:
        model = Ticket
        exclude = ('is_active', 'is_deleted')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if 'ticket_images' in representation:
            for image_data in representation['ticket_images']:
                if image_data['image']:
                    image_data['image_url'] = request.build_absolute_uri(image_data['image'])
        return representation


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_at', 'ticket_type_name', 'ticket_images', 'ticket_reviews')

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            return TicketCreateSerializer(instance).to_representation(instance)
        else:
            return TicketListSerializer(instance, context={'request': self.context['request']}).to_representation(
                instance)
