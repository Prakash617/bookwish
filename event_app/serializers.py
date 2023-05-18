from rest_framework import serializers
from .models import *
from user_accounts.models import CustomUser
from user_accounts.serializers import CustomUserSerializer
import datetime
import random


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ('id','club')

    def create(self, validated_data):
        return Event.objects.create(**validated_data)


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = ['id','user','created_at', 'payment_type', 'details', 'remarks']
        read_only_fields = ['id', 'created_at','user']

    def create(self, validated_data):
        return PaymentInfo.objects.create(**validated_data)


class EventRegistrationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EventRegistration
        fields = "__all__"
        read_only_fields = ('id',) 


class EventAttendenceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EventRegistration
        fields = ("email","event")
        read_only_fields = ('id','name','user','phone','location','attended','paid','payment_info','dob','gender','created_at') 


class EventMCQQuestionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EventMCQQuestions
        fields = "__all__"
        read_only_fields = ('id',) 

class EventWrittenQuestionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EventWrittenQuestions
        fields = "__all__"
        read_only_fields = ('id',) 

class EventPollsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EventPollsQuestions
        fields = "__all__"
        read_only_fields = ('id',) 


# class QuestionsSerializer(serializers.ModelSerializer):    
#     written_id = EventWrittenQuestionSerializer(read_only=True)
#     mcq_id = EventMCQQuestionSerializer(read_only=True )
#     poll_id = EventPollsSerializer(read_only=True)
#     class Meta:
#         model = Questions
#         fields = "__all__"
#         read_only_fields = ('id',)
         
class FeedbackSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ('id',) 


class EventMcqAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMcqAnswer
        fields = "__all__"
        read_only_fields = ('id',) 

class EventPollAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPollAnswer
        fields = "__all__"
        read_only_fields = ('id',) 

class EventWrittenAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWrittenAnswer
        fields = "__all__"
        read_only_fields = ('id',) 