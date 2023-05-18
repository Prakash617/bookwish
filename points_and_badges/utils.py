
from user_accounts.models import CustomUser
from club.models import *

import datetime
from datetime import date

from .models import *

def update_book_reading_points(start_page, end_page, userid):
    page = end_page - start_page
    if page < 5 :
        points = 0
    elif page < 10:
        points = 1
    elif page < 15:
        points = 2
    elif page < 20:
        points = 3
    elif page >= 20:
        points = 4
    else:
        points = 0

    current_user = CustomUser.objects.get(id=userid)
    BookReadingPointTable.objects.create(date=datetime.now(), user=current_user, level=points)
    current_user.points += points
    current_user.save()

def update_physical_points(time, userid):
    if time < 15 :
        points = 0
    elif time < 30:
        points = 1
    elif time < 45:
        points = 2
    elif time < 60:
        points = 3
    elif time >= 60:
        points = 4
    else:
        points = 0

    current_user = CustomUser.objects.get(id=userid)
    PhysicalPointTable.objects.create(date=datetime.now(), user=current_user, level=points)
    current_user.points += points
    current_user.save()


def update_meditation_points(time,userid):
    
    if time < 10 :
        points = 0
    elif time < 20:
        points = 1
    elif time < 30:
        points = 2
    elif time < 45:
        points = 3
    elif time >= 45:
        points = 4
    else:
        points = 0
    
    current_user = CustomUser.objects.get(id=userid)
    MeditationPointTable.objects.create(date=datetime.now(), user=current_user, level=points)
    current_user.points += points
    current_user.save()


def update_relationship_points(userid):
    current_user = CustomUser.objects.get(id=userid)
    
    obj = Relationship.objects.get(userid=current_user,record_date=date.today())
    average_relationship_store = obj.plus_points - obj.neg_points
    if average_relationship_store < 1 :
        points = 0
    elif average_relationship_store < 2:
        points = 1
    elif average_relationship_store < 4:
        points = 2
    elif average_relationship_store < 6:
        points = 3
    elif average_relationship_store >= 6:
        points = 4
    else:
        points = 0
    
    
    Relationship_obj = RelationshipPointTable.objects.filter(date=date.today(), user=current_user).exists()
    print(Relationship_obj)
    if not Relationship_obj:
        RelationshipPointTable.objects.create(date=datetime.now(), user=current_user, level=points)        
    else:
        current_obj = RelationshipPointTable.objects.get(date=date.today(), user=current_user)
        current_obj.date=date.today()
        current_obj.user = current_user
        current_obj.level= points
        current_obj.save()

    


from datetime import datetime, timedelta

def format_date(date_str):
    # Parse the date string into a datetime object
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

    # Get the year, month (abbreviated), and day from the datetime object
    year = dt.year
    month_name = dt.strftime('%b')  # Use '%b' for abbreviated month name
    day = dt.day

    # Construct the output string
    output_str = f"{year} {month_name} {day}"

    # Return the output string
    return output_str

# Example usage
# date_str = '2023-02-17 08:22:44+00:00'
# formatted_date = format_date(date_str)
# print(formatted_date)
# return formatted_date


