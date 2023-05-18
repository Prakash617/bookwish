from django.db import models

class PostEventFeedback(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=255)
    dob = models.DateField()
    phone = models.CharField(max_length=99)
    email = models.EmailField()
    permanent_address = models.CharField(max_length=99)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    feedback = models.TextField()
    is_interested = models.BooleanField(default=False)
    expected_join_date = models.DateField(null=True, blank=True)



