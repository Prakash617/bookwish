from django.contrib import admin

# Register your models here.

from .models import *


class EventAdmin(admin.ModelAdmin):
     list_display = ('id','event_name', 'event_start_time', 'event_end_time', 'event_start_date', 'event_end_date', 'event_topic', 'event_location',
                    'picture', 'description', 'registration_link', 'event_location_link', 'event_type', 'is_paid', 'participant_numbers', 'event_uuid')
     search_fields = ('id','event_name', 'event_start_time', 'event_end_time', 'event_start_date', 'event_end_date', 'event_topic', 'event_location',
                    'picture', 'description', 'registration_link', ' event_location_link', 'event_type', 'is_paid', 'participant_numbers', 'event_uuid')


admin.site.register(Event, EventAdmin)


class EventViewsAdmin(admin.ModelAdmin):
     list_display = ('event', 'view_count')
     search_fields = ('event',)

admin.site.register(EventViews, EventViewsAdmin)

class EventQuestionsAdmin(admin.ModelAdmin):
     list_display = ('question', 'option1', 'option2',
                    'option3', 'option4', 'correct_answer')
     search_fields = ('question', 'option1', 'option2',
                    'option3', 'option4', 'correct_answer')
admin.site.register(EventMCQQuestions, EventQuestionsAdmin)



class EventPollsAdmin(admin.ModelAdmin):
     list_display = ('question', 'option1', 'option2',
                    'option3', 'option4')
     search_fields = ('question', 'option1', 'option2',
                    'option3', 'option4')
admin.site.register(EventPollsQuestions, EventPollsAdmin)




class EventRegistrationAdmin(admin.ModelAdmin):
     list_display = ('name', 'email', 'phone', 'location',
                    'attended', 'event', 'created_at', 'paid')
     search_fields = ('name', 'email', 'phone', 'location',
                    'attended', 'event', 'paid', 'payment_info')
admin.site.register(EventRegistration, EventRegistrationAdmin)

# ////


class EventWrittenQuestionsAdmin(admin.ModelAdmin):
     list_display = ('id', 'questions')
     search_fields = ('id', 'questions')
admin.site.register(EventWrittenQuestions, EventWrittenQuestionsAdmin)




class FeedbackAdmin(admin.ModelAdmin):
     list_display = ('id', 'event', 'feedback', 'feedback_by')
     search_fields = ('id', 'event__event_name', 'feedback_by__user__username')


admin.site.register(Feedback, FeedbackAdmin)


class EventPollAnswerAdmin(admin.ModelAdmin): 
     list_display = ('id', 'question_id','answer')
     search_fields = ('id', 'question_id','answer')


admin.site.register(EventPollAnswer, EventPollAnswerAdmin)


class EventMcqAnswerAdmin(admin.ModelAdmin): 
     list_display = ('id', 'question_id','answer','correct_answer')
     search_fields = ('id', 'question_id','answer','correct_answer')


admin.site.register(EventMcqAnswer, EventMcqAnswerAdmin)


class EventWrittenAnswerAdmin(admin.ModelAdmin): 
     list_display = ('id', 'question_id','answer')
     search_fields = ('id', 'question_id','answer')


admin.site.register(EventWrittenAnswer, EventWrittenAnswerAdmin)

admin.site.register(EventCalender)
admin.site.register(PaymentInfo)