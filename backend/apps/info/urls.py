# -*- coding: utf-8 -*-
"""
Module/Script Name: urls
Author: Spring
Date: 29/07/2023
Description: 
"""

from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'telephone', views.TelephoneDirectoryViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'activity', views.ActivityViewSet)
router.register(r'notification', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
