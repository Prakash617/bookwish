from django.contrib import admin

# Register your models here.
from .models import (
    Assesment,
    AssessmentScores,
    AssesmentCriteria,
)



admin.site.register(AssesmentCriteria)

class AssesmentAdmin(admin.ModelAdmin):
    list_display = ('posted_date','posted_time','media','description','views_count','user')

admin.site.register(Assesment, AssesmentAdmin)

class AssessmentScoresAdmin(admin.ModelAdmin):
    list_display = ('assessed_by','assessment','scores')

admin.site.register(AssessmentScores, AssessmentScoresAdmin)
