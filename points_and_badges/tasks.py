from celery import shared_task
from club.week_generator import get_week_dates
from datetime import date
from .utils import *
from django.db.models import Sum

from user_accounts.models import CustomUser
from django.db.models.functions import Coalesce


@shared_task
def update_point_and_badge():
    dates = get_week_dates(date.today(), 0)

    all_users = CustomUser.objects.all()

    for user in all_users:
        data = BookReadingPointTable.objects.filter(date__in=dates, user=user).aggregate(total_levels=Coalesce(Sum('level'), 0))
        weekly_level_book_reading = int(data["total_levels"]/7)     
        user.mental_badge = weekly_level_book_reading
        WeeklyBookReadingPointTable.objects.create(user=user, date=date.today(), level=weekly_level_book_reading)
        
        data1 = PhysicalPointTable.objects.filter(date__in=dates, user=user).aggregate(total_levels=Coalesce(Sum('level'), 0))
        weekly_level_physical = int(data1['total_levels']/7)
        user.physical_badge = weekly_level_physical
        WeeklyPhysicalPointTable.objects.create(user=user, date=date.today(), level=weekly_level_physical)
        
        data2 = MeditationPointTable.objects.filter(date__in=dates, user=user).aggregate(total_levels=Coalesce(Sum('level'), 0))
        weekly_level_meditation = int(data2['total_levels']/7)
        user.spiritual_badge = weekly_level_meditation
        WeeklyMeditationPointTable.objects.create(user=user, date=date.today(), level=weekly_level_physical)

        data3 = RelationshipPointTable.objects.filter(date__in=dates, user=user).aggregate(total_levels=Coalesce(Sum('level'), 0))
        weekly_level_relation = int(data3['total_levels']/7)
        WeeklyRelationshipPointTable.objects.create(user=user, date=date.today(), level=weekly_level_physical)
        user.emotional_badge = weekly_level_relation
        user.save()
            
@shared_task
def daily_update_point_and_badge():
    all_users = CustomUser.objects.all()
    for user in all_users:
        try:
            book_reading_point = BookReadingPointTable.objects.get(date=date.today(), user=user).level
        except:
            book_reading_point = 0
        
        try:
            physical_point = PhysicalPointTable.objects.get(date=date.today(), user=user).level
        except:
            physical_point = 0
        try:
            meditation_point = MeditationPointTable.objects.get(date=date.today(), user=user).level
        except:
            meditation_point = 0

        try:
            relationship_point = RelationshipPointTable.objects.get(date=date.today(), user=user).level
        except:
            relationship_point = 0
    
        avarage_daily_point = (book_reading_point + physical_point + meditation_point + relationship_point)/4

        print("current points")
        user.points += avarage_daily_point
        user.save()
        # print(avarage_daily_point)
    
    
    