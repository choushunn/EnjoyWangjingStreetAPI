from django.db import models

from ..common.models import TimestampStatusMixin


# Create your models here.

class WeChatUser(TimestampStatusMixin):
    """
    微信登录用户
    """
    GENDER = (
        (1, "男"),
        (2, "女"),
        (3, "保密"),
    )
    ROLES = (
        (0, '用户'),
        (1, '工作人员'),
        (2, '管理员'),
        (3, '超级管理员'),
    )
    objects = models.Manager()
    open_id = models.CharField(max_length=255, unique=True, verbose_name='微信用户唯一标识')
    nickname = models.CharField(max_length=100, verbose_name='昵称')
    avatar = models.ImageField(upload_to='upload/avatar', verbose_name='头像')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='手机号码')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址')
    gender = models.IntegerField(default=3, choices=GENDER, null=True, blank=True, verbose_name='性别')
    role = models.IntegerField(default=0, choices=ROLES, null=True, blank=True, verbose_name='角色')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='姓名')

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


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


class Message(TimestampStatusMixin):
    """
    系统消息
    """
    objects = models.Manager()
    receiver = models.ManyToManyField(WeChatUser, verbose_name='接收者',
                                      blank=True)
    type = models.CharField(max_length=100, verbose_name='消息类型')
    content = models.TextField(verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '消息管理'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.sender
