
from django.contrib import admin
from django.urls import path, include
from .views import(
    delete_commentReport,
    delete_order,
    delete_notification,
   delete_postReport,
   delete_blogstory,
   commentReport_admin,
   delete_story_report,
   postReport_admin,
    set_order_complete,
   storyReport_admin,
   superuser,
   superuser_settings,
   testimonial_admin,
   delete_testimonial,
   shop_admin,
   delete_product,
   common_questions_admin,
   delete_common_question,
   home_resources_admin,
   delete_home_resources_item,
   refer_user,

   blogpost_admin,
   create_blog_admin,
   edit_socials,
  
   website_traffic,
   website_analytics,
   shop_data,
   bookwishes_communities,
   user_management,
   notifications_admin,
   upload_a_feed,
   edit_blogpost,
   delete_blogpost,

   superuser_login,
   superuser_logout,
   delete_post,
   delete_media,
   add_event,
   delete_event
)

# app_name = "superuser"

urlpatterns = [
    path('superuser', superuser, name="superuser"),

    path('superuser/settings', superuser_settings, name="superuser_settings"),

    path('superuser/testimonials', testimonial_admin, name="testimonial_admin"),
    path('superuser/testimonials/<int:id>/delete', delete_testimonial, name="delete_testimonial"),

    path('superuser/shop', shop_admin, name="shop_admin"),
    path('superuser/shop/<int:id>/delete', delete_product, name="delete_product"),

    path('superuser/common-questions', common_questions_admin, name="common_questions_admin"),
    path('superuser/common_questions/<int:id>/delete', delete_common_question, name="delete_common_question"),

    path('superuser/resources', home_resources_admin, name="home_resources_admin"),
    path('superuser/resources/<int:id>/delete', delete_home_resources_item, name="delete_home_resources_item"),

    path('superuser/post', blogpost_admin, name="blogpost_admin"),
    
    path('superuser/post_report', postReport_admin, name="post_report"),
    path('superuser/story_report', storyReport_admin, name="story_report"),
    path('superuser/comment_report', commentReport_admin, name="comment_report"),
    
    path('superuser/create_post', create_blog_admin, name="create_blogpost"),
    path('superuser/edit_blogpost/<int:b_id>', edit_blogpost, name='edit_blogpost'),
    path('superuser/delete_blogpost/<int:b_id>', delete_blogpost, name='delete_blogpost'),
    path('superuser/delete_order/<int:b_id>', delete_order, name='delete_order'),
    path('superuser/set_order_complete/<int:b_id>', set_order_complete, name='set_order_complete'),
    path('superuser/delete_story_report/<int:b_id>', delete_story_report, name='delete_story_report'),
    path('superuser/delete_post/<int:b_id>', delete_post, name='delete_post'),
    path('superuser/delete_media/<int:b_id>', delete_media, name='delete_media'),
    path('superuser/delete_notification/<int:b_id>', delete_notification, name='delete_notification'),
    path('superuser/delete_postReport/<int:b_id>', delete_postReport, name='delete_postReport'),
    path('superuser/delete_commentReport/<int:b_id>', delete_commentReport, name='delete_commentReport'),
    path('superuser/edit_socials', edit_socials, name='edit_socials'),


    path('superuser/login', superuser_login, name="login"),
    path('superuser/logout', superuser_logout, name="logout"),

    


    # website traffic page
    path('superuser/website-traffic',website_traffic, name="website-traffic"),

    # website analytics page
    path('superuser/website-analytics', website_analytics, name="website-analytics"),

    # merchandise shop data page
    path('superuser/shop-data', shop_data, name="shop-data"),

    # communities statistics page
    path('superuser/communities', bookwishes_communities, name="bookwishes-communities"),

    # user management page
    path('superuser/user-management', user_management, name="user-management"),

    # refer a single or multiple users
    path('superuser/refer-user', refer_user, name="refer-user"),

    # notifications admin page
    path('superuser/notifications-admin', notifications_admin, name="notifications-admin"),

    #  upload a feed
    path('superuser/upload-a-feed', upload_a_feed, name="upload-a-feed"),

    # add events
    path('superuser/add_event/', add_event, name='add_event'),
    path('superuser/delete_event/<int:event_id>/', delete_event, name='delete_event'),
   
    
]