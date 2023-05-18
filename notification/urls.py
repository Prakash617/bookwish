from django.urls import path
from .views import NotificationView,AdminNotificationView
urlpatterns = [
    path('api/notification/', NotificationView.as_view(), name='api-notification'),
    path('api/admin-notification/', AdminNotificationView.as_view(), name='api-adminnotification'),
]
