from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView,ListAPIView
from rest_framework.response import Response
import datetime
import random
from  rest_framework.viewsets import ModelViewSet
from rest_framework import status
from event_app.utils import send_mail_event_information


from .models import *
from .serializers import *

# Create your views here.

class EventDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    lookup_field = "id"

 

class EventView(ListCreateAPIView):
    
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        club = self.request.user.club
        serializer.save(club=club)
    
    def get_queryset(self):
       queryset = Event.objects.filter(club=self.request.user.club).order_by('-event_start_date')
       return queryset

class PaymentInfoViewSet(ModelViewSet):
    queryset = PaymentInfo.objects.all()
    serializer_class = PaymentInfoSerializer

    def perform_create(self, serializer):
        print(self.request.user.club)
        serializer.save(user=self.request.user)

class EventRegistrationView(ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    
    def get (self, request, id=None):
        registrations = self.queryset.filter(event=id)
        serializer = EventRegistrationSerializer(registrations, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        event_id = request.data.get('event')

        if EventRegistration.objects.filter(email=email, event=event_id).exists():
            return Response({'message': 'Email already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class EventAttendanceView(APIView):
    
    def post(self, request, *args, **kwargs):
            email = request.data.get('email')
            event_id = request.data.get('event')

            try:
                event = Event.objects.get(event_uuid=event_id)
            except:
                return Response({"status": "Event Not Found"})

            
            registration = get_object_or_404(EventRegistration, email=email, event=event)
            if registration:
                registration.attended = True
                registration.save()
                return Response({'status': 'success'})
            else:
                return Response({'status': 'error'})


# class EventMCQQuestionDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = EventMCQQuestions.objects.all()
#     serializer_class = EventMCQQuestionSerializer
#     lookup_field = "id"

# class EventMCQQuestionView(ListCreateAPIView):
#     queryset = EventMCQQuestions.objects.all()
#     serializer_class = EventMCQQuestionSerializer

#     def get (self, request, id=None):

#         questions = self.queryset.filter(event=id)
        
#         serializer = EventMCQQuestionSerializer(questions, many=True, context={'request': request})
#         return Response(serializer.data)



# class EventWrittenQuestionDetailView(ModelViewSet):
#     queryset = EventWrittenQuestions.objects.all()
#     serializer_class = EventMCQQuestionSerializer
#     lookup_field = "id"


class MCQQuestionViewSet(ModelViewSet):
    queryset = EventMCQQuestions.objects.all()
    serializer_class = EventMCQQuestionSerializer

class WrittenQuestionViewSet(ModelViewSet):
    queryset = EventWrittenQuestions.objects.all()
    serializer_class = EventWrittenQuestionSerializer

class PollQuestionViewSet(ModelViewSet):
    queryset = EventPollsQuestions.objects.all()
    serializer_class = EventPollsSerializer


# class QuestionViewSet(ModelViewSet):
#     queryset = Questions.objects.all()
#     serializer_class = QuestionsSerializer
#     lookup_field = "id"

#     def list(self, request, id=None,*args,**kwargs):
#         event_id = request.query_params.get('id')
#         print(event_id)
#         try:
#             event = Event.objects.get(id = event_id)
#         except:
#             return Response('no event found')
        
#         questions = self.queryset.filter(event=event.id)
#         print(questions)
        
#         serializer = self.serializer_class(questions, many=True)
#         return Response(serializer.data)

# class AskQuestions(ModelViewSet):
#     queryset = Questions.objects.all()
#     serializer_class = QuestionsSerializer
#     lookup_field = "id"
    
#     def list(self, request):
#         event_id = request.query_params.get('id')
#         try:
#             event = Event.objects.get(id = event_id)
#         except:
#             return Response('no event found')
        
#         questions = self.queryset.filter(event=event.id,ask_question = True)
        
#         serializer = self.serializer_class(questions, many=True, context={'request': request})
#         return Response(serializer.data)
    
# class NotAskQuestions(ModelViewSet):
#     queryset = Questions.objects.all()
#     serializer_class = QuestionsSerializer
#     lookup_field = "id"
    
#     def list(self, request):
#         event_id = request.query_params.get('id')
#         try:
#             event = Event.objects.get(id = event_id)
#         except:
#             return Response('no event found')
        
#         questions = self.queryset.filter(event=event.id,ask_question = False)
        
#         serializer = self.serializer_class(questions, many=True, context={'request': request})
#         return Response(serializer.data)
    
# class FeedBackViewSet(ModelViewSet):
#     queryset = Questions.objects.all()
#     serializer_class = QuestionsSerializer
#     lookup_field = "id"

class EventWrittenAnswerViewSet(ModelViewSet):
    queryset = EventWrittenAnswer.objects.all()
    serializer_class = EventWrittenAnswerSerializer


class EventMcqAnswerViewSet(ModelViewSet):
    queryset = EventMcqAnswer.objects.all()
    serializer_class = EventMcqAnswerSerializer

class EventPollAnswerViewSet(ModelViewSet):
    queryset = EventPollAnswer.objects.all()
    serializer_class = EventPollAnswerSerializer

class McqAskedNotAnswwerQuestionViewSet(ModelViewSet):
    serializer_class = EventMCQQuestionSerializer

    def get_queryset(self):
        event = self.request.query_params.get('event')
        current_event = Event.objects.get(id=event)

        questions = []
        if EventRegistration.objects.filter(user=self.request.user, attended=True).exists():    
            for item in EventMCQQuestions.objects.filter(event=current_event):
                if not EventMcqAnswer.objects.filter(user=self.request.user, question_id=item).exists():
                    try:
                        questions.append(EventMCQQuestions.objects.get(id=item.id, asked=True))
                    except:
                        pass
            
            return questions
        
        return EventMCQQuestions.objects.none()
    
class PollsAskedNotAnswwerQuestionViewSet(ModelViewSet):
    serializer_class = EventPollsSerializer

    def get_queryset(self):
        event = self.request.query_params.get('event_uuid')
        current_event = Event.objects.get(id=event)

        questions = []
        if EventRegistration.objects.filter(user=self.request.user, attended=True).exists():    
            for item in EventPollsQuestions.objects.filter(event=current_event):
                if not EventPollAnswer.objects.filter(user=self.request.user, question_id=item).exists():
                    try:
                        questions.append(EventPollsQuestions.objects.get(id=item.id, asked=True))
                    except:
                        pass
            
            return questions
        
        return EventMCQQuestions.objects.none()

class WrittenAskedNotAnswwerQuestionViewSet(ModelViewSet):
    serializer_class = EventWrittenQuestionSerializer

    def get_queryset(self):
        event = self.request.query_params.get('event_uuid')
        current_event = Event.objects.get(id=event)

        questions = []
        if EventRegistration.objects.filter(user=self.request.user, attended=True).exists():    
            for item in EventWrittenQuestions.objects.filter(event=current_event):
                if not EventWrittenAnswer.objects.filter(user=self.request.user, question_id=item).exists():
                    try:
                        questions.append(EventWrittenQuestions.objects.get(id=item.id, asked=True))
                    except:
                        pass
            
            return questions
        
        return EventWrittenQuestions.objects.none()





from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from rest_framework.generics import ListAPIView
from .models import Event
from .serializers import EventSerializer
from collections import defaultdict
from django.http import HttpResponse



class EventDate(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        event_name = self.request.GET.get('event_name')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        location = self.request.GET.get('location')
        location_link = self.request.GET.get('location_link')
        date = {}
        
        events = Event.objects.all()
        
        if event_name is not None:
            events = events.filter(event_name=event_name)

        if start_date is not None and end_date is not None:
            events = events.filter(event_start_date__range=(start_date, end_date))
        
        if location is not None:
            events = events.filter(event_location=location)
        
        if location_link is not None:
            events = events.filter(event_location_link=location_link)

        # data = list(events.values('id', 'event_name', 'event_start_date', 'event_end_date', 'event_location', 'event_location_link'))
        # return Response(data)
        return events
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = defaultdict(list)
        
        for event in queryset:
            event_data = self.get_serializer(event).data
            event_date = event.event_start_date.strftime('%Y-%m-%d')
            data[event_date].append(event_data)
        
        return Response(data)



class EventAttendView(ListAPIView):
    serializer_class = EventSerializer 
    def get_queryset(self):
        event = []

        if EventRegistration.objects.filter(user=self.request.user, attended=True).exists():
            for item in EventRegistration.objects.filter(user=self.request.user, attended=True):
                # try:
                event.append(item.event)
                # except:
                    # pass
            return event
        return Event.objects.none()


def send_event_information(request):
    events = Event.objects.all()
    users = EventRegistration.objects.all()
    context = {}
    for event in events:
            event_date = datetime.datetime.today() - datetime.timedelta(days=1)
            print("1")
            print(event_date.date())
            print(event.event_start_date)
            if event.event_start_date == event_date.date():
                event_user = users.filter(event=event)
                context['data'] = event
                print("2")
                for user in event_user:
                    email = user.email
                    print("3")
                    send_mail_event_information(email,context)

    return HttpResponse('Emails sent')