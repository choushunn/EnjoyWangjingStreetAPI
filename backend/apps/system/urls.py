# -*- coding: utf-8 -*-
"""
Module/Script Name: urls
Author: Spring
Date: 29/07/2023
Description: 
"""

from django.urls import include, path

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'carousel', views.CarouselViewSet)
router.register(r'system_params', views.SystemParamsViewSet)
router.register(r'menu_category', views.MenuCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
