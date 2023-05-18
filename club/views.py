from django.shortcuts import render
from points_and_badges.utils import update_relationship_points
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, DestroyAPIView
from .models import *
from .serializers import BookReadingSerializer, CommentReportSerializer, PostReportSerializer, RelationshipSerializer, RelationshipUpdateSerializer, MeditationSerializer, HealthSerializer, DailyStepCountSerializer, PersonalAchievementSerializer, DigitalWellbeingSerializer, ReferSerializer, BadgeSerializer, HelpSupportSerializer, AppDataSerializer, ReportCategorySerializer, StoryReportSerializer, FeedbackSerializer

from rest_framework.generics import ListCreateAPIView, ListAPIView
from .models import BookReading, Meditation, PersonalAchievement, PostReport, Relationship, Health, DailyStepCount, DigitalWellbeing, Refer, Badge, HelpSupport, AppData, ReportCategory, StoryReport
from user_accounts.models import CustomUser
from rest_framework.response import Response
from user_accounts.serializers import CustomUserSerializer
from feed.models import Comment, Post, Story
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import user_passes_test
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import random
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from datetime import datetime


from .week_generator import *
from .utils import *


# Create your views here.
class DailyStepCountView(ListCreateAPIView):
    queryset = DailyStepCount.objects.all()
    serializer_class = DailyStepCountSerializer

    def list(self, request):
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user).order_by('-record_date')
        serializer = DailyStepCountSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        step_exited = DailyStepCount.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        if step_exited:
            return Response({'error': 'cannot be post once in a day'})
        return super().post(request)


class StepCountWeekly(ListCreateAPIView):
    queryset = DailyStepCount.objects.all()
    serializer_class = DailyStepCountSerializer

    def list(self, request):
        dates = get_week_dates(datetime.datetime.today(), 0)
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user.id).filter(
            record_date__in=dates)

        serializer = DailyStepCountSerializer(qs, many=True)
        return Response(serializer.data)


class DailyStepCountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DailyStepCount.objects.all()
    serializer_class = DailyStepCountSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        print(datetime.datetime.now().strftime("%Y-%m-%d"))
        try:
            daily_step_detail = DailyStepCount.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            data = DailyStepCountSerializer(daily_step_detail).data
        except:
            data = {"status": "Dailystep Count detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            daily_step_detail = DailyStepCount.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(daily_step_detail, attr, value)
                print(attr, value)
            daily_step_detail.save()
            data = DailyStepCountSerializer(daily_step_detail).data
        except:
            data = {
                "update": "error",
                "status": "Dailystep Count update error"}
        return Response(data)


class PersonalAchievementView(ListCreateAPIView):
    queryset = PersonalAchievement.objects.all()
    serializer_class = PersonalAchievementSerializer


class PersonalAchievementDetailView(RetrieveUpdateDestroyAPIView):
    queryset = PersonalAchievement.objects.all()
    serializer_class = PersonalAchievementSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        try:
            personal_achievement = PersonalAchievement.objects.get(
                userid=userid)
            data = PersonalAchievementSerializer(personal_achievement).data
        except:
            data = {"status": "Personal Achievement detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            personal_achievement = PersonalAchievement.objects.get(
                userid=userid, target_set_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(personal_achievement, attr, value)
                print(attr, value)
            personal_achievement.save()
            data = PersonalAchievementSerializer(personal_achievement).data
        except:
            data = {"status": "Personal Achievement update error"}
        return Response(data)


class BookReadingView(ListCreateAPIView):
    queryset = BookReading.objects.all()
    serializer_class = BookReadingSerializer

    def list(self, request):
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user)
        serializer = BookReadingSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        book_reading_exists = BookReading.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        if book_reading_exists:
            return Response({'error': 'cannot be post once in a day'})
        return super().post(request)


class BookReadingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = BookReading.objects.all()
    serializer_class = BookReadingSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        # print(type(userid))
        # book_reading = BookReading.objects.get(userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
        # print(book_reading)
        # data = BookReadingSerializer(book_reading).data

        # print(data)

        try:
            book_reading = BookReading.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            data = BookReadingSerializer(book_reading).data
        except:
            data = {"status": "BookReading detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            book_reading = BookReading.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(book_reading, attr, value)
                print(attr, value)
            book_reading.save()
            data = BookReadingSerializer(book_reading).data
        except:
            data = {
                "update": "error",
                "status": "BookReading update error"
            }
        return Response(data)


class RelationshipView(ListAPIView):
    queryset = Relationship.objects.all().order_by('-record_date')
    serializer_class = RelationshipSerializer


class RelationshipRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        try:
            print('relation')
            relation = Relationship.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            print('after')
            data = RelationshipSerializer(relation).data
        except:
            data = {"status": "BookReading detail not found"}
        return Response(data)


class RelationshipWeekly(ListCreateAPIView):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

    def list(self, request, *args, **kwargs):
        dates = get_week_dates(datetime.datetime.today(), 0)
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user.id).filter(
            record_date__in=dates)
        serializer = RelationshipSerializer(qs, many=True).data
        # print(serializer[0])

        return Response(serializer)


class RelationshipUpdateView(APIView):
    serializer_class = RelationshipUpdateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id", "null")
        increment = serializer.validated_data.get("increment", 0)
        decrement = serializer.validated_data.get("decrement", 0)
        record_date = serializer.validated_data.get("record_date", "null")
        if request.user.id == user_id:
            cur_user = CustomUser.objects.get(id=user_id)

            # updates the relationship data of the user
            try:
                cur_rel = Relationship.objects.filter(
                    userid=user_id).get(record_date=record_date)
            except:
                cur_rel = Relationship.objects.create(
                    userid=cur_user, record_date=record_date)

            if increment:
                cur_rel.plus_points += 1
                cur_rel.record_date = record_date
                cur_rel.save()
            if decrement:
                cur_rel.neg_points += 1
                cur_rel.record_date = record_date
                cur_rel.save()

            # update the point into the relationship point table
            # using the utils update_relationship_points from 'points_and_badges' app to update the points
            update_relationship_points(cur_user.id)

            return Response({"status": "relationship stats updated"})
        else:
            return Response({"status": "relationship stats not updated"})


class MeditationView(ListCreateAPIView):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer

    def get(self, request, userid=None):
        meditation = Meditation.objects.filter(userid=request.user)
        data = MeditationSerializer(meditation, many=True).data
        return Response(data)

    def post(self, request):
        meditation_exists = Meditation.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        if meditation_exists:
            return Response({'error': 'cannot be post once in a day'})
        return super().post(request)


class MeditationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        try:
            meditation = Meditation.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            data = MeditationSerializer(meditation).data
        except:
            data = {"status": "Meditation detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            meditation = Meditation.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(meditation, attr, value)
                print(attr, value)
            meditation.save()
            data = MeditationSerializer(meditation).data
        except:
            data = {"status": "Meditation update error"}
        return Response(data)


class HealthView(ListCreateAPIView):

    serializer_class = HealthSerializer

    def get_queryset(self):
        user = self.request.user
        return Health.objects.filter(userid=user)

   


class HealthDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        try:
            health = Health.objects.filter(userid=userid).order_by("-record_date")[0]
            data = HealthSerializer(health).data
        except:
            data = {"status": "Health detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            health = Health.objects.get(userid=userid)
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(health, attr, value)
                print(attr, value)
            health.save()
            data = HealthSerializer(health).data
        except:
            data = {"status": "Health update error"}
        return Response(data)


class DigitalWellbeingView(ListCreateAPIView):
    queryset = DigitalWellbeing.objects.all()
    serializer_class = DigitalWellbeingSerializer


class DigitalWellbeingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DigitalWellbeing.objects.all()
    serializer_class = DigitalWellbeingSerializer
    lookup_field = "userid"

    def get(self, request, userid=None):
        try:
            digital_wellbeing = DigitalWellbeing.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            data = DigitalWellbeingSerializer(digital_wellbeing).data
        except:
            data = {"status": "DigitalWellbeing detail not found"}
        return Response(data)

    def update(self, request, userid=None):
        try:
            digital_wellbeing = DigitalWellbeing.objects.get(
                userid=userid, record_date=datetime.datetime.now().strftime("%Y-%m-%d"))
            request.data.pop("userid")
            for attr, value in request.data.items():
                setattr(digital_wellbeing, attr, value)
                print(attr, value)
            digital_wellbeing.save()
            data = DigitalWellbeingSerializer(digital_wellbeing).data
        except:
            data = {"status": "DigitalWellbeing update error"}
        return Response(data)


class ReferView(ListCreateAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferSerializer
    # permission_classes = [AllowAny]

    def get(self, request):
        try:
            refer = Refer.objects.filter(referred_by=request.user)
            data = ReferSerializer(refer, many=True, context={
                                   "request": request}).data
        except:
            data = {"status": "Refer detail not found"}
        return Response(data)


class ReferOnboardedView(ListCreateAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferSerializer
    # permission_classes = [AllowAny]

    def get(self, request):

        # refer = Refer.objects.filter(referred_by=request.user).exclude(onboarded_user=None)

        # data = ReferSerializer(refer, many=True).data

        try:
            refer = Refer.objects.filter(
                referred_by=request.user).exclude(onboarded_user=None)

            data = ReferSerializer(refer, many=True, context={
                                   "request": request}).data
        except:
            data = {"status": "Refer detail not found"}
        return Response(data)


class ReferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferSerializer
    permission_classes = [AllowAny]

    def get(self, request, refer_code=None):
        try:
            refer = Refer.objects.get(refer_code=refer_code)
            print(refer)
            data = ReferSerializer(refer, context={"request": request}).data
        except:
            data = {"status": "Refer detail not found"}
        return Response(data)

    def update(self, request, refer_code=None):
        try:
            refer = Refer.objects.get(
                refer_code=request.data.pop("refer_code"))
            onboarded_user = request.data.pop("onboarded_user")
            refer.onboarded_user = CustomUser.objects.get(id=onboarded_user)
            refer.save()
            data = ReferSerializer(refer).data
        except:
            data = {"status": "Refer update error"}
        return Response(data)


class BadgeView(ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer


class HelpSupportView(ListCreateAPIView):
    queryset = HelpSupport.objects.all()
    serializer_class = HelpSupportSerializer


class AppDataView(ListCreateAPIView):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    def get(self, request):
        try:
            app_data = AppData.objects.all().first()
            data = AppDataSerializer(app_data).data
        except:
            data = {"status": "AppData detail not found"}
        return Response(data)


class LeaderboardView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        try:
            my_leaderboard = CustomUser.objects.filter(id=request.user.id)
            my_leaderboard_data = CustomUserSerializer(
                my_leaderboard, many=True, context={"request": request}).data
            clubId = request.user.club
            leaderboard = CustomUser.objects.filter(
                club=clubId).order_by('-points')
            lead_data = CustomUserSerializer(leaderboard, many=True, context={
                                             "request": request}).data
            rank_data = list(leaderboard).index(request.user)
            data = {"rank": rank_data + 1,
                    "my_leaderboard": my_leaderboard_data, "leaderboard": lead_data}
            print('hey', my_leaderboard_data)
        except:
            data = {"status": "Leaderboard detail not found"}
        return Response(data)


class OverallAccomplishmentView(APIView):
    def get(self, request):
        try:
            cur_user = request.user
            try:
                total_no_of_pages = BookReading.objects.filter(userid=cur_user).aggregate(Sum('end_page'))[
                    'end_page__sum'] - BookReading.objects.filter(userid=cur_user).aggregate(Sum('start_page'))['start_page__sum']
            except:
                total_no_of_pages = 0
            total_no_of_posts = Post.objects.filter(postedBy=cur_user).count()
            total_no_of_meditations = Meditation.objects.filter(
                userid=cur_user).aggregate(Sum('time_mins'))
            total_no_of_distance = DailyStepCount.objects.filter(
                userid=cur_user).aggregate(Sum('distance'))
            total_no_of_calories = DailyStepCount.objects.filter(
                userid=cur_user).aggregate(Sum('calorie'))
            # total_no_of_steps = total_no_of_distance / 5 # 5 is the average distance per step
            data = {"total_no_of_pages": total_no_of_pages, "total_no_of_posts": total_no_of_posts, "total_no_of_meditations":
                    total_no_of_meditations, "total_no_of_distance": total_no_of_distance, "total_no_of_calories": total_no_of_calories}
        except:
            data = {"status": "Overall Accomplishment detail not found"}
        return Response(data)


class BookReadingWeekly(ListCreateAPIView):
    queryset = BookReading.objects.all()
    serializer_class = BookReadingSerializer

    def list(self, request, *args, **kwargs):
        dates = get_week_dates(datetime.datetime.today(), 0)
        print(dates)
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user.id).filter(
            record_date__in=dates)
        serializer = self.serializer_class(qs, many=True).data
        # print(serializer[0])

        return Response(serializer)


class MeditationWeekly(ListCreateAPIView):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer

    def list(self, request, *args, **kwargs):
        dates = get_week_dates(datetime.datetime.today(), 0)
        queryset = self.get_queryset()
        qs = queryset.filter(userid=request.user.id).filter(
            record_date__in=dates)
        serializer = self.serializer_class(qs, many=True).data
        # print(serializer[0])

        return Response(serializer)


class Tools_state(ListAPIView):
    queryset = DailyStepCount.objects.all()
    serializer_class = DailyStepCountSerializer

    def list(self, request, *args, **kwargs):
        res = {}
        # try:
        step_exited = DailyStepCount.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        book_reading_exists = BookReading.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        meditation_exists = Meditation.objects.filter(
            record_date=datetime.datetime.today(), userid=request.user)
        health_exists = Health.objects.filter(userid=request.user).first()



        # for weekly enter health data
        try:
            health = Health.objects.filter(userid=request.user).order_by('-date').first()
        

            today = datetime.date.today()   
            delta = today - health.date 
            days_difference = delta.days

            if days_difference >= 7:
               res['health_exists'] = False
            
            else:
                res['health_exists'] = True

        except:
            res['health_exists'] = False


        # relationship_exists = Relationship.objects.filter(record_date = datetime.datetime.today(),userid = request.user)

        res['step_exists'] = True if step_exited else False
        res['book_reading_exists'] = True if book_reading_exists else False
        res['meditation_exists'] = True if meditation_exists else False

        # try:
        #     res['health_exists'] = same_week(str(health_exists.date))
        # except:
        #     res['health_exists'] = False
            # res['relationship_exists'] = True if relationship_exists else False
        return Response(res, status=status.HTTP_200_OK)
        # except:
        # return Response(status= status.HTTP_400_BAD_REQUEST)
# class HealthWeekly(ListCreateAPIView):
#     queryset = Health.objects.all()
#     serializer_class = HealthWeaklySerializer

#     def list(self, request, *args, **kwargs):
#         dates = get_week_dates(datetime.datetime.today(),1,7)
#         queryset = self.get_queryset()
#         qs = queryset.filter(userid=request.user.id).filter(record_date__in=dates)
#         serializer = self.serializer_class(qs, many=True).data
#         # print(serializer[0])

#         return Response(serializer)


class ReportCategoryViewSet(ListAPIView):
    queryset = ReportCategory.objects.all()
    serializer_class = ReportCategorySerializer
    # permission_classes = [IsAdminUser]

    # @user_passes_test(lambda u: u.is_superuser)
    # def create(self,request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)


class PostReportViewSet(ListCreateAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = PostReportSerializer(self.queryset.all(), many=True, context={
                                    'request': request}).data
        if request.user.is_superuser:
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:

            return Response({'error': 'read permission only allowed to admin_user'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):

        user = request.user
        data = request.data
        report_category = data['report_category']
        report_obj = ReportCategory.objects.get(id=report_category)

        # post = Post.objects.filter(postId = data['post'] ).first()
        post = Post.objects.get(postId=data['post'])

        post_report = PostReport.objects.filter(
            post=post, reported_by=user).exists()
        if post_report:
            return Response({'msg': 'You have already reported this post'})

        else:
            try:
                postReport = PostReport.objects.create(
                    reported_by=user, report_category=report_obj, post=post)
                serializer = PostReportSerializer(postReport).data
                # print('create')
                return Response({'created': 'created data', 'data': serializer})
            except:
                return Response({'error': 'error occured creating post-report'})


class StoryReportViewSet(ListCreateAPIView):
    queryset = StoryReport.objects.all()
    serializer_class = StoryReportSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print('listing')

        data = StoryReportSerializer(self.queryset.all(), many=True, context={
                                     'request': request}).data
        if request.user.is_superuser:
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:

            return Response({'error': 'read permission only allowed to admin_user'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):

        user = request.user

        data = request.data
        report_category = data['report_category']
        report_obj = ReportCategory.objects.get(id=report_category)

        # post = Post.objects.filter(postId = data['post'] ).first()
        story = Story.objects.get(id=data['story'])

        story_report = StoryReport.objects.filter(
            story=story, reported_by=user).exists()
        if story_report:
            return Response({'msg': 'You have already reported this post'})

        else:
            try:
                storyReport = StoryReport.objects.create(
                    reported_by=user, report_category=report_obj, story=story)
                serializer = StoryReportSerializer(storyReport).data
                print('create')
                return Response({'created': 'created data', 'data': serializer})
            except:
                return Response({'error': 'error occured creating post-report'})


class CommentReportViewSet(ListCreateAPIView):
    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print('listing')

        data = CommentReportSerializer(self.queryset.all(), many=True, context={
                                       'request': request}).data
        if request.user.is_superuser:
            return Response({'data': data}, status=status.HTTP_200_OK)
        else:

            return Response({'error': 'read permission only allowed to admin_user'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):

        user = request.user

        data = request.data
        report_category = data['report_category']
        report_obj = ReportCategory.objects.get(id=report_category)

        # post = Post.objects.filter(postId = data['post'] ).first()
        comment = Comment.objects.get(id=data['comment'])

        comment_report = CommentReport.objects.filter(comment=comment).first()
        if comment_report:
            return Response({'msg': 'You have already reported this comment.'})

        else:
            try:
                commentReport = CommentReport.objects.create(
                    reported_by=user, report_category=report_obj, comment=comment)
                serializer = CommentReportSerializer(commentReport).data
                print('create')
                return Response({'created': 'created data', 'data': serializer})
            except:
                return Response({'error': 'error occured creating post-report'})


class FeedbackView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = FeedbackSerializer(self.queryset.all(), many=True, context={
                                  'request': request}).data
        if request.user.is_superuser:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'read permission only allowed to admin_user'}, status=status.HTTP_400_BAD_REQUEST)

    # def create(self,request, *args, **kwargs):


class PostReportDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PostReport.objects.all()
    serializer_class = PostReportSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        try:
            print('Delete')
            # instance = self.get_object()
            pk = kwargs['pk']
            print('Destroy', pk)
            post = Post.objects.get(postId=pk)
            post.delete()
            return Response({'msg': 'post and postreport is deleted'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'failed deleting post-report'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # print(post)

        # return super().delete(request, *args, **kwargs)
    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        print('Destroy', pk)
        post = PostReport.objects.get(id=pk).post
        print(post)


class HealthData(ListAPIView):
    serializer_class = HealthSerializer

    def get(self, request):
        try:
            health_data = Health.objects.filter(userid=request.user)
            # print("hey",health_data)
            health = Health.objects.filter(
                userid=request.user).order_by('-date').last()
            # print("hey",health.date)

            week_bmi_data = {
                "week1": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week2": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week3": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week4": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
            }

            week_weight_data = {
                "week1": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week2": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week3": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week4": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
            }
            week_waist_data = {
                "week1": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week2": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week3": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week4": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
            }
            week_hipsize_data = {
                "week1": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week2": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week3": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week4": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
            }
            week_bellysize_data = {
                "week1": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week2": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week3": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
                "week4": {
                    "start_date": 0,
                    "end_date": 0,
                    "value": 0.0
                },
            }

            combined_data = {
                "week_bmi_data": week_bmi_data,
                "week_weight_data": week_weight_data,
                "week_waist_data": week_waist_data,
                "week_hipsize_data": week_hipsize_data,
                "week_bellysize_data": week_bellysize_data
            }

            dates = get_dates(health.date)
            print("hello")
            print(dates)
            count = 0
            for date_items in dates:
                if count == 0:
                    if health_data.filter(date__in=date_items).exists():
                        week1 = health_data.filter(date__in=date_items)[0]

                        week_bmi_data["week1"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week1.bmi_val
                        }

                        week_weight_data["week1"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week1.weight
                        }
                        week_waist_data["week1"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week1.waist
                        }
                        week_bellysize_data["week1"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week1.bellysize
                        }
                        week_hipsize_data["week1"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week1.hipsize
                        }

                if count == 1:
                    if health_data.filter(date__in=date_items).exists():
                        week2 = health_data.filter(date__in=date_items)[0]

                        week_bmi_data["week2"] = {
                            "start_date": date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week2.bmi_val
                        }

                        week_weight_data["week2"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week2.weight
                        }
                        week_waist_data["week2"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week2.waist
                        }
                        week_bellysize_data["week2"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week2.bellysize
                        }
                        week_hipsize_data["week2"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week2.hipsize
                        }

                if count == 2:
                    if health_data.filter(date__in=date_items).exists():
                        week3 = health_data.filter(date__in=date_items)[0]

                        week_bmi_data["week3"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week3.bmi_val
                        }

                        week_weight_data["week3"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week3.weight
                        }
                        week_waist_data["week3"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week3.waist
                        }
                        week_bellysize_data["week3"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week3.bellysize
                        }
                        week_hipsize_data["week3"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week3.hipsize
                        }

                if count == 3:
                    if health_data.filter(date__in=date_items).exists():
                        week4 = health_data.filter(date__in=date_items)[0]

                        week_bmi_data["week4"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week4.bmi_val
                        }

                        week_weight_data["week4"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week4.weight
                        }
                        week_waist_data["week4"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week4.waist
                        }
                        week_bellysize_data["week4"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week4.bellysize
                        }
                        week_hipsize_data["week4"] = {
                            "start_date":date_items[0].strftime('%m/%d'),
                            "end_date": (date_items[0]+timedelta(days=7)).strftime('%m/%d'),
                            "value": week4.hipsize
                        }

                count = count +1
        

            return Response(combined_data)
        except:
           return Response({'msg': 'no data found'})
