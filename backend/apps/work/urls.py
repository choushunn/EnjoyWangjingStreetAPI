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

# router = DefaultRouter()
#
# router.register(r'appointment', views.AppointmentViewSet)
# # router.register(r'consult', views.ConsultViewSet)
# router.register(r'work', views.TicketViewSet)
# urlpatterns = [
#     path('', include(router.urls)),
# ]
