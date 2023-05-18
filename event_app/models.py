from django.utils import timezone
from django.db import models

# Create your models here.
from django.db import models
import uuid
from user_accounts.models import CustomUser
# Create your models here.




import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bookwishes.settings import ip 
from club.models import Club


class Event(models.Model):
    event_name = models.CharField(max_length=999,)
    club = models.ForeignKey(Club,on_delete=models.CASCADE,null=True,blank=True)
    event_start_time = models.TimeField()
    event_end_time = models.TimeField()
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_topic = models.CharField(max_length=999,blank=True)
    event_location = models.CharField(max_length=999,)
    picture = models.ImageField(upload_to='event/', blank=True)
    description = models.CharField(max_length=999,)
    registration_link = models.CharField(blank=True, max_length=200)
    event_location_link = models.URLField(blank=True)
    event_type = models.CharField(max_length=999,blank=True)
    is_paid = models.BooleanField(default='False')
    participant_numbers = models.IntegerField(default=0,blank=True, null=True)
    event_uuid = models.UUIDField(unique=True,default=uuid.uuid4)
    attendance_link = models.URLField(blank=True)
    attendance_qr = models.ImageField(null=True, blank=True)
    price = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.event_name) + '-'+ str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.registration_link:
            self.registration_link = f'{ip}event/registrations/?event={self.event_uuid}'

        if not self.attendance_link:
            self.attendance_link = f'{ip}event/attendance/?event={self.event_uuid}'

        # generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.attendance_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # save QR code image to ImageField
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        qr_image = ContentFile(buffer.getvalue())
        self.attendance_qr.save(f'qrcode_{self.attendance_link}.jpg', qr_image, save=False)

        super().save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
        # Convert date objects to strings in the correct format
        # self.event_start_date = self.event_start_date.strftime('%Y-%m-%d')
        # self.event_end_date = self.event_end_date.strftime('%Y-%m-%d')
        # super(Event, self).save(*args, **kwargs)

    
class EventViews(models.Model):
    event = models.ForeignKey(Event, related_name='event_views' ,on_delete = models.CASCADE)
    view_count = models.IntegerField()

    def __str__(self):
        return str(self.event)



class EventMCQQuestions(models.Model):
    question = models.CharField(max_length=999,null=True,blank=True)
    option1 = models.CharField(max_length=999,null=True,blank=True)
    option2 = models.CharField(max_length=999,null=True,blank=True)
    option3 = models.CharField(max_length=999,null=True,blank=True)
    option4 = models.CharField(max_length=999,null=True,blank=True)
    correct_answer = models.CharField(max_length=999,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='event_mcq' ,on_delete = models.CASCADE, null=True, blank=True)
    asked = models.BooleanField(default=False)
    modified_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.asked:
            self.modified_date = timezone.now()
        super().save(*args, **kwargs)

    
    def __str__(self):
        return str(self.id) + str(self.question)
    
class EventPollsQuestions(models.Model):
    question = models.CharField(max_length=999,null=True,blank=True)
    option1 = models.CharField(max_length=999,null=True,blank=True)
    option2 = models.CharField(max_length=999,null=True,blank=True)
    option3 = models.CharField(max_length=999,null=True,blank=True)
    option4 = models.CharField(max_length=999,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='event_polls' ,on_delete = models.CASCADE, null=True, blank=True)
    asked = models.BooleanField(default=False)
    modified_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.asked:
            self.modified_date = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id) + str(self.question)
    
class EventWrittenQuestions(models.Model):
    questions = models.CharField(max_length=999)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='event_written' ,on_delete = models.CASCADE, null=True, blank=True)
    asked = models.BooleanField(default=False)
    modified_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.asked:
            self.modified_date = timezone.now()
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.id) +"-"+ str(self.questions)  
    

    
PAYMENT_TYPE = (('Esewa','Esewa'),('FonePay','Fonepay'),('Bank','Bank'))


def data():
  return {"empty": "empty"}
  


class PaymentInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=9999,choices=PAYMENT_TYPE,default="ESEWA")  
    details = models.JSONField(default=data,null=True,blank=True)
    remarks = models.JSONField(default=data,null=True,blank=True)

    
    
    

class EventRegistration(models.Model):
    user = models.ForeignKey(CustomUser,related_name='event_registration',on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=999)
    email = models.EmailField()
    phone = models.CharField(max_length=999)
    location = models.CharField(max_length=999)
    attended = models.BooleanField(default=False,blank=True)
    event = models.ForeignKey(Event, related_name='Event_registration' ,on_delete = models.CASCADE)
    paid = models.BooleanField(default=False, blank=True)
    payment_info = models.ForeignKey(PaymentInfo,on_delete=models.CASCADE,null=True,blank=True)
    # payment_info =models.JSONField(null=True,blank=True)
    dob = models.DateField(null=True)
    GENDER = (('male','male'),('female','female'),('other','other'))
    gender = models.CharField(max_length=10, choices=GENDER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name) + str(self.id)
    


    
class EventSummary(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE,related_name="event_summary")
    total_questions = models.IntegerField()
    total_answers = models.IntegerField()
    total_participates = models.IntegerField()
    total_feedbacks = models.IntegerField()
    event_durations = models.TimeField()


    def __str__(self):
        return str(self.event.event_name) + "-" + str(self.id)
    

class Feedback(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="feedback_event")
    feedback = models.TextField()
    feedback_by = models.ForeignKey(EventRegistration,on_delete=models.CASCADE,related_name="feedback_user")
    
    def __str__(self):
        return str(self.event.event_name) + "-id-" + str(self.id)

class EventMcqAnswer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    question_id = models.ForeignKey(EventMCQQuestions,on_delete=models.CASCADE)
    answer = models.CharField(max_length=999)
    correct_answer = models.CharField(max_length=999)

class EventPollAnswer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    question_id = models.ForeignKey(EventPollsQuestions,on_delete=models.CASCADE)
    answer = models.CharField(max_length=999)

class EventWrittenAnswer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    question_id = models.ForeignKey(EventWrittenQuestions,on_delete=models.CASCADE)
    answer = models.TextField()


class EventCalender(models.Model):
    date = models.DateField()
    event = models.ForeignKey(Event,on_delete=models.CASCADE)