from dataclasses import fields
from notification.utils import day_ago
from rest_framework import serializers
from .models import *
from user_accounts.models import CustomUser
from user_accounts.serializers import CustomUserSerializer
from bookwishes import settings


class NotificationSerializer(serializers.ModelSerializer):    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['time'] = day_ago(str(instance.upload_timestamp.date()))
        # response['picture'] = settings.ip + instance.picture
        return response

    def create(self, validated_data):
        print(validated_data)
        print("user",self.context.get('request').user)

        validated_sender = validated_data.pop("sender")
        sender = self.context.get('request').user 
        
        print("validated_sender",validated_sender,type(str(validated_sender)))       
        print("sender",sender, type(str(sender)))  
        
        if str(validated_sender) ==  str(sender):
            try:
                revoker = validated_data.pop("revoker")
            except:
                revoker = None
            notification = Notification.objects.create(sender=sender, revoker=revoker, **validated_data)        
            return notification
        raise serializers.ValidationError("human readable error message here")

    class Meta:
        model = Notification
        fields = ('id', 'sender', 'revoker', 'status', 'notification_type', 'title', 'picture', 'description')
        read_only_fields = ('id',) 


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = '__all__'