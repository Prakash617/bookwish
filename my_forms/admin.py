from django.http import HttpResponse
import csv
from django.contrib import admin
from .models import PostEventFeedback


class PostEventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob', 'phone', 'email', 'permanent_address', 'gender', 'feedback', 'is_interested', 'expected_join_date')
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Date of Birth', 'Phone', 'Email', 'Permanent Address', 'Gender', 'Feedback', 'Interested', 'Expected Join Date'])
        for feedback in queryset:
            writer.writerow([feedback.name, feedback.dob, feedback.phone, feedback.email, feedback.permanent_address, feedback.gender, feedback.feedback, feedback.is_interested, feedback.expected_join_date])
        return response

    download_csv.short_description = "Download CSV file for selected feedback."

admin.site.register(PostEventFeedback, PostEventFeedbackAdmin)
