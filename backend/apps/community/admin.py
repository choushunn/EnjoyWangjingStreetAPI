from django.contrib import admin

from .models import Evaluation, Feedback, Favorite, Consult, Report, ConsultPhone, ConsultTime


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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
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
        ),

    )


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
    上报管理
    """
    list_display = ('id', 'user', 'title', 'phone', 'type', 'content', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'type', 'content')
    list_filter = ('is_active', 'type',)
    ordering = list_display
    list_editable = ('is_active',)
    search_fields = ('title', 'phone', 'type', 'content',)
    date_hierarchy = 'created_at'
    exclude = ('is_deleted',)
    readonly_fields = ('id', 'user', 'title', 'phone', 'type', 'content', 'created_at', 'updated_at')
    fieldsets = (
        (
            None,
            {
                'fields': ('user', 'title', 'phone', 'type',)
            }
        ), (
            '附件',
            {
                'fields': ('content',)
            }
        )
    )
