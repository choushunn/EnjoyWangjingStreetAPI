from django.contrib import admin

# Register your models here.

from .models import Notification, TelephoneDirectory, News, Activity, NewsTags, NewsCategory
from ..system.helpers import send_subscription_message
from ..system.models import WeChatUser


@admin.register(TelephoneDirectory)
class TelephoneDirectoryAdmin(admin.ModelAdmin):
    """
    便民电话
    """
    fields = ('title', 'number', 'type', 'address')
    list_display = ('title', 'number', 'address', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('title', 'number', 'address')
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


# @admin.register(NewsTags)
# class NewsTagsAdmin(admin.ModelAdmin):
#     """
#     新闻管理
#     """
#     fields = ('name', 'color')
#     list_display = ('name', 'color', 'is_active', 'created_at', 'updated_at')
#     list_display_links = ('name', 'color',)
#     list_filter = ('name', 'color', 'is_active',)
#     ordering = list_display
#     list_editable = ('is_active',)
#     search_fields = ('name',)
#     date_hierarchy = 'created_at'
#     exclude = ('is_deleted',)
#     readonly_fields = ('id', 'created_at', 'updated_at')


# @admin.register(NewsCategory)
# class NewsCategoryAdmin(admin.ModelAdmin):
#     """
#     新闻管理
#     """
#     fields = ('name',)
#     list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
#     list_display_links = ('id', 'name',)
#     list_filter = ('name', 'is_active',)
#     ordering = list_display
#     list_editable = ('is_active',)
#     search_fields = ('name',)
#     date_hierarchy = 'created_at'
#     exclude = ('is_deleted',)
#     readonly_fields = ('id', 'created_at', 'updated_at')


# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     """
#     新闻管理
#     """
#     list_display = ('title', 'summary', 'category', 'is_active', 'image', 'created_at', 'updated_at')
#     list_display_links = ('title', 'summary', 'category')
#     list_filter = ('category', 'is_active',)
#     ordering = list_display
#     list_editable = ('is_active',)
#     search_fields = ('title', 'summary', 'category',)
#     date_hierarchy = 'created_at'
#     exclude = ('is_deleted',)
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (None, {'fields': ('title', 'content', 'summary', 'image', 'category')}),
#         ('新闻标签', {
#             'fields': ('tags',)
#         })
#     )
#     filter_horizontal = ('tags',)
#
#     def save_model(self, request, obj, form, change):
#         # 获取当前登录用户
#         current_user = request.user
#         # 在保存对象之前设置发送者为当前用户
#         obj.creator = current_user
#
#         super().save_model(request, obj, form, change)


# @admin.register(Activity)
# class ActivityAdmin(admin.ModelAdmin):
#     """
#     活动管理
#     """
#     fields = ('title', 'content', 'summary', 'category', 'image')
#     list_display = ('title', 'is_active', 'created_at', 'updated_at')
#     list_display_links = ('title',)
#     list_filter = ('is_active',)
#     ordering = list_display
#     list_editable = ('is_active',)
#     search_fields = ('title', 'content',)
#     date_hierarchy = 'created_at'
#     exclude = ('is_deleted',)
#     readonly_fields = ('id', 'created_at', 'updated_at')
#
#     def save_model(self, request, obj, form, change):
#         # 获取当前登录用户
#         current_user = request.user
#
#         # 在保存对象之前设置发送者为当前用户
#         obj.creator = current_user
#
#         super().save_model(request, obj, form, change)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('content',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'sender', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('content', 'summary',)
        }),
    )

    # filter_horizontal = ('receivers',)

    def save_model(self, request, obj, form, change):
        # 获取当前登录用户
        current_user = request.user

        # 在保存对象之前设置发送者为当前用户
        obj.sender = current_user
        # Send notification to all users
        users = WeChatUser.objects.all().filter(is_active=False)
        for user in users:
            self.send_notice(user, obj)

        super().save_model(request, obj, form, change)

    def send_notice(self, user, obj):
        openid = user.open_id
        template_id = 'ulg9KZqdxKK_CqX4cQ_l3mIu0-vt5fcmqsHSo1ImQTI'
        data = {
            "thing1": {
                "value": "王井社区居委会"
            },
            "thing2": {
                "value": obj.content
            },
            "time3": {
                "value": obj.created_at.strftime("%Y-%m-%d %H:%M")
            },
            "thing4": {
                "value": obj.summary
            },
        }

        send_subscription_message(openid, template_id, data)
