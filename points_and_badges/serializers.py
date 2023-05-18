from rest_framework import serializers
from .models import *
from user_accounts.models import CustomUser


# class WeeklyBookReadingPointTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyBookReadingPointTable
#         fields = '__all__'

# class WeeklyMedidationPointTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyMeditationPointTable
#         fields = '__all__'

# class WeeklyPhysicalPointTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyPhysicalPointTable
#         fields = '__all__'

# class WeeklyRelationshipPointTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyRelationshipPointTable
#         fields = '__all__'


class CombineWeeklyPointsSerializer(serializers.Serializer):
    user = serializers.CharField()
    date = serializers.DateField()
    level = serializers.IntegerField()



class CombineDailyPointsSerializer(serializers.Serializer):
    user = serializers.CharField()
    date = serializers.DateField()
    level = serializers.IntegerField()
