from django.shortcuts import render
from .models import Notification,AdminNotification
from .serializers import NotificationSerializer,AdminNotificationSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,ListAPIView
# from django.views.generic.list import ListView
from rest_framework import status

# Create your views here.
class NotificationView(ListCreateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        notification = Notification.objects.filter(revoker=request.user).order_by('-upload_timestamp')
        data = NotificationSerializer(notification, many=True, context={"request":request}).data
        
        return Response(data)
class AdminNotificationView(ListAPIView):
    serializer_class = AdminNotificationSerializer
    queryset = AdminNotification.objects.all()