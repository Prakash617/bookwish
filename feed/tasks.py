from celery import shared_task
from .models import Story,PopUp
from django.utils import timezone
from datetime import datetime, timedelta
from user_accounts.models import CustomUser
from .utils import send_mail_daily_report
from points_and_badges.models import PhysicalPointTable,MeditationPointTable,BookReadingPointTable,RelationshipPointTable
from .views import send_daily_progress




@shared_task
def delete_old_stories():
    stories = Story.objects.all()
    for story in stories:
        story.delete_old_stories()


   
@shared_task
def reset_pop_up():
    data = PopUp.objects.all()
    for d in data:
        d.is_popup = False
        d.save()



@shared_task
def set_pop_up():
    data = PopUp.objects.all()
    user = CustomUser.objects.all()
    context={}

    for d in data:
        d.is_popup = True
        d.save()
    

    
    for u in user:
        try:
            bookreading_data = BookReadingPointTable.objects.get(user=u, date=datetime.datetime.today()).level
        except:
            bookreading_data = 0
        try:
            meditation_data = MeditationPointTable.objects.get(user=u, date=datetime.datetime.today()).level
        except:
            meditation_data = 0
        try:
            physical_data = PhysicalPointTable.objects.get(user=u, date=datetime.datetime.today()).level
        except:
            physical_data = 0
        try:

            relationship_data = RelationshipPointTable.objects.get(user=u, date=datetime.datetime.today()).level
        except:
            relationship_data = 0
        context = {
            'book_reading_data': bookreading_data,
            'meditation_data': meditation_data,
            'physical_data': physical_data,
            'relationship_data': relationship_data,
        }

        send_mail_daily_report(u.email,context)
        