from django.core.validators import RegexValidator
from django.db import models

from ..common.models import TimestampStatusMixin
from ..community.models import WeChatUser
from ..system.helpers import send_message


class AppointmentTime(TimestampStatusMixin):
    time = models.CharField(max_length=100, verbose_name='预约时间段')

    class Meta:
        verbose_name = '预约时间'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.time)


class AppointmentType(TimestampStatusMixin):
    name = models.CharField(max_length=100, verbose_name='预约类型')

    class Meta:
        verbose_name = '预约类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Appointment(TimestampStatusMixin):
    """
    预约管理
    """
    STATUS_CHOICES = [
        (0, '待审核'),
        (1, '已通过'),
        (2, '已驳回'),
        (3, '已完成')
    ]
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='微信用户')
    name = models.CharField(max_length=100, verbose_name='预约人姓名')
    phone = models.CharField(max_length=100, verbose_name='联系电话')
    type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE, verbose_name='预约类型', blank=True,
                             null=True)
    date = models.DateField(verbose_name='预约日期', blank=True, null=True)
    time = models.ForeignKey(AppointmentTime, on_delete=models.CASCADE, verbose_name='预约时间', blank=True, null=True)
    remark = models.TextField(verbose_name='其他备注信息', blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='预约状态')
    reply = models.TextField(verbose_name='回复', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original_instance = Appointment.objects.get(pk=self.pk)
            if original_instance.status != self.status:
                status_display = dict(self.STATUS_CHOICES).get(self.status)
                send_message(self.user, m_type="预约管理", content=f"您提交的服务预约 {status_display}。")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TicketType(TimestampStatusMixin):
    name = models.CharField(max_length=100, verbose_name='工单类型')

    class Meta:
        verbose_name = '工单类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TicketImage(TimestampStatusMixin):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, verbose_name='工单', related_name='ticket_images')
    image = models.ImageField(upload_to='upload/ticket', verbose_name='图片')

    class Meta:
        verbose_name = '工单图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '图像'


class Ticket(TimestampStatusMixin):
    """
    工单
    """
    phone_regex = RegexValidator(
        regex=r'^\+?\d{1,3}[-.\s]?\d{1,14}$',
        message="请输入有效的电话号码。"
    )
    STATUS = ((0, '待处理'), (1, '处理中'), (2, '已完成'),)
    objects = models.Manager()
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, verbose_name='用户')
    worker = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, related_name='worker_tickets',
                               limit_choices_to={'role__in': (1, 2)}, verbose_name='工作人员', blank=True,
                               null=True)
    admin = models.ForeignKey(WeChatUser, on_delete=models.CASCADE, related_name='admin_tickets',
                              limit_choices_to={'role': 2}, blank=True, null=True, verbose_name='管理员')
    name = models.CharField(max_length=30, verbose_name='姓名')
    phone = models.CharField(max_length=15, validators=[phone_regex], verbose_name='联系电话')
    address = models.CharField(max_length=100, verbose_name='地址', blank=True, null=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, verbose_name='工单类型', blank=True,
                                    null=True, related_name='ticket_type')
    description = models.TextField(verbose_name='问题描述', blank=True, null=True)
    status = models.IntegerField(default=0, choices=STATUS, blank=True, null=True, verbose_name='工单状态')
    replay = models.TextField(verbose_name='回复信息', blank=True, null=True)

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.pk:
            original_instance = Appointment.objects.get(pk=self.pk)
            if original_instance.status != self.status:
                status_display = dict(self.STATUS).get(self.status)
                send_message(self.user, m_type="居民服务", content=f"您提交的居民服务 {status_display}。")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.nickname + '-'


class TicketReview(TimestampStatusMixin):
    """
    工单评价
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单', related_name='ticket_reviews')
    comment = models.TextField(verbose_name='评价内容', blank=True, null=True)
    rating = models.IntegerField(verbose_name='评分', choices=[
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星')
    ], blank=True, null=True)

    class Meta:
        verbose_name = '工单评价'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ticket
