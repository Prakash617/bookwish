from django.http import HttpResponse
from django.shortcuts import render

from feed.utils import decrease_like_count, increase_like_count, send_mail_daily_report
from notification.models import Notification
from points_and_badges.models import BookReadingPointTable, MeditationPointTable, PhysicalPointTable, RelationshipPointTable
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView,DestroyAPIView
from .models import *
import datetime
from rest_framework.permissions import AllowAny

# from rest_framework.generics import DeleteAPIView

from rest_framework.permissions import IsAuthenticated

# Create your views here.
# class FeedView(APIView):
#     def get(self, request):
#         user = request.user
#         posts = Post.objects.filter(user=user)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         request.data['user'] = user.id
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_g_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# storyserializer
class StoryView(ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    # def transform_result(self, datas):
    #     """custom data transformations"""
    #     result = {}
    #     for data in datas:
    #         key = str(data["userid"]["id"])
    #         if key in result:
    #             if data in result[key]:
    #                 continue
    #             result[key].append(data)
    #         else:
    #             result[key] = []
    #             result[key].append(data)
    #     return result

    # def get (self, request):
    #     user_club = self.request.user.club
    #     my_stories = Story.objects.filter(userid=request.user)
    #     # print("my_stories", my_stories)
    #     stories = Story.objects.filter(posted_club=user_club)
    #     # print("stories", stories)
    #     # stories = [*my_stories , *stories]
    #     serializer = StorySerializer(stories, many=True, context={'request': request})        
    #     return Response(serializer.data)
    def get(self, request):
        user_club = request.user.club
        my_stories = Story.objects.filter(userid=request.user)
        other_stories = Story.objects.filter(posted_club=user_club).exclude(userid=request.user)
        stories = list(my_stories) + list(other_stories)
        serializer = StorySerializer(stories, many=True, context={'request': request})
        return Response(serializer.data)
    
    # def post(
    
        # user = request.user
        # posted_club = user.club
        # story = Story.objects.create(userid=user, posted_club=posted_club, **validated_data)
        

class StoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = "id"

    def delete(self, request, id=None):
        reponse = {}
        if id:
            story  = Story.objects.filter(id = id , userid =request.user)
            if story.exists(): 
                story.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                reponse["error"] = "no story or unauthorised"
                return Response(reponse,status=status.HTTP_401_UNAUTHORIZED)

        reponse["error"] = "no story "
        return Response(reponse,status=status.HTTP_204_NO_CONTENT)
from django.db.models import F
class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get (self, request):
       
        user_club = request.user.club
        
        posts = Post.objects.filter(posted_club=user_club).order_by('-postdate', '-posttime')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class MyPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get (self, request):
        user = request.user
        posts = Post.objects.filter(postedBy=user)       
        serializer = PostSerializer(posts, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"

    def delete(self, request, pk=None):
        reponse = {}
        if pk:
            post  = Post.objects.filter(postId = pk , postedBy =request.user)
            if post.exists(): 
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                reponse["error"] = "no post or unauthoired"
                return Response(reponse,status=status.HTTP_401_UNAUTHORIZED)

        reponse["error"] = "no post "
        return Response(reponse,status=status.HTTP_204_NO_CONTENT)
        


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get (self, request):
        comments = Comment.objects.filter(commented_by=request.user)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"

    def delete(self, request, id):
        
        try:    
            comment = Comment.objects.get(id=id,commented_by = request.user)
            post = comment.post
            comment.delete()
            post.comments_count -= 1
            post.save()
            return Response({"status": "deleted by user"})
        except:
             pass
        
        
        try:
            comment = Comment.objects.get(id=id)
            postUser=comment.post.postedBy
            post = comment.post
            post.save()
            if postUser == request.user:
                post.comments_count -= 1
                post_comment=Comment.objects.get(id=id,post = post)
                post_comment.delete()
                return Response({"status": "deleted own_user_post_comment"})
        
        except:
            pass
            
        return Response({"status": "error occurred"})

        # user = request.user
        # print(user)
        # post = comment.post
        # post.comments_count -= 1
        # post.save()
        # if comment.post == postedBy:



class LikeView(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get (self, request):
        likes = Like.objects.filter(liked_by=request.user)
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)
    
   

class LikeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "id"

    def delete(self, request, id):
        like = Like.objects.get(id=id)
        post = like.post
        post.likes_count -= 1
        post.save()
        like.delete()
        return Response({"status": "deleted"})


def generateRatingNotification(userid, receiver, rating):
    print(receiver)
    new_rating = int(rating)
    try:
        if userid.picture == '':
            picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
        else:
            picture = userid.picture
            
        user_obj = CustomUser.objects.get(id=userid.id)
        # picture = user_obj.picture
        fullName = userid.first_name + " " + userid.last_name
        notification = f"{fullName} has rated {rating} on your post. "

        return {
            "description": notification,
            "picture": picture,
            "sender": user_obj,
            "revoker": receiver,
            "title": '',
            "upload_timestamp": datetime.datetime.now(),
        }
    except:
        return None

    
class RateView(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # lookup_field = "id"
    
    def post(self, request, *args, **kwargs):
        userid = request.user
        data = request.data
        
        try:
            like_obj = Like.objects.get(liked_by=userid, post=data['post'])
        except:
            like_obj = None
            
        if like_obj:
            like_obj.rating = data['rating']
            like_obj.save()
            # update the like count
            increase_like_count(data['post'])
            
            # send the notification that the post has been liked
            notify_user = Post.objects.get(postId=data['post']).postedBy
            print(notify_user)
            
            notification = generateRatingNotification(userid, notify_user, data["rating"])
            print(notification)
            print("hello")
            if notification is not None:
                # print('notification',notification['sender'])
                if notification['sender'] == notification['revoker']:
                    return Response({"info":"self notification not allowed"})
                else:
                    Notification.objects.create(**notification)
            
            
            return Response(LikeSerializer(like_obj).data)
        
        else:
            
            post = Post.objects.get(postId=data["post"])
            rating = data["rating"]
            response = Like.objects.create(**{
                "liked_by": userid,
                "post": post,
                "rating":rating
            })

            # update the like count
            increase_like_count(data['post'])
            
            # send the notification that the post has been liked
            notification = generateRatingNotification(userid, post.postedBy)
            # print(notification)
            if notification is not None:
                if notification['sender'] == notification['revoker']:
                    return Response({"info":"self notification not allowed"})
                else:
                    Notification.objects.create(**notification)
            return Response(LikeSerializer(response).data)

class UnrateView(RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # lookup_field = "id"
    # permission_classes=[AllowAny]
    def delete(self, request, pk=None, *args, **kwargs ):
        print(pk)
        if pk:
            post = Post.objects.get(postId = pk)
            like = Like.objects.get(liked_by = request.user, post = post)
            # self.perform_destroy(like)
            like.delete()
            # decrease like count
            decrease_like_count(pk)
            return Response({'message':'deleted',"status":status.HTTP_204_NO_CONTENT})
        return Response({'message':"Unsuccessfull-not provided postId"})



class PopUpView(ListCreateAPIView):
    queryset = PopUp.objects.all()
    serializer_class = PopUpSerializer

    def post(self, request, *args, **kwargs):
        data = PopUp.objects.get(user=request.user)
        data.is_popup = False
        data.save()

        serializer = PopUpSerializer(data)
        return Response(serializer.data)

    def get(self,request):
        try:
            popup= PopUp.objects.get(user=request.user)
        except:
            popup = PopUp.objects.none()

        serializer = PopUpSerializer(popup)
        return Response(serializer.data)
    

def send_daily_progress(request):
    
    user = CustomUser.objects.all()
    context={}

    
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
    return HttpResponse('Emails sent')
        