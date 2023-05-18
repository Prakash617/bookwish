from django.contrib import admin
from django.urls import path, include

# for summernote
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    # summernote
    path('summernote/', include('django_summernote.urls')),
    #django rest auth
    # path('auth/', include('rest_auth.urls')),
    # user account urls
    path('', include('user_accounts.urls')),
    path('', include('points_and_badges.urls')),
    path('', include('library.urls')),
    path('', include('club.urls')),
    path('', include('website.urls')),
    path('', include('superuser.urls')),
    path('', include('feed.urls')),
    path('', include('notification.urls')),
    path('', include('event_app.urls')),
    path('', include('assesment.urls')),
    path('', include('my_forms.urls')),
    # path('', include('app.urls')),
    path('api-auth/', include('rest_framework.urls')),

]

# for summernote
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)