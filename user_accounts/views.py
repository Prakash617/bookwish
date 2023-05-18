from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from user_accounts.models import CustomUser
from club.models import Refer, Club
from .serializers import CreateCustomUserSerializer, CustomUserSerializer, OTPSerializer, EligibilitySerializer, FindAccountSerializer, ResetPasswordSerializer, LoginSerializer, UserChangePasswordSerializer
from .utils import verify_phone, send_verification_email,validateEmailToken
from django.contrib.auth.hashers import check_password
from datetime import datetime
from .models import ActiveUser
from django.shortcuts import get_object_or_404
from bookwishes.settings import ip 

from notification.models import Notification


def generateReferPointsNotification(userid, receiver, email):
    try:
        if userid.picture == '':
            picture = 'https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg' 
        else:
            picture = userid.picture
            
        user_obj = CustomUser.objects.get(id=userid.id)
        # picture = user_obj.picture
        fullName = userid.first_name + " " + userid.last_name
        notification = f"You received 5 points for refering {email}"

        return {
            "description": notification,
            "picture": picture,
            "sender": user_obj,
            "revoker": receiver,
            "title": ''
        }
    except:
        return None


# Create your views here.
class CreateCustomUserAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    permission_classes = [AllowAny]
    
    
    def create(self, request, *args, **kwargs):

        
        email = request.data.get('email')
        # print('email',email)

        
        try:
            refer_obj = Refer.objects.get(generated_for= email)
        except:
            return Response({"error":"no refer email found"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        
        user = refer_obj.referred_by
        
        
        notification = generateReferPointsNotification(user, user, serializer.instance.email)
        if notification:
            Notification.objects.create(**notification)
        return Response({**serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
      
        if Token.objects.filter(user=user).exists():
            return Response({"error": "already login in another device"}, status  = status.HTTP_401_UNAUTHORIZED )
        
        token, created = Token.objects.get_or_create(user=user)
        # ActiveUser.objects.get_or_create(activeUser = user)
        try:
            ActiveUser.objects.create(activeUser = user)
        except:
            pass
            

        return Response({"token": token.key, "user_id": user.id, "verified": user.email_verified}, status=status.HTTP_200_OK)




class ReLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(user)
      
        if Token.objects.filter(user=user).exists():
            token=Token.objects.get(user=user)
            print(token)
            try:
                token.delete()
            except:
                    
                return Response({"error": "failed to delete token"}, status  = status.HTTP_401_UNAUTHORIZED )
        
            token, created = Token.objects.get_or_create(user=user)
            try:
                ActiveUser.objects.create(activeUser = user)
            except:
                pass
            

        return Response({"token": token.key, "user_id": user.id, "verified": user.email_verified}, status=status.HTTP_200_OK)
    


class CustomUserList(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer    
    permission_classes = [AllowAny]

class CustomUserDetail(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer    
    permission_classes = [AllowAny]
    lookup_field = 'id'

class LogoutCustomUserAPIView(APIView):
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class EligibilityCheck(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = EligibilitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)             
        refer_code = serializer.validated_data["refer_code"]
        if Refer.objects.filter(refer_code=refer_code).exists():
            club_name = Refer.objects.get(refer_code=refer_code).referred_by.club.club_name
            response = {
                "response": "eligible",
                "club" : {
                        "club name": club_name
                    },
                    "dob": serializer.validated_data["dob"],
                    "gender": serializer.validated_data["gender"]
                }
            
        else:
            response = {"response": "not eligible"}
        
        return Response(response)

class OTPView(APIView):
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)             
        try:
            response_return = verify_phone(serializer.validated_data["country_code"], serializer.validated_data["mobile"], serializer.validated_data["code"])
        except:
            response_return = verify_phone(serializer.validated_data["country_code"], serializer.validated_data["mobile"])
 
        return Response(response_return)
    


class SendEmailView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)             
        email = serializer.validated_data["email"]
        send_verification_email(request, ip, email)
        print("at last", request.user.username)
        return Response({'response': "email sent"})
    

def VerifyEmailView(request, token):
    response = validateEmailToken(request, token)
    # cur_user = CustomUser.objects.get_or_404(id=request.user.id)
    # cur_user.verify_token = ''
    # cur_user.save()
    return response

class CheckVerifyEmailView(APIView):
    serializer_class = CustomUserSerializer

    def get(self, request,email=None):
        # print('email',email)
        if email is None:
            return Response({'response':'no email provided'})

        user = get_object_or_404(CustomUser,email = email)
        if user is not None:
            return Response({'email_verified':user.email_verified})
        return Response({'response':"email does not match"})

class FindAccountView(APIView):
    serializer_class = FindAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email", "null")
        country_code = serializer.validated_data.get("country_code", 0)
        phone = serializer.validated_data.get("phone", 0)
        username = serializer.validated_data.get("username", "null")        
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(phone=phone, country_code = country_code).exists():
            return Response({"status": "user found"})
        else:
            return Response({"status": "user not found"})
            

# class ResetPasswordView(UpdateAPIView):
#     serializer_class = ResetPasswordSerializer
#     model = CustomUser

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # try:
#         new_password = serializer.validated_data.get("password", "null")
#         username =  serializer.validated_data.get("username")
#         print("user", serializer.validated_data)
#         cur_user = CustomUser.objects.get(username=username)
#         cur_user.set_password(new_password)
#         # cur_user.save()
#         return Response({"status": "password succesfully reset"})
#         # except:
#         #     return Response({"status": "Error occured: pasword not reset"})


class IsSuperuser(APIView):
    def get(self, request, id=None):
        print(id)

        try:
            user = CustomUser.objects.get(id=id)
            if (Club.objects.filter(club_owner=user).exists()):
                data = {
                    "is_superuser":True
                }
            else:
                data = {
                    "is_superuser":False
                }
        except:
            data = {
                    "is_superuser":False
                }
           
        return Response(data)
    
class UserChangePasswordView(CreateAPIView):
    serializer_class =  UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        old_password = request.data['old_password']
        currentpassword= request.user.password
        password_checked =  check_password( old_password ,currentpassword)
        print('Current password')
        print("Password changed",password_checked)
        if password_checked:
            serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
            serializer.is_valid(raise_exception=True)
            return Response({'msg':'Password Changed Successfully','status': 'created' }, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'old password doesnot match', "status":'not_created'}, status=status.HTTP_401_UNAUTHORIZED)
