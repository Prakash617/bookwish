# import os
# from celery.schedules import crontab
# # from django_celery_beat.models import PeriodicTask
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookwishes.settings')

# app = Celery('bookwishes')
# app.conf.enable_utc= False

# app.conf.update(timezone='Asia/Kathmandu')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')


# # celery beat settings
# app.conf.beat_schedule = {
#     'delete_old_stories': {
#         'task': 'myapp.tasks.delete_old_stories',
#         'schedule': crontab(hour='*/24'),
#     },

# }

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')



import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
# from django_celery_beat.models import PeriodicTask
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookwishes.settings')

app = Celery('bookwishes')
app.conf.enable_utc= True

app.conf.update(timezone='Asia/Kathmandu')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
from datetime import datetime, timedelta
from django.utils import timezone
import calendar


# celery beat settings
app.conf.beat_schedule = {
    'delete_old_stories': {
        'task': 'feed.tasks.delete_old_stories',
        'schedule': timedelta(seconds=30), # to run the task every 30 seconds
    },
    'update_point_and_badge':{
        'task':'points_and_badges.tasks.update_point_and_badge',
        'schedule':crontab(hour=0, minute=1, day_of_week="sat"),
    },
    'daily_update_point_and_badge':{
        'task':'points_and_badges.tasks.daily_update_point_and_badge',
        'schedule':crontab(hour=21, minute=0),
    },
    'reset_pop_up':{
        'task':'feed.tasks.reset_pop_up',
        'schedule':crontab(hour=21, minute=0),
    },
    'set_pop_up':{
        'task':'feed.tasks.set_pop_up',
        'schedule':crontab(hour=0, minute=0),
    },
    'send_event_remainder':{
        'task':'event_app.tasks.send_event_remainder',
        'schedule':crontab(hour=21, minute=0),
    }
   
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')