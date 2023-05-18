from django.db import models

STATUS_CHOICES = (
    ("unread", "unread"),
    ("read", "read")

)

NOTIFICATIONS_CHOICES = (
    ("general", "general"),
    ("rating", "rating"),
    ("comment", "comment")

)

class Notification(models.Model):
    sender = models.ForeignKey("user_accounts.CustomUser", null=True, blank=True, on_delete=models.CASCADE, related_name="notification_sender") 
    revoker = models.ForeignKey("user_accounts.CustomUser", null=True, blank=True, on_delete=models.CASCADE, related_name="notification_revoker") 
    status = models.CharField(max_length=100,choices = STATUS_CHOICES, default = 'unread')
    picture = models.ImageField(max_length=400,upload_to = 'customuser/', blank=True, default="customuser/bell.png")
    notification_type = models.CharField(max_length=100,choices=NOTIFICATIONS_CHOICES, default='general' ) 
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    upload_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null= True)

    def __str__(self):
        return self.description + " " +str(self.upload_timestamp)

class AdminNotification(models.Model):
    status = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=100 )  
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.title

class NotificationTemplate(models.Model):
    name= models.CharField(max_length=20)
    template = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# from django.db import models

# Create your models here.
# class Notification(models.Model):
#     sender = models.ForeignKey("user_accounts.CustomUser", null=True, blank=True, on_delete=models.CASCADE, related_name="notification_sender") 
#     revoker = models.ForeignKey("user_accounts.CustomUser", null=True, blank=True, on_delete=models.CASCADE, related_name="notification_revoker") 
#     status = models.CharField(max_length=100)
#     notification_type = models.CharField(max_length=100)        # INDIVIDUAL, ALL
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=1000)