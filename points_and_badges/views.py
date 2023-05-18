from django.db.models import Sum
from django.http import HttpResponse
from user_accounts.models import CustomUser
from datetime import date, timedelta
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
import csv
import requests
import json
from django.shortcuts import render
from points_and_badges.tasks import update_point_and_badge
from rest_framework.generics import ListAPIView
from .serializers import CombineWeeklyPointsSerializer, CombineDailyPointsSerializer
from . models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from club.week_generator import get_week_dates
from rest_framework.authtoken.models import Token
from datetime import date
from bookwishes.settings import ip
# Create your views here.

from .utils import *


class CombineWeeklyPointsView(APIView):
    serializer_class = CombineWeeklyPointsSerializer

    def get(self, request):
        book_reading_point_data = WeeklyBookReadingPointTable.objects.filter(
            user=self.request.user)
        physical_point_data = WeeklyPhysicalPointTable.objects.filter(
            user=self.request.user)
        meditation_point_data = WeeklyMeditationPointTable.objects.filter(
            user=self.request.user)
        relationship_point_data = WeeklyRelationshipPointTable.objects.filter(
            user=self.request.user)
        dates = get_week_dates(date.today(), 0)

        # change today_data variable name to this_week_data
        this_week_data = {
            "book_reading_data": 0,
            "physical_data": 0,
            "meditation_data": 0,
            "relationship_data": 0,
        }

        archive_data = {
            "book_reading_data": [],
            "physical_data": [],
            "meditation_data": [],
            "relationship_data": [],
        }

        combined_data = {
            "this_week_data": this_week_data,
            "archive_data": archive_data


        }
        
        for data in book_reading_point_data:
            archive_data['book_reading_data'].append(
                {'user': data.user.id, 'date': data.date, 'level': data.level})
            if data.date == dates[6]:
                this_week_data['book_reading_data'] = data.level

        for data in physical_point_data:
            archive_data['physical_data'].append(
                {'user': data.user.id, 'date': data.date, 'level': data.level})
            if data.date == dates[6]:
                this_week_data['physical_data'] = data.level

        for data in meditation_point_data:
            archive_data['meditation_data'].append(
                {'user': data.user.id, 'date': data.date, 'level': data.level})
            if data.date == dates[6]:
                this_week_data['meditation_data'] = data.level

        for data in relationship_point_data:
            archive_data['relationship_data'].append(
                {'user': data.user.id, 'date': data.date, 'level': data.level})
            if data.date == dates[6]:
                this_week_data['relationship_data'] = data.level

        return Response(combined_data)

def group_by_club_name(data):
    club_dict = {}
    for obj in data:
        club_name = obj["club_name"]
        if club_name in club_dict:
            club_dict[club_name].append(obj)
        else:
            club_dict[club_name] = [obj]
    return club_dict
from rest_framework.permissions import IsAuthenticated
class IsSuperuser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_superuser

class ClubBadegeView(APIView):
    serializer_class = CombineWeeklyPointsSerializer
    permission_classes = [IsSuperuser]
    
    def get(self, request, *args, **kwargs):
        dates = WeeklyBookReadingPointTable.objects.all().values('date').distinct()

        
        clubs = Club.objects.all()
        csvrow = {
            "club_name":'',
            'data':[],
            
        }
        context = {
            
            'club_name':'',
            'date':{
                "start_date":'',
                "end_date":''
                },
            'bookreadingppoints':{},
            'Relationshippoints':{},
            'Meditationpoints':{},
            'Step_Counterpoints':{},
            
        }
        row_data ={
            
        }
        # # print(clubs[0].)
        datalist = []
        for club in clubs:
            club_set = True
            
            #     print(club)
            users = CustomUser.objects.filter(club=club)
                
                # print(date)
            for date in dates: 
                bookreading = {
                                'Beginner': 0,
                                'Competent': 0,
                                'Proficient': 0,
                                'Expert': 0,
                                }

                Relationship = {
                                'Beginner': 0,
                                'Competent': 0,
                                'Proficient': 0,
                                'Expert': 0,
                                }
                Meditation = {
                                'Beginner': 0,
                                'Competent': 0,
                                'Proficient': 0,
                                'Expert': 0,
                                }
                Step_Counter = {
                                'Beginner': 0,
                                'Competent': 0,
                                'Proficient': 0,
                                'Expert': 0,
                                }
                for user in users:
                
                    # instances = WeeklyBookReadingPointTable.objects.filter(date=date['date'],user = user)
                    wbr = WeeklyBookReadingPointTable.objects.filter(date=date['date'],user = user)
                    # print('date',date)
                    # print('wbr',wbr)
                    wrt = WeeklyRelationshipPointTable.objects.filter(date=date['date'],user = user)
                    wpt = WeeklyPhysicalPointTable.objects.filter(date=date['date'],user = user)
                    wmt = WeeklyMeditationPointTable.objects.filter(date=date['date'],user = user)
                    
                    
                    for w in wbr:
                        if w.level == 1:
                            bookreading['Beginner'] += 1
                        elif w.level == 2:
                            bookreading['Competent'] += 1
                        elif w.level == 3:
                            bookreading['Proficient'] += 1
                        else:
                            bookreading['Expert'] += 1
                    for w in wrt:
                        if w.level == 1:
                            Relationship['Beginner'] += 1
                        elif w.level == 2:
                            Relationship['Competent'] += 1
                        elif w.level == 3:
                            Relationship['Proficient'] += 1
                        else:
                            Relationship['Expert'] += 1
                    for w in wmt:
                        if w.level == 1:
                            Meditation['Beginner'] += 1
                        elif w.level == 2:
                            Meditation['Competent'] += 1
                        elif w.level == 3:
                            Meditation['Proficient'] += 1
                        else:
                            Meditation['Expert'] += 1
                    for w in wpt:
                        if w.level == 1:
                            Step_Counter['Beginner'] += 1
                        elif w.level == 2:
                            Step_Counter['Competent'] += 1
                        elif w.level == 3:
                            Step_Counter['Proficient'] += 1
                        else:
                            Step_Counter['Expert'] += 1
                
                context['club_name'] = user.club.club_name
                context['bookreadingppoints'] =bookreading
                base_date = date['date']
                week_dates = get_week_dates(base_date, 0)
                start_date = format_date(week_dates[0].strftime('%Y-%m-%d'))
                end_date = format_date(week_dates[-1].strftime('%Y-%m-%d'))
                context['date']['start_date']= start_date 
                context['date']['end_date']= end_date 
                context['Relationshippoints']=Relationship
                context['Meditationpoints']=Meditation
                context['Step_Counterpoints']=Step_Counter
            
                datalist.append(context.copy())
            
        grouped_data = group_by_club_name(datalist)
        
        # writing csv---------------
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Badegs_club_summary.csv"'
        writer = csv.writer(response)
        # Write the header row

        # writer.writerow(['', '','', '','', '','', '','', '<span style="font-size:24px; font-weight:bold;">Badegs Club Summary</span>'])
        writer.writerow(['', ''])
        writer.writerow(['', ''])
        writer.writerow(['', ''])
        
        writer.writerow(['', '', '',
                    'Book', '', '', '',
                    'Relationship', '', '', '',
                    'Step Counter', '', '', '',
                    'Meditation', '', '', '',
                    ])
     
        writer.writerow(['Name', 'Start Date', 'End Date',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert'])

        for club in grouped_data:
            print(club)
            writer.writerow([club])
            for data in grouped_data[club]:
                print(data['club_name'])
                print(data['date']['start_date'])
                writer.writerow([
                        "", data['date']['start_date'], data['date']['end_date'],
                        # for bookreading
                        
                        data['bookreadingppoints']['Beginner'], data['bookreadingppoints']['Competent'], 
                            data['bookreadingppoints']['Proficient'], data['bookreadingppoints']['Expert'],
                        # Relationship
                        data['Relationshippoints']['Beginner'], data['Relationshippoints']['Competent'], 
                            data['Relationshippoints']['Proficient'], data['Relationshippoints']['Expert'],
                        # Step_Counter
                        data['Step_Counterpoints']['Beginner'], data['Step_Counterpoints']['Competent'], 
                            data['Step_Counterpoints']['Proficient'], data['Step_Counterpoints']['Expert'],
                        # Meditation
                        data['Meditationpoints']['Beginner'], data['Meditationpoints']['Competent'], data['Meditationpoints']['Proficient'], data['Meditationpoints']['Expert'],
                        ])
        
        return response
        # return Response({"data":grouped_data})

class DownloadExcel(APIView):
    serializer_class = CombineWeeklyPointsSerializer
    API_URL =ip + 'api/weekly-badges/'

    def get(self, request):
        # ip = 'http://127.0.0.1:8000/'
        # lcpaymentdetails_api = ip + 'api/weekly-badges/'
        print(self.headers)
        resp = requests.get(self.API_URL,
                            headers={
                                "Authorization": "Token 163801d87b10ff164ca6665c090ba1a6cb095ef4"
                            })
        # + str(self.kwargs['pk']) + '/detail/'
        user = CustomUser.objects.get(pk=1)
        # print(user.__dict__)
        # print(resp.json())
        data = resp.json()
        # print('----------------')
        # print('book_reading_data',
        #       data['archive_data']['book_reading_data'][0]['level'])
        # print('sum total', )
        return Response(data)


@api_view(('GET',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def export_csv(request, pk=None):
    API_URL =ip + 'api/weekly-badges/'
    if pk is not None:
        user = CustomUser.objects.get(pk=pk)
    else:
        return Response('No pk')
    # print('user', user)
    user_token = Token.objects.filter(user=user).first()
    try:

        token = user_token.key
    except:
        print('no token')
        return Response({'error': 'no token'})
    resp = requests.get(API_URL,
                        headers={
                            "Authorization": f"Token {user_token}"
                        })
    data = resp.json()
    # print(data['archive_data'])
    # //////////////////
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
        user.username)

    writer = csv.writer(response)
    # Write the header row
    # user = CustomUser.objects.get(pk=1)
    try:
        refer = Refer.objects.filter(onboarded_user=user).first().refer_code
    except:
        refer = 'no refer code'
    writer.writerow(['Name:', user.first_name + ' ' + user.last_name])
    # writer.writerow(['ReferCode:',user.refer_code])
    writer.writerow(['ReferCode:', refer])
    writer.writerow(['Username:', user.username])
    writer.writerow(['Email:', user.email])
    writer.writerow(['Address', user.location])
    writer.writerow(['Date Joined', user.date_joined])

    writer.writerow(['', ''])
    writer.writerow(['', ''])

    writer.writerow(['Start Date', 'End Date', 'Book Reading Badges',
                    'Relationship Badges', 'Meditation Badges', 'Step Count Badges'])
    archive_data = data['archive_data']

    book_reading_data = data['archive_data']['book_reading_data']
    physical_data = data['archive_data']['physical_data']
    meditation_data = data['archive_data']['meditation_data']
    relationship_data = data['archive_data']['relationship_data']
    
    for i, r in enumerate(book_reading_data):
        s_date = datetime.strptime(book_reading_data[i]['date'], '%Y-%m-%d')
        week_dates = get_week_dates(s_date, 0)

        start_date = format_date(week_dates[0].strftime('%Y-%m-%d'))

        end_date = format_date(week_dates[-1].strftime('%Y-%m-%d'))
        try:
            book_reading_level = book_reading_data[i]['level']
        except:
            book_reading_level = '-'
        try:
            relationship_level = relationship_data[i]['level']
        except:
            relationship_level = '-'
        try:
            meditation_level = meditation_data[i]['level']
        except:
            meditation_level = '-'
        try:
            physical_level = physical_data[i]['level']
        except:
            physical_level = '-'
        writer.writerow([
            start_date,
            end_date,
            book_reading_level,
            relationship_level,
            meditation_level,
            physical_level
        ])

    return response



    
def community_weekly_badges_csv(request, pk=None):
    
    # print('enter', pk)
    # club = Club.objects.get(pk=pk)
    # club_members = CustomUser.objects.filter(club=club).count()
    # print("club_members", club_members)
    # wbr = WeeklyBookReadingPointTable.objects.filter(user__club=pk)
    # wrt = WeeklyRelationshipPointTable.objects.filter(user__club=pk)
    # wpt = WeeklyPhysicalPointTable.objects.filter(user__club=pk)
    # wmt = WeeklyMeditationPointTable.objects.filter(user__club=pk)
    # bookreading = {
    #     'Beginner': 0,
    #     'Competent': 0,
    #     'Proficient': 0,
    #     'Expert': 0,
    # }

    # Relationship = {
    #     'Beginner': 0,
    #     'Competent': 0,
    #     'Proficient': 0,
    #     'Expert': 0,
    # }
    # Meditation = {
    #     'Beginner': 0,
    #     'Competent': 0,
    #     'Proficient': 0,
    #     'Expert': 0,
    # }
    # Step_Counter = {
    #     'Beginner': 0,
    #     'Competent': 0,
    #     'Proficient': 0,
    #     'Expert': 0,
    # }

    # for w in wbr:
    #     print('wbr', type(w.level))
    #     if w.level == 1:
    #         bookreading['Beginner'] += 1
    #     elif w.level == 2:
    #         bookreading['Competent'] += 1
    #     elif w.level == 3:
    #         bookreading['Proficient'] += 1
    #     else:

    #         bookreading['Expert'] += 1
    # for w in wrt:
    #     if w.level == 1:
    #         Relationship['Beginner'] += 1
    #     elif w.level == 2:
    #         Relationship['Competent'] += 1
    #     elif w.level == 3:
    #         Relationship['Proficient'] += 1
    #     else:

    #         Relationship['Expert'] += 1
    # for w in wmt:
    #     if w.level == 1:
    #         Meditation['Beginner'] += 1
    #     elif w.level == 2:
    #         Meditation['Competent'] += 1
    #     elif w.level == 3:
    #         Meditation['Proficient'] += 1
    #     else:

    #         Meditation['Expert'] += 1
    # for w in wpt:
    #     if w.level == 1:
    #         Step_Counter['Beginner'] += 1
    #     elif w.level == 2:
    #         Step_Counter['Competent'] += 1
    #     elif w.level == 3:
    #         Step_Counter['Proficient'] += 1
    #     else:

    #         Step_Counter['Expert'] += 1

    # context = {
    #     'club_name': club.club_name,
    #     'total_users': club_members,
    #     'bookreading': bookreading,
    #     'Relationship': Relationship,
    #     'Step_Counter': Step_Counter,
    #     'Meditation': Meditation
    # }
    # print('context', context)

    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
    #     club.club_name)

    # writer = csv.writer(response)
    # # Write the header row

    # writer.writerow(['Club_name:', club.club_name])
    # writer.writerow(['club_owner', club.club_owner])
    # writer.writerow(['Club Created at', club.date_join])

    # writer.writerow(['', ''])
    # writer.writerow(['', ''])

    # writer.writerow(['', '', '',
    #                 'Book', '', '', '',
    #                  'Relationship', '', '', '',
    #                  'Step Counter', '', '', '',
    #                  'Meditation', '', '', '',

    #                  ])
    # writer.writerow(['Name', 'Start Date', 'End Date',
    #                 'Beginner', 'Competent', 'Proficient', 'Expert',
    #                  'Beginner', 'Competent', 'Proficient', 'Expert',
    #                  'Beginner', 'Competent', 'Proficient', 'Expert',
    #                  'Beginner', 'Competent', 'Proficient', 'Expert'])

    # writer.writerow([
    #     context['total_users'], "", "",
    #     # for bookreading
    #     context['bookreading']['Beginner'], context['bookreading']['Competent'], context[
    #         'bookreading']['Proficient'], context['bookreading']['Expert'],
    #     # Relationship
    #     context['Relationship']['Beginner'], context['Relationship']['Competent'], context[
    #         'Relationship']['Proficient'], context['Relationship']['Expert'],
    #     # Step_Counter
    #     context['Step_Counter']['Beginner'], context['Step_Counter']['Competent'], context[
    #         'Step_Counter']['Proficient'], context['Step_Counter']['Expert'],
    #     # Meditation
    #     context['Meditation']['Beginner'], context['Meditation']['Competent'], context['Meditation']['Proficient'], context['Meditation']['Expert'],
    # ])

    # return response
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'
    writer = csv.writer(response)
    # Write the header row


    writer.writerow(['', ''])
    writer.writerow(['', ''])

    writer.writerow(['', '', '',
                    'Book', '', '', '',
                    'Relationship', '', '', '',
                    'Step Counter', '', '', '',
                    'Meditation', '', '', '',
                    ])
    
    writer.writerow(['Name', 'Start Date', 'End Date',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert',
                    'Beginner', 'Competent', 'Proficient', 'Expert'])
    
    
    
    
    
    
    dates = WeeklyBookReadingPointTable.objects.all().values('date').distinct()
    # for date in dates:
    #     instances = WeeklyBookReadingPointTable.objects.filter(date=date['date'])
    #     print(instances)
        
    clubs = Club.objects.all()
    csvrow = {
        'data':[],
    }
    context = {
        
        'bookreadingppoints':[],
        'Relationshippoints':[],
        'Meditationpoints':[],
        'Step_Counterpoints':[],
    }
    # # print(clubs[0].)
    for club in clubs:
        club_set = True
        bookreading = {
        'Beginner': 0,
        'Competent': 0,
        'Proficient': 0,
        'Expert': 0,
        }

        Relationship = {
        'Beginner': 0,
        'Competent': 0,
        'Proficient': 0,
        'Expert': 0,
        }
        Meditation = {
        'Beginner': 0,
        'Competent': 0,
        'Proficient': 0,
        'Expert': 0,
        }
        Step_Counter = {
        'Beginner': 0,
        'Competent': 0,
        'Proficient': 0,
        'Expert': 0,
        }
        
    #     print(club)
        users = CustomUser.objects.filter(club=club)
            
        for user in users:
            for date in dates:
                # instances = WeeklyBookReadingPointTable.objects.filter(date=date['date'],user = user)
                wbr = WeeklyBookReadingPointTable.objects.filter(date=date['date'],user = user)
                wrt = WeeklyRelationshipPointTable.objects.filter(date=date['date'],user = user)
                wpt = WeeklyPhysicalPointTable.objects.filter(date=date['date'],user = user)
                wmt = WeeklyMeditationPointTable.objects.filter(date=date['date'],user = user)
                
                # bookreading["Beginner"] = 
                for w in wbr:
                    print('wbr', type(w.level))
                    if w.level == 1:
                        bookreading['Beginner'] += 1
                    elif w.level == 2:
                        bookreading['Competent'] += 1
                    elif w.level == 3:
                        bookreading['Proficient'] += 1
                    else:

                        bookreading['Expert'] += 1
                for w in wrt:
                    if w.level == 1:
                        Relationship['Beginner'] += 1
                    elif w.level == 2:
                        Relationship['Competent'] += 1
                    elif w.level == 3:
                        Relationship['Proficient'] += 1
                    else:

                        Relationship['Expert'] += 1
                for w in wmt:
                    if w.level == 1:
                        Meditation['Beginner'] += 1
                    elif w.level == 2:
                        Meditation['Competent'] += 1
                    elif w.level == 3:
                        Meditation['Proficient'] += 1
                    else:

                        Meditation['Expert'] += 1
                for w in wpt:
                    if w.level == 1:
                        Step_Counter['Beginner'] += 1
                    elif w.level == 2:
                        Step_Counter['Competent'] += 1
                    elif w.level == 3:
                        Step_Counter['Proficient'] += 1
                    else:

                        Step_Counter['Expert'] += 1
                    
            context['bookreadingppoints'].append(bookreading)
            context['Relationshippoints'].append(Relationship)
            context['Meditationpoints'].append(Meditation)
            context['Step_Counterpoints'].append(Step_Counter)
        
            
        
        csvrow['club_name'] = club.club_name
        csvrow['data'].append(context)
        print("================================")
        # print(csvrow)
        print("================================")
        
    for data in csvrow['data']:
        
        print("dasdasd", data)
        
        writer.writerow([
        context['club_name'], "", "",
        # for bookreading
        
        context['bookreadingppoints']['Beginner'], context['bookreading']['Competent'], context[
            'bookreading']['Proficient'], context['bookreading']['Expert'],
        # Relationship
        context['Relationship']['Beginner'], context['Relationship']['Competent'], context[
            'Relationship']['Proficient'], context['Relationship']['Expert'],
        # Step_Counter
        context['Step_Counter']['Beginner'], context['Step_Counter']['Competent'], context[
            'Step_Counter']['Proficient'], context['Step_Counter']['Expert'],
        # Meditation
        context['Meditation']['Beginner'], context['Meditation']['Competent'], context['Meditation']['Proficient'], context['Meditation']['Expert'],
        ])
    
        
    
    # return response
            
            
    
    # for count,user in enumerate (CustomUser.objects.all()):
    #     for club in clubs:
    #         if user.club == club:
    #             for date in dates:
    #                 # print('date')
    #                 # date = datetime.date(2023, 3, 17)
    #                 # date_string = date.strftime('%Y-%m-%d')
    #                 # print(date['date'])
    #                 # s_date = datetime.strptime(date['date'], '%Y-%m-%d')
    #                 # week_dates = get_week_dates(s_date, 1)
    #                 # start_date = format_date(week_dates[0].strftime('%Y-%m-%d'))
    #                 # end_date = format_date(week_dates[1].strftime('%Y-%m-%d'))
                    
    #                 wbr = WeeklyBookReadingPointTable.objects.filter(date = date,user = user)
    #                 wrt = WeeklyRelationshipPointTable.objects.filter(date = date,user = user)
    #                 wpt = WeeklyPhysicalPointTable.objects.filter(date = date,user = user)
    #                 wmt = WeeklyMeditationPointTable.objects.filter(date = date,user = user)
    #                 for w in wbr:
    #                     print('wbr', type(w.level))
    #                     if w.level == 1:
    #                         bookreading['Beginner'] += 1
    #                     elif w.level == 2:
    #                         bookreading['Competent'] += 1
    #                     elif w.level == 3:
    #                         bookreading['Proficient'] += 1
    #                     else:

    #                         bookreading['Expert'] += 1
    #                 for w in wrt:
    #                     if w.level == 1:
    #                         Relationship['Beginner'] += 1
    #                     elif w.level == 2:
    #                         Relationship['Competent'] += 1
    #                     elif w.level == 3:
    #                         Relationship['Proficient'] += 1
    #                     else:

    #                         Relationship['Expert'] += 1
    #                 for w in wmt:
    #                     if w.level == 1:
    #                         Meditation['Beginner'] += 1
    #                     elif w.level == 2:
    #                         Meditation['Competent'] += 1
    #                     elif w.level == 3:
    #                         Meditation['Proficient'] += 1
    #                     else:

    #                         Meditation['Expert'] += 1
    #                 for w in wpt:
    #                     if w.level == 1:
    #                         Step_Counter['Beginner'] += 1
    #                     elif w.level == 2:
    #                         Step_Counter['Competent'] += 1
    #                     elif w.level == 3:
    #                         Step_Counter['Proficient'] += 1
    #                     else:

    #                         Step_Counter['Expert'] += 1

    #                 writer.writerow([
    #                 context['something'], "", "",
    #                 # for bookreading
    #                 context['bookreading']['Beginner'], context['bookreading']['Competent'], context[
    #                     'bookreading']['Proficient'], context['bookreading']['Expert'],
    #                 # Relationship
    #                 context['Relationship']['Beginner'], context['Relationship']['Competent'], context[
    #                     'Relationship']['Proficient'], context['Relationship']['Expert'],
    #                 # Step_Counter
    #                 context['Step_Counter']['Beginner'], context['Step_Counter']['Competent'], context[
    #                     'Step_Counter']['Proficient'], context['Step_Counter']['Expert'],
    #                 # Meditation
    #                 context['Meditation']['Beginner'], context['Meditation']['Competent'], context['Meditation']['Proficient'], context['Meditation']['Expert'],
    #             ])
    #             print("\n================================",bookreading)
        
    
    # return response



from django.db.models import IntegerField, F
from django.db.models.functions import Cast

def all_community_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="community.csv"'
    writer = csv.writer(response)

    context = {}
    clubs = Club.objects.all()
    # club_name = club.club_name
    # club_owner = club.club_owner
    # club_name = club.club_name
    context["data"] = []
    post_count = 0
    neg_points = 0
    pos_points = 0

    # writer.writerow(['ClubName:', club.club_name])
    # writer.writerow(['Club Owner:', club.club_owner])
    # writer.writerow(['Date Joined', club.date_join])

    writer.writerow(['', ''])
    writer.writerow(['', ''])
    # heading table
    writer.writerow(['name', 'total_members', 'total_posts',
                    'total_steps', 'total_pages', 'neg_points', 'plus_points'])
    for c in clubs:
        total_steps = 0
        neg_points = 0
        pos_points = 0
        total_read_pages = 0
        Custom_user = CustomUser.objects.filter(club=c.club_id)
        post = Post.objects.filter(posted_club=c.club_id)
        post_count = post.count()
        member_count = Custom_user.count()

        for u in Custom_user:
            dc = DailyStepCount.objects.filter(
                userid=u.id).aggregate(total=Sum("distance"))
            sum = dc['total'] if dc['total'] else 0
            total_steps += sum

            read_pages = BookReading.objects.filter(userid=u.id).annotate(read_pages=Cast(F('end_page') - F('start_page'),  output_field=IntegerField())
                                                                        ).aggregate(total=Sum('read_pages'))

            page = read_pages['total'] if read_pages['total'] else 0
            total_read_pages += page

            neg_point = Relationship.objects.filter(
                userid=u.id).aggregate(total=Sum("neg_points"))
            negs = neg_point['total'] if neg_point['total'] else 0
            neg_points += negs
            pos_point = Relationship.objects.filter(
                userid=u.id).aggregate(total=Sum("plus_points"))
            pos = pos_point['total'] if pos_point['total'] else 0
            pos_points += pos

        current_data = {
            'club_id': c.club_id,
            'name': c.club_name,
            'total_members': member_count,
            'total_posts': post_count,
            'total_steps': total_steps,
            'total_pages': total_read_pages,
            'neg_points': neg_points,
            'plus_points': pos_points
        }

        writer.writerow([
            c.club_name,
            member_count,
            post_count,
            total_steps,
            total_read_pages,
            neg_points,
            pos_points
        ])

    return response


class CombineDailyPointsView(APIView):
    serializer_class = CombineDailyPointsSerializer

    def get(self, request):
        today_data = {
            "book_reading_points": 0,
            "physical_points": 0,
            "meditation_points": 0,
            "relationship_points": 0,
            "average_daily_points": 0,
        }

        try:
            book_reading_point = BookReadingPointTable.objects.get(
                date=date.today(), user=self.request.user).level
        except:
            book_reading_point = 0

        try:
            physical_point = PhysicalPointTable.objects.get(
                date=date.today(), user=self.request.user).level
        except:
            physical_point = 0
        try:
            meditation_point = MeditationPointTable.objects.get(
                date=date.today(), user=self.request.user).level
        except:
            meditation_point = 0

        try:
            relationship_point = RelationshipPointTable.objects.get(
                date=date.today(), user=self.request.user).level
        except:
            relationship_point = 0
        # for data in physical_point:
        today_data['book_reading_points'] = book_reading_point
        # for data in physical_point:
        today_data['physical_points'] = physical_point
        # for data in physical_point:
        today_data['meditation_points'] = meditation_point

        # for data in physical_point:
        today_data['relationship_points'] = relationship_point

        today_data['average_daily_points'] = (
            physical_point + meditation_point + relationship_point + book_reading_point)/4
        return Response(today_data)
