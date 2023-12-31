from datetime import datetime

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
    today = datetime.today()
    folder_name = today.strftime('%Y/%m/%d')
    image = models.ImageField(upload_to=F'upload/feedback/{folder_name}', null=True, blank=True, verbose_name='图片')
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
    user = models.ForeignKey(WeChatUser, on_delete=models.DO_NOTHING, verbose_name='用户')
    content = models.TextField(verbose_name='反馈内容')
    replay = models.TextField(verbose_name='意见回复', default=None, blank=True, null=True)

    class Meta:
        verbose_name = '意见反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class ReportImage(TimestampStatusMixin):
    report = models.ForeignKey(to='Report', on_delete=models.CASCADE, related_name='report_images',
                               verbose_name='问题上报')
    image = models.ImageField(upload_to='upload/report', null=True, blank=True, verbose_name='图片')


class Report(TimestampStatusMixin):
    """
    问题上报
    """
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.DO_NOTHING, verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='联系人')
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    address = models.CharField(max_length=255, verbose_name='地址', blank=True, null=True)
    content = models.TextField(verbose_name='反馈内容')
    reply = models.TextField(verbose_name='回复内容', default=None, blank=True, null=True)

    class Meta:
        verbose_name = '问题上报'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ConsultPhone(TimestampStatusMixin):
    """
    电话咨询管理
    """
    objects = models.Manager()
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    content = models.TextField(verbose_name='具体内容')
    title = models.CharField(max_length=100, blank=True, verbose_name='咨询事项')

    class Meta:
        verbose_name = '电话咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


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
    user = models.ForeignKey(WeChatUser, on_delete=models.DO_NOTHING, verbose_name='用户')
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    content = models.TextField(verbose_name='咨询内容')
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')
    date = models.DateField(verbose_name='预约咨询日期')
    time = models.ForeignKey(ConsultTime, on_delete=models.DO_NOTHING, verbose_name='预约时间', blank=True, null=True)

    class Meta:
        verbose_name = '预约咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Favorite(TimestampStatusMixin):
    """
    收藏
    """
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.DO_NOTHING, verbose_name='用户')
    item = models.CharField(max_length=100, verbose_name='收藏内容')

    class Meta:
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item


class ServiceList(TimestampStatusMixin):
    """
    公共服务清单
    """
    objects = models.Manager()
    sxmc = models.CharField(max_length=100, verbose_name='事项名称')
    blfs = models.CharField(max_length=100, default='直接办理', verbose_name='办理方式')
    fwsj = models.CharField(max_length=100, default="09:00—17:00(周一至周五）", verbose_name='服务时间')
    bjsx = models.CharField(max_length=100, default='即时办理', verbose_name='办结时限')
    fwdx = models.CharField(max_length=100, default="辖区居民", verbose_name='服务对象')
    sxyj = models.CharField(max_length=100, default="身份证、户口簿及相关证明材料", verbose_name='所需要件')

    class Meta:
        verbose_name = '服务清单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sxmc
