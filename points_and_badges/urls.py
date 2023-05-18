from django.urls import path
from .views import *

from .views import *
urlpatterns = [
    path('api/weekly-badges/', CombineWeeklyPointsView.as_view(), name='api-weekly-badges'),
    path('api/weekly-badges/download', DownloadExcel.as_view(), name='api-notification-download'),
    path('api/daily-badges/', CombineDailyPointsView.as_view(), name='api-daaily-badges'),
    path('api/export_csv/<int:pk>', export_csv, name='export_csv'),
    path('api/community_weekly_badges_csv/<int:pk>', community_weekly_badges_csv, name='community_weekly_badges_csv'),
    path('api/all_community_export_csv', all_community_export_csv, name='all_community_export_csv'),
    path('api/ClubBadegeView', ClubBadegeView.as_view(), name='ClubBadegeView'),
]
