from django.urls import path
from .views import (
    AssessmentList,
    AssessmentDetailView,
    AssessmentScoresViewSet,
    AssessmentCriteriaView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/assess',AssessmentScoresViewSet, basename= 'assessment_scores')
# router.register(r'api/assess/<int:pk>',AssessmentScoresViewSet, basename= 'assessment_scores')

urlpatterns = [
    path('api/assessment', AssessmentList.as_view(), name="assesment"),
    path('api/assessment/<int:id>', AssessmentDetailView.as_view(), name="assesment_detail"),
    path('api/assessment-criteria', AssessmentCriteriaView.as_view(), name="AssessmentCriteriaView")
]
urlpatterns += router.urls