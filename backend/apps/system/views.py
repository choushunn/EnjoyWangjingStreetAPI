from .models import Carousel, SystemParams, MenuItem, MenuCategory, Pages
from .serializers import CarouselSerializer, SystemParamsSerializer, MenuItemSerializer, MenuCategorySerializer, \
    PagesSerializer

from rest_framework import viewsets


class CarouselViewSet(viewsets.ReadOnlyModelViewSet):
    """
    轮播图 GET
    """
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer


class SystemParamsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    参数 GET
    """
    queryset = SystemParams.objects.all()
    serializer_class = SystemParamsSerializer


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    菜单项 GET
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    菜单类别 GET
    """
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class PagesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    菜单类别 GET
    """
    queryset = Pages.objects.all()
    serializer_class = PagesSerializer
