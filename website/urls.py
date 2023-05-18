"""bookwishes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


from .views import *

router = DefaultRouter()
# router.register(r'sentcheckoutmail',SentCheckoutMail,basename='sentcheckoutmail')


urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('courses', services_page, name="service_provided_page"),
    
    # event
    path('event/registrations/', event_registration, name="event-registration"),
    path('event/attendance/', event_attendance, name="event-attendance"),


    # blog
    path('blog', blog, name="blog"),
    path('blog/<int:id>/<slug:slug>', blogpost, name="blogpost"),
    # path('helpful-forms', helpful_forms, name="helpful_forms"),
    path('resources', resources, name="resources"),
    path('faqs', faqs, name="faqs"),
    path('shop', shop, name="shop"),
    path('shop/cart', cart, name='cart'),
    path('privacy-policy/', privacy_policy, name="privacy_policy" ),
    path('terms-and-conditions/', terms_and_conditions, name="terms_and_conditions" ),
    path('consultation-request/', consultation_request, name="consultation-request" ),
    path('checkoutdetail/', checkoutdetail, name="checkoutdetail" ),
    path('superuser/courses/',courses,name="course"),
    path('superuser/recommended_book/',recommended_book,name="book"),
    path('superuser/recommended_article/',recommended_article,name="article"),
    path('superuser/recommended_videos/',recommended_videos,name="video"),
    path('superuser/admin-consultation-request/',consultation_request_admin,name="admin_consultation_request"),
    path('superuser/pages/',pages,name="pages"),
    path('superuser/edit-aboutus/',edit_aboutus,name="edit_aboutus"),
    path('superuser/edit-privacy-policy/',edit_privacy_policy,name="edit_privacy_policy"),
    path('superuser/edit-terms-and-services/',edit_terms_and_services,name="edit_terms_and_services"),
    path('superuser/edit-link-and-resources/',edit_link_and_resources,name="edit_link_and_resources"),
    path('superuser/edit-consultation-request/',edit_consultation_request,name="edit_consultation_request"),
    path('superuser/edit-service-pages/',edit_service_pages,name="edit_service_pages"),
    path('superuser/media/',media,name="media"),

    
    
    # api
    path('api/',include(router.urls)),




]

