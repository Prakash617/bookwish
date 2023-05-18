from django.urls import path, include
# from .views import FacebookLogin
from .views import CreateCustomUserAPIView, IsSuperuser,ReLoginAPIView, CustomUserDetail, CustomUserList, LogoutCustomUserAPIView,CheckVerifyEmailView, OTPView, SendEmailView, UserChangePasswordView, VerifyEmailView, EligibilityCheck, FindAccountView, LoginAPIView

urlpatterns = [
    # path("rest-auth/facebook/", FacebookLogin.as_view(), name='fb_login'),
    path('auth/register/', CreateCustomUserAPIView.as_view(), name='auth_user_create'),
    path('auth/users/', CustomUserList.as_view(), name='user_list'),
    path('auth/users/<int:id>', CustomUserDetail.as_view(), name='user_detail'),
    path('auth/logout/', LogoutCustomUserAPIView.as_view(), name='auth_user_logout'),
    path('auth/eligibilty-check/', EligibilityCheck.as_view(), name='auth_eligibilty_check'),
    path('auth/otp/', OTPView.as_view(), name='auth_user_otp'),
    path('auth/send-email/', SendEmailView.as_view(), name='auth_send_email'),
    path('auth/verify-email/<str:token>/', VerifyEmailView, name='auth_verify_email'),
    path('auth/verify-email/check/<str:email>/', CheckVerifyEmailView.as_view(), name='check_auth_verify_email'),
    path('auth/find-account/', FindAccountView.as_view(), name='auth_find_account'),
    path('auth/login/', LoginAPIView.as_view(), name='auth_user_login'),
    path('auth/relogin/', ReLoginAPIView.as_view(), name='auth_user_relogin'),
    path('auth/is_superuser/<int:id>', IsSuperuser.as_view(), name='auth_is_superuser'),
    path('auth/changepassword/', UserChangePasswordView.as_view(), name ='changepassword')


    # for password reset
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]