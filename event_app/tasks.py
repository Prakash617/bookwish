from celery import shared_task

from event_app.utils import send_mail_event_information
from .models import EventRegistration,Event
import datetime



@shared_task
def send_event_remainder():
    events = Event.objects.all()
    users = EventRegistration.objects.all()
    context = {}
    for event in events:
            event_date = datetime.datetime.today() - datetime.timedelta(days=1)
            # print("1")
            print(event_date.date())
            print(event.event_start_date)
            if event.event_start_date == event_date.date():
                event_user = users.filter(event=event)
                context['data'] = event
                # print("2")
                for user in event_user:
                    email = user.email
                    # print("3")
                    send_mail_event_information(email,context)

    
