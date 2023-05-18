from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from django.apps import apps

class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        # Get a list of all the models in your app
        models = apps.get_models()
        # Add a search bar for each model
        search_fields = {model._meta.model_name: ['__all__'] for model in models}
        context['search_fields'] = search_fields
        return context
    

class HelpSupportAdmin(SummernoteModelAdmin):
    summernote_fields = ('answer',)

class AppDataAdmin(SummernoteModelAdmin):
    summernote_fields = ('privacy_policy', 'physical_badge_info', 'mental_badge_info', 'emotional_badge_info', 'spiritual_badge_info', 'beginner_info')

# Register your models here.
# admin.site.register(Club)
# admin.site.register(Refer)
# admin.site.register(Badge)
# admin.site.register(HelpSupport, HelpSupportAdmin)
# admin.site.register(AppData, AppDataAdmin)

# admin.site.register(DailyStepCount)
# admin.site.register(DigitalWellbeing)
# admin.site.register(BookReading)
# admin.site.register(Health)
# admin.site.register(PersonalFitness)
# admin.site.register(PersonalAchievement)
# admin.site.register(Relationship)
# admin.site.register(Meditation)
# admin.site.register([ReportCategory,PostReport,StoryReport,CommentReport])

# admin.site.register(Feedback)
# admin.site.register([ReportCategory,PostReport,StoryReport])

class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_id','club_name' , 'club_owner','date_join')
    search_fields = ["club_id","club_name","club_owner__username"]
admin.site.register(Club, ClubAdmin)

class ReferAdmin(admin.ModelAdmin):
     list_display = ('referred_by','generated_for','refer_code','onboarded_user')
     search_fields = ('referred_by__username','generated_for','refer_code','onboarded_user__username')
admin.site.register(Refer, ReferAdmin)

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('badgeName','badgeLevel','badgeIcon')
    search_fields = ('badgeName','badgeLevel','badgeIcon')
admin.site.register(Badge, BadgeAdmin)

class HelpSupportAdmin(admin.ModelAdmin):
     list_display = ('question','answer')
admin.site.register(HelpSupport, HelpSupportAdmin)

class AppDataAdmin(admin.ModelAdmin):
     list_display = ('privacy_policy','mental_badge_info','emotional_badge_info','spiritual_badge_info','beginner_info')
admin.site.register(AppData, AppDataAdmin)

class DailyStepCountAdmin(admin.ModelAdmin):
     list_display = ('userid','record_date','start_time','end_time','duration','distance','calorie')
     search_fields = ('userid__username','record_date','start_time','end_time','duration','distance','calorie')
admin.site.register(DailyStepCount, DailyStepCountAdmin)

class DigitalWellbeingAdmin(admin.ModelAdmin):
     list_display = ('userid','record_date','total_usage','unlocks','top_1','top_2','top_3')
     search_fields = ('userid__username','record_date','total_usage','unlocks','top_1','top_2','top_3')
admin.site.register(DigitalWellbeing, DigitalWellbeingAdmin)

class BookReadingAdmin(admin.ModelAdmin):
     list_display = ('userid','record_date','start_page','end_page','reading_time','book_name')
     search_fields = ('userid__username','record_date','start_page','end_page','reading_time','book_name')
admin.site.register(BookReading, BookReadingAdmin)

class HealthAdmin(admin.ModelAdmin):
     list_display = ('userid','day','date','time','weight','height_ft','height_in','waist','hipsize','bellysize','bmi_val')
     search_fields = ('userid__username','day','date','time','weight','height_ft','height_in','waist','hipsize','bellysize','bmi_val')

admin.site.register(Health, HealthAdmin)

class PersonalAchievementAdmin(admin.ModelAdmin):
     list_display = ('userid','target_set_date','daily_step_target','daily_socialmedia_target','daily_bookpages_target')
     search_fields = ('userid__username','target_set_date','daily_step_target','daily_socialmedia_target','daily_bookpages_target')

admin.site.register(PersonalAchievement, PersonalAchievementAdmin)


class RelationshipAdmin(admin.ModelAdmin):
     list_display = ('userid','plus_points','neg_points','record_date')
     search_fields = ('userid__username','record_date')
admin.site.register(Relationship, RelationshipAdmin)

class MeditationAdmin(admin.ModelAdmin):
     list_display = ('userid','time_mins','record_date')
     search_fields = ('userid__username','record_date')
admin.site.register(Meditation, MeditationAdmin)

class FeedbackAdmin(admin.ModelAdmin):
     list_display = ('feedback_by','feedback')
     search_fields = ('feedback_by__username','feedback')
admin.site.register(Feedback, FeedbackAdmin)

class ReportCategoryAdmin(admin.ModelAdmin):
     list_display = ('name','descriptions')
     search_fields = ('name',)
admin.site.register(ReportCategory, ReportCategoryAdmin)

class PostReportAdmin(admin.ModelAdmin):
     list_display = ('reported_by','report_category','post')
     search_fields = ('reported_by__username','report_category__name')
admin.site.register(PostReport, PostReportAdmin)


class StoryReportAdmin(admin.ModelAdmin):
     list_display = ('reported_by','report_category','story')
     search_fields = ('reported_by__username','report_category__name')
admin.site.register(StoryReport, StoryReportAdmin)

class CommentReportAdmin(admin.ModelAdmin):
     list_display = ('reported_by','report_category','comment')
     search_fields = ('reported_by__username','report_category__name')
admin.site.register(CommentReport, CommentReportAdmin)

















