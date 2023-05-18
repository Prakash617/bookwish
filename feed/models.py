from django.utils import timezone
from django.utils.timezone import get_fixed_timezone
from datetime import timedelta
from django.db import models
# from cloudinary.models import CloudinaryField
import pytz

# from PIL import Image

kathmandu_tz = pytz.timezone('Asia/Kathmandu')
# from .utils import get_avg_rating

# Create your models here.
class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    postDescription = models.CharField(max_length=1000, blank=True, null=True)
    # postMedia = models.CharField(max_length=200, blank=True, null=True)
    postMedia = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    postdate = models.DateField(auto_now_add=True)
    posttime = models.TimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    postedBy = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="post_userid")
    posted_club = models.ForeignKey("club.Club", on_delete=models.CASCADE, blank=True, null=True, related_name="post_clubid")
    is_liked = models.BooleanField(default=False) 
    total_rating = models.FloatField(default=0.0 ,null=True, blank=True)
    modified_date = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return 'postId  '+str(self.postId)+'--'+str(self.postDescription[:12])
    
    
    # def compute_rating(self):
        
    #     total_rating_obj = Like.objects.filter(post = self).values('rating')
        
       
    #     if total_rating_obj.count() == 0 :
    #         total_user =  1
    #     else:
    #         total_user = total_rating_obj.count()
    #     total_rating = get_avg_rating(total_rating_obj,total_user)
    #     return total_rating
    
    # def save(self, *args, **kwargs):
    #     self.total_rating = self.compute_rating()
    #     super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    post =  models.ForeignKey(Post, on_delete= models.CASCADE, related_name="comments")
    commented_by = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="comment_userid")

    def __str__(self):
        return str(self.comment)
    
class Story(models.Model):
    userid = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="story_userid")
    media =  models.FileField(upload_to='story/',blank= True,null=True,max_length=200)
    upload_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    posted_club = models.ForeignKey("club.Club", on_delete=models.CASCADE, blank=True, null=True, related_name="story_clubid")
    
    
    def __str__(self):
        return str(self.userid) + '-'+str(self.media)+'-' + str(self.posted_club)

    def delete_old_stories(self):
        kathmandu_tz = pytz.timezone("Asia/Kathmandu")
        expire_date = timezone.localtime(timezone.now() - timedelta(hours=24), kathmandu_tz)
        upload_timestamp_aware = timezone.localtime(self.upload_timestamp, kathmandu_tz)
        if upload_timestamp_aware < expire_date :
            self.delete()
    
class TipRecord(models.Model):
    user = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="tiprecord_user")
    story_uploaded = models.BooleanField(default=False,null=True, blank=True)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_by = models.ForeignKey("user_accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="like_userid")
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.post) + ' -by- ' + str(self.liked_by)

class Media(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    alt = models.CharField(max_length=200,  blank=True, null=True)
    media = models.FileField(upload_to = 'medias/',blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True)

class PopUp(models.Model):
    user = models.ForeignKey("user_accounts.CustomUser",on_delete=models.CASCADE,related_name="popup")
    is_popup = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username) + "-" + str(self.is_popup)


