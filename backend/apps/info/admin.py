from django.contrib import admin
from django.db import models
from django.forms import ClearableFileInput
from django.utils.html import format_html

# Register your models here.

from .models import Notification, TelephoneDirectory, News, Activity, NewsTags, NewsCategory


@admin.register(TelephoneDirectory)
class TelephoneDirectoryAdmin(admin.ModelAdmin):
    """
    便民电话
    """
    fields = ('title', 'number', 'address')
    list_display = ('id', 'title', 'number', 'address', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'number', 'address')
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'number', 'address',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_help_text = '搜索便民电话'

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        obj.save()


@admin.register(NewsTags)
class NewsTagsAdmin(admin.ModelAdmin):
    """
    新闻管理
    """
    fields = ('name', 'color')
    list_display = ('id', 'name', 'color', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'color',)
    list_filter = ('name', 'color', 'is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """
    新闻管理
    """
    fields = ('name',)
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    新闻管理
    """
    list_display = ('id', 'title', 'summary', 'category', 'is_active', 'image', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'summary', 'category')
    list_filter = ('category', 'is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'summary', 'category',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'content', 'summary', 'image', 'category')}),
        ('新闻标签', {
            'fields': ('tags',)
        })
    )
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        # 获取当前登录用户
        current_user = request.user
        # 在保存对象之前设置发送者为当前用户
        obj.creator = current_user

        super().save_model(request, obj, form, change)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    活动管理
    """
    fields = ('title', 'summary', 'content', 'category', 'image')
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # 获取当前登录用户
        current_user = request.user

        # 在保存对象之前设置发送者为当前用户
        obj.creator = current_user

        super().save_model(request, obj, form, change)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'title',  'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'sender', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'content', 'attachment')
        }),
        ('接收人', {
            'fields': ('receivers',)
        })
    )
    filter_horizontal = ('receivers',)

    def save_model(self, request, obj, form, change):
        # 获取当前登录用户
        current_user = request.user

        # 在保存对象之前设置发送者为当前用户
        obj.sender = current_user

        super().save_model(request, obj, form, change)
