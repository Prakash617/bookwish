from django.db import models
from user_accounts.models import CustomUser
# Create your models here.

class Assesment(models.Model):
    posted_date = models.DateField(auto_now_add=True)
    posted_time = models.TimeField(auto_now_add=True)    
    media = models.URLField()
    description = models.CharField(max_length=999)
    views_count = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class AssesmentCriteria(models.Model):
    criteria_name = models.CharField(max_length=99)

    def __str__(self):
        return self.criteria_name

def default_score_json():
    return {"score_data":[]}

class AssessmentScores(models.Model):
    assessed_by = models.ForeignKey(CustomUser, related_name="assessed_by_user", on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assesment, related_name="assessment_object", on_delete=models.CASCADE)
    scores = models.JSONField(default=default_score_json)