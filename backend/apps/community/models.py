from django.contrib.auth import get_user_model
from django.db import models

from ..common.models import TimestampStatusMixin
from ..system.models import WeChatUser


class Evaluation(TimestampStatusMixin):
    """
    评价管理
    """
    objects = models.Manager()
    title = models.CharField(max_length=100, verbose_name='评价标题')
    description = models.CharField(max_length=100, verbose_name='评价内容')
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')

    class Meta:
        verbose_name = '评价管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FeedbackImages(TimestampStatusMixin):
    """
    意见反馈关联图像
    """
    objects = models.Manager()
    image = models.ImageField(upload_to='upload/feedback', null=True, blank=True, verbose_name='图片')
    feedback = models.ForeignKey(to='Feedback', on_delete=models.CASCADE, verbose_name='意见反馈',
                                 related_name='feedback_images')

    class Meta:
        verbose_name = '意见反馈关联图像'
        verbose_name_plural = verbose_name


class Feedback(TimestampStatusMixin):
    """
    意见反馈
    """

    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(verbose_name='反馈内容')

    class Meta:
        verbose_name = '意见反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname


class ReportImage(TimestampStatusMixin):
    report = models.ForeignKey(to='Report', on_delete=models.CASCADE, related_name='report_images',
                               verbose_name='问题上报')
    image = models.ImageField(upload_to='upload/report', null=True, blank=True, verbose_name='图片')


class Report(TimestampStatusMixin):
    """
    问题上报
    """
    REPORT_TYPE = (
        (0, '社区服务'), (1, '社区服务1'), (2, '社区服务2')
    )
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=100, verbose_name='标题')
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    type = models.IntegerField(choices=REPORT_TYPE, default=0, verbose_name='反馈类型')
    content = models.TextField(verbose_name='反馈内容')

    class Meta:
        verbose_name = '问题上报'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname


class ConsultPhone(TimestampStatusMixin):
    """
    电话咨询管理
    """
    objects = models.Manager()
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    content = models.TextField(verbose_name='咨询内容')
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')

    class Meta:
        verbose_name = '电话咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class ConsultTime(TimestampStatusMixin):
    time = models.CharField(max_length=100, verbose_name='预约时间段')

    class Meta:
        verbose_name = '预约时间'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.time)


class Consult(TimestampStatusMixin):
    """
    咨询管理
    """
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='用户')
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    content = models.TextField(verbose_name='咨询内容')
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')
    date = models.DateField(verbose_name='预约咨询日期')
    time = models.ForeignKey(ConsultTime, on_delete=models.CASCADE, verbose_name='预约时间', blank=True, null=True)

    class Meta:
        verbose_name = '预约咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname


class Favorite(TimestampStatusMixin):
    """
    收藏
    """
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='用户')
    item = models.CharField(max_length=100, verbose_name='收藏内容')

    class Meta:
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item
