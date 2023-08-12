# -*- coding: utf-8 -*-
"""
Module/Script Name: serializers
Author: Spring
Date: 29/07/2023
Description: 
"""

from rest_framework import serializers
from .models import Carousel, SystemParams, MenuItem, MenuCategory, Pages
from django.contrib.auth.models import User


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
    class Meta:
        model = Pages
        exclude = ('is_active', 'is_deleted', 'created_at', 'updated_at')
