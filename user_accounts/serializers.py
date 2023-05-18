from email.policy import default
from select import select
from venv import create
from rest_framework import serializers
from .models import CustomUser
from rest_framework.response import Response
# from club.serializers import ClubSerializer
from club.models import Club,Refer
from django.contrib.auth import authenticate
from .utils import random_with_N_digits, send_verified_token
from .utils import calculate_page,calculate_step_walked

class ClubSerializer(serializers.ModelSerializer):    
    
    def create(self, validated_data):
        club = Club.objects.create(**validated_data)        
        return club

    class Meta: 
        model = Club
        fields = ('club_id', 'club_name')
        read_only_fields = ('club_id', )


class CreateCustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                    style={'input_type': 'password'})
    # club = ClubSerializer(many=False)

    class Meta:
        model = CustomUser
        fields = ('id','username', 'password', 'first_name', 'last_name', 'email', 'picture', 'country_code', 'phone', 'dob', 'gender', 'location')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        print("================================")
        print('validated_data', validated_data)
        
        email = validated_data['email']
        new_club = Refer.objects.get(generated_for=email).referred_by.club
        
        refer_obj = Refer.objects.get(generated_for=email)
        
        if refer_obj.onboarded_user is None:
            # generate a token
            token = random_with_N_digits(6)
            user = super(CreateCustomUserSerializer, self).create(validated_data)   
            
            # save token to user.verify_token
            user.verify_token = token
            user.club = new_club            
            user.set_password(validated_data['password'])
            email = validated_data['email']
            
            user.save()
            
            referred_by = refer_obj.referred_by
            new_points = referred_by.points + 5
            referred_by.points = new_points
            referred_by.save()
            
            refer_obj.onboarded_user = user
            refer_obj.save()

            # send token to email or(and) phone
            send_verified_token(token = token,email=email)

            return user
        else:
            raise ValueError("Refer Code Already Used and Activated")

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    
class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class CustomUserSerializer(serializers.ModelSerializer):
    club = ClubSerializer(many=False,read_only=True, required=False)


    def to_representation(self,instance):
        context= super().to_representation(instance)
        
        try:
            context['total_pages'] = calculate_page(instance.id)
            context['step_walked'] = calculate_step_walked(instance.id)
            context["is_superuser"] = instance.is_superuser

            context["is_club_admin"] = Club.objects.filter(club_owner=instance.id).exists()
            
        except:
            pass
        
        return context


    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'picture', 'country_code', 'phone', 'dob', 'gender', 'location', 'club', 'points', 'physical_badge', 'mental_badge', 'emotional_badge', 'spiritual_badge')
        read_only_fields = ('id','club')


class OTPSerializer(serializers.Serializer):
    country_code = serializers.IntegerField()
    mobile = serializers.IntegerField()
    code = serializers.IntegerField(required=False)
    
    class Meta:
        write_only_fields = ("code",)

class EligibilitySerializer(serializers.Serializer):
    refer_code = serializers.IntegerField(required=True)
    dob = serializers.DateField()
    gender = serializers.CharField()

class FindAccountSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    country_code = serializers.IntegerField(required=False)
    phone  = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)

class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

