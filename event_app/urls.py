from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# Adding Questions Section
router.register(r'event/registration',EventRegistrationView,basename='event/registration')
router.register(r'event/mcq',MCQQuestionViewSet,basename='event/mcq')
router.register(r'event/written',WrittenQuestionViewSet,basename='event/written')
router.register(r'event/polls',PollQuestionViewSet,basename='event/polls')
router.register(r'event/answer/mcq',EventMcqAnswerViewSet,basename='event/answer/mcq')
router.register(r'event/answer/written',EventWrittenAnswerViewSet,basename='event/answer/written')
router.register(r'event/answer/polls',EventPollAnswerViewSet,basename='event/answer/polls')
router.register(r'event/ask-questions/mcq',McqAskedNotAnswwerQuestionViewSet,basename='event/ask-questions/mcq')
router.register(r'event/ask-questions/polls',PollsAskedNotAnswwerQuestionViewSet,basename='event/ask-questions/polls')
router.register(r'event/ask-questions/written',WrittenAskedNotAnswwerQuestionViewSet,basename='event/ask-questions/written')
router.register(r'event/payment_info',PaymentInfoViewSet,basename='event/payment_info')
# router.register(r'event/event-attendance', EventAttendanceViewset, basename='event/event-attendance')



urlpatterns = [
    path('api/',include(router.urls)),
    path('api/event/', EventView.as_view(), name='api-event'),
    path('api/user-event/', EventAttendView.as_view(), name='user-event'),
    path('api/event-date/', EventDate.as_view(), name='api-event-date'),
    path('api/event/event-attendent',EventAttendanceView.as_view(),name='api/event/event-attendent'),
    path('send/event-information',send_event_information,name='event_information')

    

]