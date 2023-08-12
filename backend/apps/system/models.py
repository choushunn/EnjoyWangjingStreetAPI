from django.db import models

from ..common.models import TimestampStatusMixin


# Create your models here.


class ActiveCarouselManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Carousel(TimestampStatusMixin):
    title = models.CharField(max_length=255, verbose_name='标题')
    image = models.ImageField(upload_to='upload/carousel', verbose_name='轮播图')
    target_url = models.CharField(max_length=255, default='', blank=True, verbose_name='跳转链接')
    description = models.CharField(max_length=255, default='', blank=True, verbose_name='轮播图说明')
    objects = models.Manager()
    active_objects = ActiveCarouselManager()

    class Meta:
        verbose_name = '首页宣传图'
        verbose_name_plural = '首页宣传图'

    def __str__(self):
        return self.title


class SystemParams(TimestampStatusMixin):
    key = models.CharField(max_length=255, verbose_name='参数名')
    value = models.CharField(max_length=255, default='', blank=True, verbose_name='参数值')
    description = models.CharField(max_length=255, default='', blank=True, verbose_name='参数说明')
    objects = models.Manager()

    class Meta:
        verbose_name = '系统参数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.key


class MenuCategory(TimestampStatusMixin):
    name = models.CharField(max_length=255, verbose_name='菜单名称')
    url = models.CharField(max_length=255, default='', verbose_name='菜单链接')
    icon = models.CharField(max_length=255, default='', blank=True, verbose_name='菜单图标')
    color = models.CharField(max_length=255, default='', blank=True, verbose_name='菜单颜色')
    items = models.ManyToManyField('MenuItem', blank=True, verbose_name='菜单项')
    objects = models.Manager()

    class Meta:
        verbose_name = '菜单类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MenuItem(TimestampStatusMixin):
    name = models.CharField(max_length=255, verbose_name='菜单项名称')
    url = models.CharField(max_length=255, default='', verbose_name='菜单项链接')
    icon = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name='菜单项图标')
    color = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name='菜单项颜色')
    appid = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name='菜单项appid')
    objects = models.Manager()

    class Meta:
        verbose_name = '菜单项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MenuColor(TimestampStatusMixin):
    name = models.CharField(max_length=255, verbose_name='菜单颜色')
    code = models.CharField(max_length=255, default='', blank=True, verbose_name='颜色代码')
    objects = models.Manager()

    class Meta:
        verbose_name = '菜单颜色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Pages(TimestampStatusMixin):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=True, verbose_name='页面标识')
    title = models.CharField(max_length=255, verbose_name='页面标题')
    content = models.TextField(verbose_name='页面内容')
    signature = models.CharField(max_length=255, default='', blank=True, verbose_name='页面署名')

    class Meta:
        verbose_name = '页面管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
