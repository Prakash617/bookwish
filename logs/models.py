from django.db import models
from user_accounts.models import CustomUser

# Create your models here.
LOG = (
    ('Report','Report'),
    ('Refer','Refer'),
    ('Tip Upload','Tip Uplod'),
    ('Physical','Physical'),
    ('Relationship','Relationship'),
    ('Book Reading','Book Reading'),
    ('Meditation','Meditation'),

)
class PointLogs(models.Model):
    log_description = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add = True)
    log_type = models.CharField(max_length=100,choices=LOG)