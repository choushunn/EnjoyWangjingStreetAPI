from django.contrib import admin
from django.db import models
from django.db.models import OuterRef, Subquery
from django.forms import ClearableFileInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# Register your models here.

from .models import Appointment, TicketReview, Ticket, TicketType, AppointmentType, TicketImage, AppointmentTime


@admin.register(AppointmentType)
class AppointmentAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    预约管理
    """
    list_display = (
        'id', 'user', 'name', 'phone', 'type', 'date', 'remark', 'status', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'name', 'phone')
    list_filter = ('type', 'status', 'is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('user', 'name', 'phone', 'type', 'date', 'remark', 'status',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'user', 'name', 'phone', 'type', 'date', 'remark', 'created_at', 'updated_at')
    fieldsets = (
        (
            None, {
                'fields': ('user', 'name', 'phone', 'type', 'date', 'time', 'remark',)
            }
        ),
        (
            '管理员审核', {
                'fields': ('status', 'reply',)
            }
        )
    )


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    """
    工单类型管理
    """
    fields = ('name',)
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    list_editable = ('is_active',)
    ordering = list_display


@admin.register(AppointmentTime)
class AppointmentTimeAdmin(admin.ModelAdmin):
    """
    工单类型管理
    """
    fields = ('time',)
    list_display = ('id', 'time', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'time')
    list_editable = ('is_active',)
    ordering = list_display


class TicketImageInline(admin.StackedInline):
    model = TicketImage
    exclude = ('is_deleted', 'is_active')
    extra = 1

    formfield_overrides = {
        models.ImageField: {'widget': ClearableFileInput()}
    }

    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                f'<a target="_blank" href="{obj.image.url}"><img src="{obj.image.url}" style="width: 400px;height: '
                f'300px"/></a>')
        else:
            return "无"

    image_tag.short_description = '图像预览'
    fields = ('image_tag', 'image')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [TicketImageInline]
    list_display = (
        'id', 'user', 'worker', 'ticket_type', 'name', 'phone', 'address', 'status', 'created_at', 'updated_at')
    ordering = ('-id',)
    list_display_links = ('id', 'user')
    readonly_fields = (
        'id', 'user', 'name', 'phone', 'ticket_type', 'address', 'description', 'created_at', 'updated_at')
    fieldsets = (
        (
            None, {
                'fields': ('user', 'name', 'phone', 'ticket_type', 'address', 'description',),

            }
        ),
        (
            '管理员审核', {
                'fields': ('worker', 'status', 'replay')
            }
        )
    )


@admin.register(TicketReview)
class TicketReviewAdmin(admin.ModelAdmin):
    exclude = ('is_deleted', 'is_active')
    list_display = (
        'id', 'ticket', 'rating', 'created_at', 'updated_at')
    list_display_links = ('id', 'ticket')
