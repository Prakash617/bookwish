from dataclasses import fields
from points_and_badges.utils import update_book_reading_points, update_meditation_points, update_physical_points
from rest_framework import serializers
from .models import *
from user_accounts.models import CustomUser
from user_accounts.serializers import CustomUserSerializer
import datetime
import random
from user_accounts.utils import send_refer_code


class ClubSerializer2(serializers.ModelSerializer):    
    # club_owner = CustomUserSerializer(many=False)

    def create(self, validated_data):
        # club_owner = validated_data.pop("club_owner")
        club = Club.objects.create(**validated_data)        
        # CustomUser.objects.create(user = club_owner)
        return club

    class Meta: 
        model = Club
        fields = ('club_id', 'club_name')
        read_only_fields = ('club_id', )
        


class ReferSerializer(serializers.ModelSerializer):    
    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['referred_by'] = CustomUserSerializer(instance.referred_by,context={"request":request}).data
        response['onboarded_user'] = CustomUserSerializer(instance.onboarded_user,context={"request":request}).data
        return response

    def create(self, validated_data):
        referred_by = self.context.get('request').user
        
        onboarded_user = None
        refer_code = "BW" + str(random.randint(100011, 999999))
        
        refer = Refer.objects.create(referred_by=referred_by, onboarded_user=onboarded_user, refer_code=refer_code, **validated_data)
        print(validated_data["generated_for"])
        send_refer_code(refer_code, validated_data["generated_for"])
        return refer

    class Meta:
        model = Refer
        fields = ('id', 'referred_by', 'generated_for', 'refer_code', 'onboarded_user')
        read_only_fields = ('id', 'refer_code', )


class BadgeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Badge
        fields = ("badgeName", "badgeLevel", "badgeIcon")


class HelpSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpSupport
        fields = ("question", "answer")


class AppDataSerializer(serializers.ModelSerializer):    
    class Meta:
        model = AppData
        fields = ("privacy_policy", "physical_badge_info", "mental_badge_info", "beginner_info", "spiritual_badge_info", "emotional_badge_info")


class DailyStepCountSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        response["day"] = instance.record_date.strftime('%A')
        return response

    def create(self, validated_data):

        # recording the stepcount data for a day of a user
        userid = validated_data.pop("userid")
        dailystepcount = DailyStepCount.objects.create(userid=userid, **validated_data)
        
        # updating the points and levels table of the user 
        # using the utils from 'points_and_badges' app to update it.
        time = validated_data['duration']/60
        print(validated_data['duration'])
        print("function call, time=", time)
        update_physical_points(time,userid.id)        
        return dailystepcount

    def get_steps(self, obj):
        steps = obj.distance * 1500          # average stride length is 5 feet
        return steps

    class Meta:
        model = DailyStepCount
        fields = ("userid", "record_date", "start_time", "end_time", "duration", "distance", "calorie", "steps")


class DigitalWellbeingSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        return response

    def create(self, validated_data):
        userid = validated_data.pop("userid")
        digitalwellbeing = DigitalWellbeing.objects.create(userid=userid, **validated_data)        
        return digitalwellbeing

    class Meta:
        model = DigitalWellbeing
        fields = ("userid", "record_date", "unlocks", "total_usage", "top_1", "top_2", "top_3")


class BookReadingSerializer(serializers.ModelSerializer):
    # userid = CustomUserSerializer(many=False)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        response['day'] = instance.record_date.strftime('%A')
        response['pages'] =  instance.end_page - instance.start_page
        return response

    def create(self, validated_data):
        print("at pop garne thau")
        userid = validated_data.pop("userid")

        # recording the book reading data of the person for the day
        bookreading = BookReading.objects.create(userid=userid, **validated_data)
        
        # updating the data into the points table of the user
        # this updates happen from the utils of the 'points_and_badges' app
        update_book_reading_points(validated_data['start_page'], validated_data['end_page'], userid.id)

        return bookreading

    class Meta:
        model = BookReading
        fields = ("userid", "record_date", "start_page", "end_page", "reading_time", "book_name")
        # fields= '__all__'
        


class HealthSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        return response

    def create(self, validated_data):
        userid = validated_data.pop("userid")

        
        # try:
        #     bmi = Health.objects.filter(userid=userid).get(date=datetime.datetime.now().strftime("%Y-%m-%d"))
        #     for attr, value in validated_data.items():
        #         setattr(bmi, attr, value)
        #     bmi.save()            
        # except:
        bmi = Health.objects.create(userid=userid, **validated_data)        
        return bmi

    class Meta:
        model = Health
        fields = ("userid", "day", "date", "time", "weight", "height_ft","height_in", "waist", "hipsize", "bellysize","bmi_val")




# class PersonalFitnessSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['userid'] = CustomUserSerializer(instance.userid).data
#         return response

#     def create(self, validated_data):
#         userid = validated_data.pop("userid")
#         personalfitness = PersonalFitness.objects.create(**validated_data)        
#         return personalfitness

#     class Meta:
#         model = PersonalFitness
#         fields = ("userid", "bmi_val", "start_time", "weight", "target_date")


class PersonalAchievementSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):  
        response = super().to_representation(instance)
        response['userid'] = CustomUserSerializer(instance.userid).data
        return response

    def create(self, validated_data):
        userid = validated_data.pop("userid")
        personal_achievement = PersonalAchievement.objects.create(userid=userid, **validated_data)        
        return personal_achievement

    class Meta:
        model = PersonalAchievement
        fields = ("userid", "target_set_date", "daily_step_target", "daily_socialmedia_target", "daily_bookpages_target")

class RelationshipSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        response['day'] = instance.record_date.strftime('%A')
        return response

    class Meta:
        model = Relationship
        fields = ("userid", "plus_points", "neg_points", "record_date")
        
    
    

class RelationshipUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    increment = serializers.BooleanField()
    decrement = serializers.BooleanField()
    record_date = serializers.DateField()

class MeditationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['userid'] = CustomUserSerializer(instance.userid).data
        response['day'] = instance.record_date.strftime('%A')
        # response['time_mins'] = round(instance.time_mins/60,2)
        return response
    
    def create(self, validated_data):

        # recording today's data of the user of meditation tool
        userid = validated_data.pop("userid")        
        try:
            meditation = Meditation.objects.filter(userid=userid).get(record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            meditation.time_mins = validated_data.pop("time_mins")    
            meditation.save()
            return meditation
        except:
            meditation = Meditation.objects.create(userid=userid, **validated_data) 

        # updating the data into the meditaion time table
        # using the update_meditation_points utils of 'points_and_badges' table to update the points

        update_meditation_points(validated_data['time_mins'], userid.id)       
        return meditation

    class Meta:
        model = Meditation
        fields = ("userid", "time_mins", "record_date")
        
class ReportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCategory
        fields = "__all__"

class PostReportSerializer(serializers.ModelSerializer):
    report_category = ReportCategorySerializer(many = False,read_only=True)
    
    class Meta:
        model = PostReport
        fields = ('id','reported_by','post','report_category',)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
        
class StoryReportSerializer(serializers.ModelSerializer):
    report_category = ReportCategorySerializer(many = False,read_only=True)
    
    class Meta:
        model = StoryReport
        fields = ('id','reported_by','story','report_category',)
class CommentReportSerializer(serializers.ModelSerializer):
    report_category = ReportCategorySerializer(many = False,read_only=True)
    
    class Meta:
        model = CommentReport
        fields = "__all__"
        # fields = ('id','reported_by','story','report_category',)
