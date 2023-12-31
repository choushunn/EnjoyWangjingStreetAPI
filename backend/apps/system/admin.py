# from adminlteui.core import AdminlteConfig
from django.contrib import admin
from simpleui.admin import AjaxAdmin

from .models import Carousel, SystemParams, MenuCategory, MenuItem, Pages, Message
from ..community.models import WeChatUser

admin.site.site_title = "乐享王井街微信小程序后台管理系统"
admin.site.site_header = "乐享王井街后台管理系统"


# class MyAdminlteConfig(AdminlteConfig):
#     skin = 'green'
#     welcome_sign = '微信小程序后台管理系统'
#     show_avatar = False
#     copyright = '乐享王井街微信小程序后台管理系统'


# Register your models here.
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """
    轮播图
    """
    fields = ('title', 'image', 'target_url', 'description')
    list_display = ('id', 'title', 'image', 'target_url', 'description', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'image', 'target_url', 'description',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'description',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(SystemParams)
class SystemParamsAdmin(admin.ModelAdmin):
    """
    系统参数
    """
    fields = ('key', 'value', 'description')
    list_display = ('id', 'key', 'value', 'description', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'key')
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('key', 'value', 'description',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    """
    菜单类别
    """
    list_display = ('id', 'name', 'url', 'icon', 'color', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'url')
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('name', 'url', 'icon', 'color',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('items',)

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "url"],
            },
        ),
        (
            "增加",
            {
                # "classes": ["collapse"],
                "fields": ["icon", "color"],
                "description": "选填项",
            },

        ),
        (
            "添加",
            {
                # "classes": ["collapse"],
                "fields": ["items", ],
                "description": "菜单项",
            },
        )
    ]
    filter_vertical = ('items',)


@admin.register(MenuItem)
class MenuItemAdmin(AjaxAdmin):
    """
    菜单项
    """
    list_display = ('id', 'name', 'url', 'icon', 'color', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'name',)
    ordering = list_display
    list_editable = ('url', 'icon', 'color', 'is_active',)
    search_fields = ('name', 'url', 'icon', 'color',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "url"],
            },
        ),
        (
            "选填项",
            {
                "fields": ["icon", "color", "appid"],
            },
        ),
    ]


@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    """
    页面管理
    """
    fields = ('name', 'title', 'content', 'signature')
    list_display = ( 'title', 'name', 'signature', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('name', 'title', 'signature')
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('name', 'title',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    消息管理
    """
    fields = ('type', 'content', 'receiver')
    list_display = ('id', 'type', 'is_read', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('is_active',)
    ordering = list_display
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(WeChatUser)
class WeChatUserAdmin(admin.ModelAdmin):
    """
    微信用户管理
    """
    fields = ('open_id', 'nickname', 'avatar', 'phone', 'address', 'gender', 'role')
    list_display = (
        'id', 'open_id', 'nickname', 'name', 'phone', 'address', 'gender', 'role', 'is_active', 'created_at',
        'updated_at')
    list_display_links = ('id', 'open_id', 'nickname', 'phone',)
    list_filter = ('gender', 'role', 'is_active',)
    ordering = list_display
    list_editable = ('is_active', 'gender', 'role')
    search_fields = ('open_id', 'nickname', 'phone', 'address')
    date_hierarchy = 'created_at'
    exclude = ('id', 'is_deleted',)
    readonly_fields = ('id', 'created_at', 'updated_at')
