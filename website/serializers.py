from dataclasses import fields
from rest_framework import serializers
from .models import *
from user_accounts.models import CustomUser
from user_accounts.serializers import CustomUserSerializer


class TestimonialsSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = Testimonials
        fields = ('id', 'picture', 'intro', 'name', 'message')
        read_only_fields = ('id') 
        

class BasicInfoSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = BasicInfo
        fields = ('id', 'founder_name', 'founder_image', 'founder_bio', 'founder_story', 'about_us', 'about_mission', 'about_vision', 'contact_phone1', 'contact_phone2', 'contact_address')
        read_only_fields = ('id') 


class BookingsSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = Bookings
        fields = ('id', 'booking_date', 'attendee_name', 'attendee_address', 'ateendee_contact', 'start_time', 'end_time')
        read_only_fields = ('id') 
        

class ShopSerializer(serializers.ModelSerializer):    
   
    class Meta:
        model = Shop
        fields = ('id', 'product_name', 'product_description', 'product_price', 'product_photos')
        read_only_fields = ('id') 


class BlogSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Shop
        fields = ('id', 'article_title', 'article_body', 'post_date')
        read_only_fields = ('id') 
        
class OrderSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Shop
        fields = '__all__'
