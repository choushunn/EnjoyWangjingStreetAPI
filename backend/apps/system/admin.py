from adminlteui.core import AdminlteConfig
from django.contrib import admin

from .models import Carousel, SystemParams, MenuCategory, MenuItem, Pages

admin.site.site_title = "微信小程序后台管理系统"
admin.site.site_header = "乐享王井街"


class MyAdminlteConfig(AdminlteConfig):
    skin = 'green'
    welcome_sign = '微信小程序后台管理系统'
    show_avatar = False
    copyright = '乐享王井街微信小程序后台管理系统'


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
class MenuItemAdmin(admin.ModelAdmin):
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
    fields = ('title', 'content')
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
