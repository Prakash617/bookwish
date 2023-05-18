from django.urls import path
from .views import UnrateView, RateView, StoryView, StoryDetailView, PostView, PostDetailView, CommentView, CommentDetailView, LikeView, LikeDetailView, MyPostView,PopUpView, send_daily_progress


urlpatterns = [
    path('api/story/', StoryView.as_view(), name='api-story'),
    path('api/story/detail/<int:id>', StoryDetailView.as_view(), name='api-story-detail'),

    path('api/post/', PostView.as_view(), name='api-post'),
    path('api/post/detail/<int:pk>', PostDetailView.as_view(), name='api-post-detail'),
    path('api/mypost/', MyPostView.as_view(), name='api-mypost'),

    path('api/comment/', CommentView.as_view(), name='api-comment'),
    path('api/comment/detail/<int:id>/', CommentDetailView.as_view(), name='api-comment-detail'),

    path('api/like/', LikeView.as_view(), name='api-like'),
    path('api/like/detail/<int:id>', LikeDetailView.as_view(), name='api-like-detail'),
    
    path('api/rating/', RateView.as_view(), name='api-rate'),
    path('api/unrating/<int:pk>', UnrateView.as_view(), name='api-unrate'),
    path('api/popup/', PopUpView.as_view(), name='api-unrate'),
    path('send_mail/', send_daily_progress, name='send_mail'),
    
    

]