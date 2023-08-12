from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Message, WeChatUser, Favorite, \
    Feedback, Evaluation, Consult, Report, ConsultPhone, ReportImage, FeedbackImages
from .serializers import MessageSerializer, WeChatUserSerializer, FavoriteSerializer, FeedbackSerializer, \
    EvaluationSerializer, ConsultSerializer, ReportSerializer, ConsultPhoneSerializer, ReportImageSerializer, \
    FeedbackImagesSerializer, WeChatUserCreateSerializer
from ..common.auth import OpenidAuthentication


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


class EvaluationViewSet(viewsets.ModelViewSet):
    """
    评价接口 GET
    """
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    反馈接口 GET
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Feedback.objects.filter(user=request.user.id)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class FeedbackImagesViewSet(viewsets.ModelViewSet):
    """
    反馈意见图像上传接口 GET/POST
    """
    queryset = FeedbackImages.objects.all()
    serializer_class = FeedbackImagesSerializer


class ReportImageViewSet(viewsets.ModelViewSet):
    """
    问题上报图像上传接口 GET/POST
    """
    queryset = ReportImage.objects.all()
    serializer_class = ReportImageSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    问题上报接口 GET
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Report.objects.filter(user=request.user.id)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class ConsultPhoneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    预约咨询接口 GET
    """
    queryset = ConsultPhone.objects.all()
    serializer_class = ConsultPhoneSerializer


class ConsultViewSet(viewsets.ModelViewSet):
    """
    预约咨询接口 GET
    """
    queryset = Consult.objects.all()
    serializer_class = ConsultSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Consult.objects.filter(user=request.user.id)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    收藏接口 GET/POST
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        return self.queryset.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Message.objects.filter(user=request.user.id).order_by('-created_at')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
