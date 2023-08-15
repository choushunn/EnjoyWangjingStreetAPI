"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from . import settings
from rest_framework.routers import DefaultRouter

from apps.community import views as community_views
from apps.info import views as info_views
from apps.work import views as work_views
from apps.system import views as system_views

router = DefaultRouter()


router.register(r'evaluation', community_views.EvaluationViewSet)
router.register(r'feedback_image', community_views.FeedbackImagesViewSet)
router.register(r'feedback', community_views.FeedbackViewSet)
router.register(r'favorite', community_views.FavoriteViewSet)

router.register(r'consult', community_views.ConsultViewSet)
router.register(r'consult_phone', community_views.ConsultPhoneViewSet)
router.register(r'report_image', community_views.ReportImageViewSet)
router.register(r'report', community_views.ReportViewSet)

router.register(r'telephone', info_views.TelephoneDirectoryViewSet)
router.register(r'news', info_views.NewsViewSet)
router.register(r'activity', info_views.ActivityViewSet)
router.register(r'notification', info_views.NotificationViewSet)

router.register(r'carousel', system_views.CarouselViewSet)
router.register(r'system_params', system_views.SystemParamsViewSet)
router.register(r'menu_category', system_views.MenuCategoryViewSet)
router.register(r'pages', system_views.PagesViewSet)
router.register(r'message', system_views.MessageViewSet)
router.register(r'user', system_views.WeChatUserViewSet)
router.register(r'appointment', work_views.AppointmentViewSet)
router.register(r'appointment_type', work_views.AppointmentTypeViewSet)
router.register(r'appointment_time', work_views.AppointmentTimeViewSet)
router.register(r'work', work_views.TicketViewSet)
router.register(r'work_image', work_views.TicketImageViewSet)
router.register(r'work_type', work_views.TicketTypeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]

# 添加静态文件的 URL 映射
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 添加 media 文件的 URL 映射
urlpatterns += static('/upload/', document_root=settings.MEDIA_ROOT + '/upload/')
urlpatterns += static('/avatar/', document_root=settings.AVATAR_ROOT)
