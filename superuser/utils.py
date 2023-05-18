def get_DailyStepCount(distance):
    step = 0
    for d in distance:
        step += d.distance
        
    return step

def get_relations(relations):
    neg_points = 0
    pos_points = 0
    for r in relations:
        neg_points += r.neg_points
        pos_points += r.plus_points
        
    return neg_points,pos_points

def get_BookReading(books):
    pages = 0
    for b in books:
        pages += b.end_page - b.start_page
    
    return pages


import re
import cloudinary
import cloudinary.api
import cloudinary.uploader


def delete_image_from_url(url):
    # Use a regular expression to extract the public ID from the URL
    match = re.search(r"upload/(.+)\.", url)
    if not match:
        print("Error: Could not extract public ID from URL")
    else:
        public_id_with_version = match.group(1)
        public_id = public_id_with_version.split('/')[-1].split('.')[0]
        print("Public ID: " + public_id)

    # Call the destroy method to delete the image
    response = cloudinary.uploader.destroy(public_id)

    # Check the response to see if the image was successfully deleted
    if response['result'] == 'ok':
        print("Image was successfully deleted")
    else:
        print("Failed to delete image: " + response['message'])

# delete_image_from_url("https://res.cloudinary.com/dnfwsqh2e/image/upload/v1677648347/Screenshot_from_2023-02-26_09-09-50_ycqjzm.png")

# def users_by_month(query_set):
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
# from user_accounts.models import CustomUser

# def users_by_month():
def users_by_month(model):
    now = datetime.now()
    start_year = datetime(now.year, 1, 1)
    end_year = datetime(now.year + 1, 1, 1)

    users_by_month = model.objects.filter(
        date_joined__gte=start_year,
        date_joined__lt=end_year
    ).annotate(
        month=TruncMonth('date_joined')
    ).values(
        'month'
    ).annotate(
        total_users=Count('id')
    ).order_by('month')

    # create a list of dictionaries with month names
    month_names = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]

    # create a list of dictionaries with total users per month
    users_by_month_with_names = []
    for month in users_by_month:
        month_name = month['month'].strftime('%B')
        users_by_month_with_names.append({
            'month': month_name,
            'total_users': month['total_users']
        })

    # fill in months with 0 users
    for month_name in month_names:
        found = False
        for month in users_by_month_with_names:
            if month['month'] == month_name:
                found = True
                break
        if not found:
            users_by_month_with_names.append({
                'month': month_name,
                'total_users': 0
            })

    # sort by month name
    users_by_month_with_names.sort(key=lambda x: month_names.index(x['month']))
    # print(users_by_month_with_names)
    return users_by_month_with_names
def club_by_month(model):
    now = datetime.now()
    start_year = datetime(now.year, 1, 1)
    end_year = datetime(now.year + 1, 1, 1)

    users_by_month = model.objects.filter(
        date_join__gte=start_year,
        date_join__lt=end_year
    ).annotate(
        month=TruncMonth('date_join')
    ).values(
        'month'
    ).annotate(
        total_users=Count('club_id')
    ).order_by('month')

    # create a list of dictionaries with month names
    month_names = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]

    # create a list of dictionaries with total users per month
    users_by_month_with_names = []
    for month in users_by_month:
        month_name = month['month'].strftime('%B')
        users_by_month_with_names.append({
            'month': month_name,
            'total_users': month['total_users']
        })

    # fill in months with 0 users
    for month_name in month_names:
        found = False
        for month in users_by_month_with_names:
            if month['month'] == month_name:
                found = True
                break
        if not found:
            users_by_month_with_names.append({
                'month': month_name,
                'total_users': 0
            })

    # sort by month name
    users_by_month_with_names.sort(key=lambda x: month_names.index(x['month']))
    # print(users_by_month_with_names)
    return users_by_month_with_names