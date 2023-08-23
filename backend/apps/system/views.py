import hashlib
import os

import django_filters
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import Carousel, SystemParams, MenuItem, MenuCategory, Pages, Message
from .serializers import CarouselSerializer, SystemParamsSerializer, MenuItemSerializer, MenuCategorySerializer, \
    PagesSerializer, MessageSerializer, WeChatUserSerializer, WeChatUserCreateSerializer, \
    WeChatUserAvatarUpdateSerializer, WeChatUserUpdateSerializer, WeChatUserCreatePhoneSerializer

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import WeChatUser
from django_filters import rest_framework as filters
from ..common.auth import OpenidAuthentication
from backend.settings import AVATAR_ROOT, AVATAR_URL


class CarouselViewSet(viewsets.ReadOnlyModelViewSet):
    """
    轮播图 GET
    """
    queryset = Carousel.objects.all().filter(is_active=True)
    serializer_class = CarouselSerializer


class SystemParamsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    参数 GET
    """
    queryset = SystemParams.objects.all().filter(is_active=True)
    serializer_class = SystemParamsSerializer
    # filter_backends = []


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    菜单项 GET
    """
    queryset = MenuItem.objects.all().filter(is_active=True)
    serializer_class = MenuItemSerializer


class MenuCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    菜单类别 GET
    """
    queryset = MenuCategory.objects.all().filter(is_active=True)
    serializer_class = MenuCategorySerializer
    filterset_fields = ['name', 'url']


class PagesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    页面类别 GET
    """
    queryset = Pages.objects.all().filter(is_active=True)
    serializer_class = PagesSerializer
    filterset_fields = ['name', ]


class MessageViewSet(mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    消息接口 GET
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def get_queryset(self):
        # 当前用户的数据
        return self.queryset.filter(receiver=self.request.user.id).order_by('-created_at').filter(is_active=True)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'success', 'message': '消息已标记为已读'})

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
        return self.queryset.filter(id=self.request.user.id).order_by('-created_at').filter(is_active=True)

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


class CheckSignatureAPIView(APIView):
    def get(self, request):
        signature = request.GET.get("signature")
        timestamp = request.GET.get("timestamp")
        nonce = request.GET.get("nonce")
        echostr = request.GET.get("echostr")
        token = "weChatMessagePush1"
        if signature and timestamp and nonce:
            data = [token, timestamp, nonce]
            data.sort()
            sha1 = hashlib.sha1()
            sha1.update("".join(data).encode())
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                return Response(data={"echostr": echostr}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"echostr": echostr}, status=status.HTTP_403_FORBIDDEN)


class WeChatUserAvatarUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OpenidAuthentication]

    def post(self, request):
        user = request.user
        serializer = WeChatUserAvatarUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # 保存新头像
            avatar = request.data.get('avatar')
            file_extension = os.path.splitext(avatar.name)[1]
            new_avatar_name = f"{user.open_id}{file_extension}"
            avatar_path = os.path.join(AVATAR_ROOT, new_avatar_name)

            # 将头像文件保存到指定路径
            with open(avatar_path, 'wb') as file:
                file.write(avatar.read())

            # 更新用户对象的头像字段
            serializer.save(avatar=os.path.join(AVATAR_URL, new_avatar_name))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeChatUserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OpenidAuthentication]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = WeChatUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeChatUserCreateAPIView(APIView):
    """
    用户注册接口
    """

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = WeChatUserCreatePhoneSerializer(data=request.data)
        open_id = serializer.get_open_id()
        phone = serializer.get_phone()
        try:
            user = WeChatUser.objects.get(open_id=open_id)
            # 手动签发jwt token
            refresh = RefreshToken.for_user(user)
            resp_data = {
                'user_id': user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(resp_data, status=status.HTTP_200_OK)
        except WeChatUser.DoesNotExist:
            if phone and open_id:
                # self.perform_create(serializer)
                created_object = WeChatUser.objects.create(
                    nickname='',
                    avatar='',
                    open_id=open_id,
                    phone=phone
                )
                # 创建用户
                user = created_object
                # 手动签发jwt token
                refresh = RefreshToken.for_user(user)
                resp_data = {
                    'user_id': user.id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
                return Response(resp_data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={"message": "注册失败，参数错误"}, status=status.HTTP_406_NOT_ACCEPTABLE)


from django.shortcuts import render


def home(request):
    return render(request, 'home.html')
