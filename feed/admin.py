from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
     list_display = ("postId","postDescription","postMedia", "postdate","posttime","likes_count","comments_count","postedBy","posted_club","is_liked","total_rating","modified_date")
     search_fields = ("postId","postDescription", "postdate","posttime","likes_count","comments_count","postedBy__username","posted_club__club_name","total_rating")

admin.site.register(Post, PostAdmin)

class StoryAdmin(admin.ModelAdmin):
     list_display = ("userid","media","upload_timestamp","posted_club",)
     search_fields = ("userid","posted_club__club_name",)
admin.site.register(Story, StoryAdmin)

class CommentAdmin(admin.ModelAdmin):
     list_display = ('comment','post','commented_by')
     search_fields = ('comment','post__postId','commented_by__username')
admin.site.register(Comment, CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
     list_display = ('post','liked_by','rating')
     search_fields = ('post__postId','liked_by__username','rating')
admin.site.register(Like, LikeAdmin)


admin.site.register(Media)
admin.site.register(TipRecord)
admin.site.register(PopUp)

