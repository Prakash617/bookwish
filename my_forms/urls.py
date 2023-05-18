from django.urls import path
from .views import feedback_view, feedback_success

urlpatterns = [
    path('event/feedback/', feedback_view, name='event_feedback_form'),
    path('event/feedback/success/', feedback_success, name='feedback_success'),
]
