from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from random import randint
from bookwishes.settings import DEBUG

def send_order_email(email, order_items, address):
    print("sending email")
    summary  = order_items.pop()
    
    
    subject, from_email, to = 'Your Order Has Been Placed', "thebookwishesclub@gmail.com", email
    html_content = render_to_string('website/checkout_mail/order.html', {'order_items':order_items,'summary':summary, "address": address}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    print(subject, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
  

def send_consultation_request_email(consultation):
    subject, from_email, to = 'Your consultation request has been received.', 'thebookwishesclub@gmail.com', consultation['email']
    html_content = render_to_string('website/consultation_mail.html', {'consultation':consultation}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
   
   

