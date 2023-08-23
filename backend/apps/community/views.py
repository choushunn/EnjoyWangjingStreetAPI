from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite, \
    Feedback, Evaluation, Consult, Report, ConsultPhone, ReportImage, FeedbackImages, ConsultTime
from .serializers import FavoriteSerializer, FeedbackSerializer, \
    EvaluationSerializer, ConsultSerializer, ReportSerializer, ConsultPhoneSerializer, ReportImageSerializer, \
    FeedbackImagesSerializer, ConsultTimeSerializer

from ..common.auth import OpenidAuthentication
from ..system.helpers import send_message


class EvaluationViewSet(viewsets.ModelViewSet):
    """
    评价接口 GET
    """
    queryset = Evaluation.objects.all().filter(is_active=True)
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

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Report.objects.filter(user=request.user.id)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class ConsultPhoneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    预约咨询接口 GET
    """
    queryset = ConsultPhone.objects.all().filter(is_active=True)
    serializer_class = ConsultPhoneSerializer


class ConsultTimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    预约时间接口 GET
    """
    queryset = ConsultTime.objects.all().filter(is_active=True)
    serializer_class = ConsultTimeSerializer


class ConsultViewSet(viewsets.ModelViewSet):
    """
    预约咨询接口 GET
    """
    queryset = Consult.objects.all()
    serializer_class = ConsultSerializer
    permission_classes = [IsAuthenticated, ]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_message(request.user.id, m_type="预约咨询", content="您已提交预约咨询。请耐心等待工作人员的回复")
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
