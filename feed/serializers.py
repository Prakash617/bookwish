from dataclasses import fields
from urllib import request
from rest_framework import serializers

from notification.models import Notification
from .models import *
from user_accounts.models import CustomUser
from notification.models import Notification
from user_accounts.serializers import CustomUserSerializer
from .utils import get_avg_rating
# from .utils import generateCommentNotification


from .utils import get_avg_rating
from rest_framework.response import Response

def generateCommentNotification(commented_by, comment_on):

    try:
        if commented_by.picture == '':
            picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
        else:
            picture = commented_by.picture
        
        print(comment_on.postId)
            
        user_obj = Post.objects.get(postId=comment_on.postId).postedBy
        # print(user_obj)
        # print("user_obj",user_obj)
        # print(picture)
        # picture = user_obj.picture
        fullName = commented_by.first_name + " " + commented_by.last_name
        notification = f"{fullName} has commented on your post."
        # print("fullName", fullName)
        data =  {
            "description": notification,
            "picture": picture,
            "revoker": user_obj,
            "sender": commented_by,
            "title": '',
            # "upload_timestamp": datetime.datetime.now(),
        }

        return data
    except:
        return None

class CommentSerializer(serializers.ModelSerializer):    
    commented_by = CustomUserSerializer(many=False, read_only=True)

    def create(self, validated_data):
        commented_by = self.context.get('request').user
        post = validated_data.pop("post") 
        post.comments_count += 1
        post.save() 

        comment = Comment.objects.create(commented_by=commented_by, post=post, **validated_data)  


        notification = generateCommentNotification(commented_by,post)
        if notification is not None:
            if notification['sender'] == notification['revoker']:
                return comment
                # return Response({"info":"self notification not allowed"})
                # raise serializers.ValidationError({"info":"self notification not allowed"})
            else:
                Notification.objects.create(**notification)
        
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'post', 'commented_by')
        read_only_fields = ('id', 'commented_by', ) 


class LikeSerializer(serializers.ModelSerializer):    
    liked_by = CustomUserSerializer(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ( 'post', 'liked_by', 'rating')
        read_only_fields = ('id',) 


class PostSerializer(serializers.ModelSerializer):    
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    def to_representation(self, instance):
        request = self.context.get('request')
        
        response = super().to_representation(instance)
        response['postedBy'] = CustomUserSerializer(instance.postedBy,context = {"request":request}).data
        
        response["likes_count"] = Like.objects.filter(post=instance).count()
        response["comments_count"] = Comment.objects.filter(post=instance).count()

        liked = Like.objects.filter(post__postId=instance.postId).filter(liked_by=self.context.get('request').user).exists()
        
        response['is_liked'] = liked
        
        total_rating_obj = Like.objects.filter(post = instance).filter(rating__gt = 0).values('rating')
        total_user = total_rating_obj.count()
        
        if total_user == 0:
            response['total_rating'] = 0.0
        else:
            total_rating = get_avg_rating(total_rating_obj,total_user)
            print(total_rating)
            response['total_rating'] = total_rating
        
        return response 

    def create(self, validated_data):
        postedBy = self.context.get('request').user
        posted_club = postedBy.club
        post = Post.objects.create(postedBy=postedBy, posted_club=posted_club, **validated_data)        
        return post

    class Meta:
        model = Post
        fields = ('modified_date','postId', 'postedBy', 'posted_club', 'comments', 'likes', 'postDescription', 'postMedia', 'postdate', 'posttime', 'likes_count', 'comments_count','is_liked')
        read_only_fields = ('postId','postedBy', 'posted_club' ) 
        
def sendStoryUploadNotifications(userid,n):
    try:
    
        if userid.picture == '':
            picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
        else:
            
            picture = userid.picture
            
        user_obj = CustomUser.objects.get(id=userid.id)
        # picture = user_obj.picture
        if n:
            notification = "You received 5 points for uploading daily Tip."
        else:
            # notification = "You have already get today daily Tip."
            return None

        return {
            "description": notification,
            "picture": picture,
            "sender": user_obj,
            "revoker": user_obj,
            "title": '',
            
        }
    except:
        return None

from datetime import date

class StorySerializer(serializers.ModelSerializer):  
    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['userid'] = CustomUserSerializer(instance.userid,context={'request': request}).data
    
        return response        

    def create(self, validated_data):
        user = self.context.get('request').user
        posted_club = user.club
        # user_id = validated_data.pop("userid")
        # print('user_id',user_id)
        
        print('val:', validated_data)
        story = Story.objects.create(userid=user, posted_club=posted_club, **validated_data)
        today = date.today()
        n = False
        
        ui = user.id
        u = CustomUser.objects.get(id = ui)
        try:
            tp = TipRecord.objects.filter(user=user , date = today ).exists()
            TipRecord.objects.create(user=user , date = today )
            if  not tp:
                u.points += 5
                tps=TipRecord.objects.get(user=user , date = today )
                tps.story_uploaded = True
                tps.save()
                u.save()
                n = True
            else:
                n= False
        except:
            print("today already updated")
        print("user.points",u.points)

        #notification 
        notification = sendStoryUploadNotifications(user,n)
        print(notification)
        if notification is not None:
            Notification.objects.create(**notification)
  
        return story

    class Meta:
        model = Story
        fields = ('id', 'userid', 'media', 'upload_timestamp', 'posted_club')
        read_only_fields = ('id', 'posted_club', 'userid') 


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ( 'post', 'liked_by', 'rating')

class PopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopUp
        fields ="__all__"