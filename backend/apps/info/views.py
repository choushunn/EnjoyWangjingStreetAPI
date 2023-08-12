from rest_framework import viewsets

from .models import TelephoneDirectory, News, Notification, Activity
from .serializers import TelephoneDirectorySerializer, NotificationSerializer, NewsSerializer, ActivitySerializer


class TelephoneDirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    便民电话接口 GET
    """
    queryset = TelephoneDirectory.objects.all()
    serializer_class = TelephoneDirectorySerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    新闻接口 GET
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    活动接口 GET
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    通知接口 GET
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
