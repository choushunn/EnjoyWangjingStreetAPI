from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appointment, Ticket, TicketType, AppointmentType, AppointmentTime, TicketImage
from .serializers import AppointmentSerializer, TicketSerializer, TicketTypeSerializer, AppointmentTimeSerializer, \
    AppointmentTypeSerializer, TicketImageSerializer

from ..common.auth import OpenidAuthentication
from ..system.helpers import send_message


class AppointmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    预约类型接口 GET
    """
    queryset = AppointmentType.objects.all()
    serializer_class = AppointmentTypeSerializer


class AppointmentTimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    预约时间接口 GET
    """
    queryset = AppointmentTime.objects.all()
    serializer_class = AppointmentTimeSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    预约接口 GET/POST
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]  # 增加此行
    authentication_classes = [OpenidAuthentication, ]  # 增加此行

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_message(request.user.id, m_type="服务预约", content="您已提交预约服务。请耐心等待工作人员的回复")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        appointments = Appointment.objects.filter(user=self.request.user.id).order_by('-created_at')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # 当前用户的数据
        return self.queryset.filter(user=self.request.user.id).order_by('-created_at')


class TicketTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    工单类型接口 GET
    """
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class TicketImageViewSet(viewsets.ModelViewSet):
    """
    工单图像上传接口 GET/POST
    """
    queryset = TicketImage.objects.all()
    serializer_class = TicketImageSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    工单管理接口 GET/POST
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    ordering_fields = ['created_at', 'id', 'ticket_type']
    permission_classes = [IsAuthenticated]  # 权限
    authentication_classes = [OpenidAuthentication, ]  # 认证

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_message(request.user.id, m_type="居民服务", content="你已提交居民服务，请耐心等待工作人员的回复")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # 当前用户的数据
        return Ticket.objects.filter(user=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        tickets = Ticket.objects.filter(user=self.request.user.id).order_by('-created_at')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
