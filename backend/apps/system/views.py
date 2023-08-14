from .models import Carousel, SystemParams, MenuItem, MenuCategory, Pages, Message
from .serializers import CarouselSerializer, SystemParamsSerializer, MenuItemSerializer, MenuCategorySerializer, \
    PagesSerializer, MessageSerializer, WeChatUserSerializer, WeChatUserCreateSerializer

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import WeChatUser

from ..common.auth import OpenidAuthentication


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


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    消息接口 GET
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def get_queryset(self):
        # 当前用户的数据
        return self.queryset.filter(receiver=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Message.objects.filter(user=request.user.id).order_by('-created_at')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class WeChatUserViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    用户个人信息接口 GET/POST
    """
    queryset = WeChatUser.objects.all()
    serializer_class = WeChatUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [OpenidAuthentication, ]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WeChatUserCreateSerializer
        return WeChatUserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return super().get_permissions()

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = WeChatUser.objects.get(open_id=serializer.validated_data['open_id'])
            # 手动签发jwt token
            refresh = RefreshToken.for_user(user)
            resp_data = {
                'user_id': user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(resp_data, status=status.HTTP_200_OK)
        except WeChatUser.DoesNotExist:
            if serializer.validated_data['phone'] and serializer.validated_data['open_id']:
                self.perform_create(serializer)
                user = serializer.instance
                # 手动签发jwt token
                refresh = RefreshToken.for_user(user)
                resp_data = {
                    'user_id': user.id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
                return Response(resp_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
