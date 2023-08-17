from django.contrib.auth import get_user_model
from django.db import models
from djrichtextfield.models import RichTextField
from mdeditor.fields import MDTextField
from tinymce.models import HTMLField

from ..common.models import TimestampStatusMixin
from ..community.models import WeChatUser


class TelephoneDirectory(TimestampStatusMixin):
    """
    便民电话
    """
    objects = models.Manager()
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='创建者')
    title = models.CharField(max_length=100, verbose_name='名称')
    number = models.CharField(max_length=100, verbose_name='电话号码')
    address = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='所在地址')

    class Meta:
        verbose_name = '便民电话'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NewsTags(TimestampStatusMixin):
    """
    新闻标签
    """
    objects = models.Manager()
    name = models.CharField(max_length=10, verbose_name="标签名称")
    color = models.CharField(max_length=10, default='red', blank=True, verbose_name="标签颜色")

    class Meta:
        verbose_name = "新闻标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NewsCategory(TimestampStatusMixin):
    objects = models.Manager()
    name = models.CharField(max_length=10, verbose_name="新闻类别")

    class Meta:
        verbose_name = '新闻类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(TimestampStatusMixin):
    """
    新闻
    """

    objects = models.Manager()
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='创建者')
    title = models.CharField(max_length=255, verbose_name='新闻标题')
    summary = models.TextField(max_length=100, null=True, blank=True, verbose_name='新闻摘要')
    content = MDTextField(verbose_name='新闻内容')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name='新闻类别', blank=True, null=True)
    image = models.ImageField(upload_to='upload/news', null=True, blank=True, verbose_name='新闻图片')
    tags = models.ManyToManyField(to="NewsTags", verbose_name="新闻标签")

    class Meta:
        verbose_name = '新闻发布'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Activity(TimestampStatusMixin):
    """
    活动
    """
    objects = models.Manager()
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='创建者')
    title = models.CharField(max_length=255, verbose_name='活动标题')
    summary = models.TextField(max_length=100, null=True, blank=True, verbose_name='活动摘要')
    content = MDTextField(verbose_name='活动内容')
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name='活动类别')
    image = models.ImageField(upload_to='upload/activity', null=True, blank=True, verbose_name='活动图片')

    class Meta:
        verbose_name = '活动发布'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Notification(TimestampStatusMixin):
    """
    通知管理
    """
    objects = models.Manager()
    sender = models.ForeignKey(get_user_model(), default=None, on_delete=models.CASCADE,
                               related_name='sent_notifications',
                               verbose_name='发送者')
    receivers = models.ManyToManyField(WeChatUser, related_name='received_notifications', verbose_name='接收者',
                                       blank=True)
    title = models.CharField(max_length=100, verbose_name='通知标题')
    summary = models.CharField(max_length=100, null=True, blank=True, verbose_name='通知摘要')
    content = models.TextField(verbose_name='通知内容')
    attachment = models.FileField(upload_to='upload/attachment', null=True, blank=True, verbose_name='附件')

    class Meta:
        verbose_name = '通知发布'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
