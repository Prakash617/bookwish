from twilio.rest import Client

from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from random import randint
from club.models import BookReading,DailyStepCount

import json

from user_accounts.models import CustomUser
from django.http import JsonResponse


def verify_phone(country_code, mobile, code=""):
    account_sid = 'ACb3d0c35b238727c51de5a6a9ff40e741'
    auth_token = 'c360c1dc061162f74942fc9ab1ab78f0'
    client = Client(account_sid, auth_token)
    if code != "":
        return {"response": "Disabled but Verify api is functional."}
    return {"response": "Disabled but OTP api is functional."}

    # receiver = '+' + str(country_code) + str(mobile)
    # if code != "":
    #     print("for verification check ", receiver, code)
    #     verification_check = client.verify \
    #                        .services('VAcc3e6dae403b4317a41f44bd37fc4d20') \
    #                        .verification_checks \
    #                        .create(to=receiver, code=code)
    #     if verification_check.status == "approved":
    #         return True
    #     return False
    
    # verification = client.verify \
    #                  .services('VAcc3e6dae403b4317a41f44bd37fc4d20') \
    #                  .verifications \
    #                  .create(to=receiver, channel='sms')
    # return verification.status

def send_verification_email(request, path, email):
    token = get_random_string(length=32)
    request.user.verify_token = token
    request.user.save()
    verify_link = path + 'email-verify/' + token
    subject, from_email, to = 'Verify Your Email', 'from@test.com', email
    html_content = render_to_string('verify_email.html', {'verify_link':verify_link, 'base_url': path, 'backend_url': path}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def validateEmailToken(request, token):
    # data = json.loads(request.body.decode('utf-8'))
    # token = data['token']
    res = {
        'status': 'success',
        'message': 'Valid',
    }
    
    if CustomUser.objects.filter(verify_token=token, email_verified=False).exists():
        tokenExists = CustomUser.objects.get(verify_token=token, email_verified=0)

        tokenExists.email_verified = True
        tokenExists.save()

    else:
        res = {
            'status': 'failed',
            'message': 'Invalid',
        }
    
    return JsonResponse(res)



def send_refer_code(refer_code, email):
    referCode = refer_code 
    subject, from_email, to = 'Verify Your Email', 'from@test.com', email
    html_content = render_to_string('user_accounts/verify_email.html', {'refer_code':referCode}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    print('msg.seng()',msg.send())
    
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_verified_token(token, email):
    code = str(token)
   
    subject, from_email, to = 'Verify Your token', 'from@test.com', email
    html_content = render_to_string('user_accounts/verify.html', {'code':code}) 
    text_content = strip_tags(html_content) 

    print(text_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def calculate_page(userid):
    books = BookReading.objects.filter(userid=userid)
    total_page = 0
    for book in books:
        page=book.end_page - book.start_page 
        total_page= total_page + page
    return total_page

def calculate_step_walked(userid):
    steps = DailyStepCount.objects.filter(userid=userid)
    step_walked = 0
    for step in steps:
       step_walked = step_walked + step.distance
    return int(step_walked * 1500)

