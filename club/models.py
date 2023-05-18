from datetime import datetime
from enum import unique
from django.db import models

from feed.models import Post

# Create your models here.
class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=200,unique=True)
    club_owner = models.OneToOneField("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="club_owner", null=True)
   
    date_join = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return self.club_name

class Refer(models.Model):
    referred_by = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="referred_by", null=True, blank=True)
    generated_for = models.CharField(max_length=500, unique=True)
    refer_code = models.CharField(max_length=9,unique=True)
    onboarded_user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="onboarded_user", null=True, blank=True)

    def __str__(self):
        return self.refer_code

class Badge(models.Model):
    badgeName = models.CharField(max_length=200)
    badgeLevel = models.IntegerField()
    badgeIcon = models.CharField(max_length=200)
    
# #############################################
# ############  Basic AppData  ################
# #############################################

class HelpSupport(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=500)

class AppData(models.Model):
    privacy_policy = models.TextField()
    physical_badge_info = models.TextField(max_length=500)
    mental_badge_info = models.TextField(max_length=500)
    emotional_badge_info = models.TextField(max_length=500)
    spiritual_badge_info = models.TextField(max_length=500)
    beginner_info = models.TextField(max_length=500)


# #############################################
# #########  User-specific Data  ##############
# #############################################


class DailyStepCount(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="daily_step_userid") 
    # 561115
    # set record date to true
    record_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField()
    distance = models.FloatField(default= 0)
    calorie = models.FloatField()
    
    def __str__(self):
        return str(self.userid) +'--'+ str(self.distance) +'--'+ str(self.userid.club)
    

class DigitalWellbeing(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="digital_wellbeing_userid")
    record_date = models.DateField()
    total_usage = models.IntegerField()
    unlocks = models.IntegerField()
    top_1 = models.CharField(max_length=100)
    top_2 = models.CharField(max_length=100)
    top_3 = models.CharField(max_length=100)

class BookReading(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="book_reading_userid") 
    record_date = models.DateField(auto_now_add=True)
    start_page = models.IntegerField()
    end_page = models.IntegerField()
    reading_time = models.IntegerField()
    book_name = models.CharField(max_length=200)

    def page(self):
        pages = self.start_page - self.end_page
        return pages
    
    def __str__(self):
        return str(self.userid) +'--'+ str(self.book_name)

class Health(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="bmi_userid") 
    day = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    weight = models.FloatField()
    height_ft = models.FloatField()
    height_in = models.FloatField()
    waist = models.FloatField()
    hipsize = models.FloatField()
    bellysize = models.FloatField()
    bmi_val = models.FloatField()
    record_date = models.DateField(auto_now_add=True,blank=True,null=True)
    

# class PersonalFitness(models.Model):
#     # userid = models.ForeignKey(CustomUser) 
#     bmi_val = models.FloatField()
#     weight = models.FloatField()
#     target_date = models.DateField()

class PersonalAchievement(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="personal_achievement_userid")
    target_set_date = models.DateField()
    daily_step_target = models.IntegerField()
    daily_socialmedia_target = models.IntegerField()
    daily_bookpages_target = models.IntegerField()

class Relationship(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="relationship_userid") 
    plus_points = models.IntegerField(default=0)
    neg_points = models.IntegerField(default=0)
    record_date = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.userid) + '--' + str(self.record_date)
    

class Meditation(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, related_name="meditation_userid") 
    time_mins = models.FloatField()
    record_date = models.DateField(auto_now_add=True, null=True)

class ReportCategory(models.Model):
    name = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=300,null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class PostReport(models.Model):
    reported_by = models.ForeignKey("user_accounts.CustomUser",on_delete=models.CASCADE, related_name='report_user')
    report_category = models.ForeignKey("ReportCategory",on_delete=models.CASCADE, related_name='report_category')
    post = models.ForeignKey("feed.Post",on_delete=models.CASCADE, related_name='reported_post')
    
    def __str__(self):
        return str(self.post)



class Feedback(models.Model):
    feedback_by = models.ForeignKey("user_accounts.CustomUser",on_delete=models.CASCADE, related_name='feedback_user')
    feedback = models.CharField(max_length=999)
    # attachment = models.ImageField(upload_to='media/feedback', null=True, blank=True)
    
class StoryReport(models.Model):
    reported_by = models.ForeignKey("user_accounts.CustomUser",on_delete=models.CASCADE, related_name='story_user')
    report_category = models.ForeignKey(ReportCategory,on_delete=models.CASCADE, related_name='story_report_category')
    story = models.ForeignKey("feed.Story",on_delete=models.CASCADE, related_name='reported_story')

    def __str__(self):
        return str(self.story)
    
class CommentReport(models.Model):
    reported_by = models.ForeignKey("user_accounts.CustomUser",on_delete=models.CASCADE, related_name='comment_user')
    report_category = models.ForeignKey("ReportCategory",on_delete=models.CASCADE, related_name='comment_report_category')
    comment = models.ForeignKey("feed.Comment",on_delete=models.CASCADE, related_name='reported_comment')

    def __str__(self):
        return str(self.comment)
    

