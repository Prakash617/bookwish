from django.db import models
from django.contrib.auth.models import AbstractUser
from club.models import Club

# for pasword reset
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


Gender_Status =(
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
)


# Create your models here.
class CustomUser(AbstractUser):    
    picture = models.ImageField(max_length=400,upload_to = 'customuser/', blank=True, default="customuser/default_profile.jpg")
    country_code = models.CharField(max_length=4)
    phone = models.CharField(max_length=10)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=100, choices=Gender_Status, default="Male", null=True)
    location = models.CharField(max_length=1000, null=True)
    verify_token = models.CharField(max_length=100)
    email_verified = models.BooleanField(default=False)
    
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, null=True)
    points = models.FloatField(default=0.0)
    physical_badge = models.IntegerField(default=0)
    mental_badge = models.IntegerField(default=0)
    emotional_badge = models.IntegerField(default=0)
    spiritual_badge = models.IntegerField(default=0)
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class ActiveUser(models.Model):
    activeUser = models.OneToOneField(CustomUser,on_delete=models.CASCADE,)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.activeUser.username



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )