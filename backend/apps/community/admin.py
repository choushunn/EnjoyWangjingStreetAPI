from django.contrib import admin
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin

from .models import Evaluation, Feedback, Favorite, Consult, Report, ConsultPhone, ConsultTime, ServiceList
from ..system.helpers import send_subscription_message


@admin.register(ServiceList)
class ServiceListAdmin(admin.ModelAdmin):
    """
    预约时间管理
    """
    fields = ('sxmc', 'blfs', 'fwsj', 'bjsx', 'fwdx', 'sxyj')
    list_display = ('id', 'sxmc', 'blfs', 'fwsj', 'bjsx', 'fwdx', 'sxyj', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'sxmc')
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted', 'is_active')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(ConsultTime)
class ConsultTimeAdmin(admin.ModelAdmin):
    """
    预约时间管理
    """
    fields = ('time',)
    list_display = ('id', 'time', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'time')
    list_editable = ('is_active',)
    ordering = list_display


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """
    评价管理
    """
    list_display = ('id', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    # search_fields = ('title', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted', 'is_active')
    readonly_fields = ('id', 'created_at', 'updated_at')


from datetime import datetime


@admin.register(Feedback)
class FeedbackAdmin(AjaxAdmin):
    """
    反馈管理
    """
    list_display = ('id', 'user', 'content', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'content')
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'user', 'content', 'created_at', 'updated_at')
    # 用户反馈意见只读，回复意见可读
    fieldsets = (
        (
            None,
            {
                'fields': ('user', 'content',)
            }
        ), (
            '管理员回复',
            {
                'fields': ('replay',)
            }
        )

    )

    def save_model(self, request, obj, form, change):
        openid = obj.user.open_id
        template_id = 'aAuVyMBl3gscHus9WJzI8wnWUj-rvpVdpdBlkmnJ754'
        data = {
            "thing1": {
                "value": "反馈结果通知"
            },
            "time2": {
                "value": obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
            },
            "thing4": {
                "value": obj.replay
            },
            "time5": {
                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        if 'replay' in form.changed_data:
            send_subscription_message(openid, template_id, data)
        obj.save()


@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    """
    咨询管理
    """
    fields = ('user', 'phone', 'content', 'address')
    list_display = ('id', 'user', 'phone', 'content', 'address', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'phone')
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('phone', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(ConsultPhone)
class ConsultPhoneAdmin(admin.ModelAdmin):
    """
    电话咨询管理
    """
    fields = ('title', 'phone', 'content',)
    list_display = ('id', 'phone', 'content', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'phone')
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('phone', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    收藏管理
    """
    list_display = ('id', 'user', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    问题上报
    """
    list_display = ('id', 'user', 'name', 'phone', 'address', 'content', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'address', 'content')
    list_filter = ('is_active', 'address',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'phone', 'address', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'user', 'name', 'phone', 'address', 'content', 'created_at', 'updated_at')
    fieldsets = (
        (
            None,
            {
                'fields': ('user', 'name', 'phone', 'address','content')
            }
        ), (
            '回复',
            {
                'fields': ('reply',)
            }
        )
    )

    def save_model(self, request, obj, form, change):
        openid = obj.user.open_id
        template_id = 'aAuVyMBl3gscHus9WJzI80tADXMnBu48K0f6bMwvNe8'
        data = {
            "thing1": {
                "value": obj.content
            },
            "time2": {
                "value": obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
            },
            "thing4": {
                "value": obj.reply
            },
            "thing3": {
                "value": "王井社区居委会"
            },
            "time5": {
                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        if 'reply' in form.changed_data:
            send_subscription_message(openid, template_id, data)
        obj.save()
