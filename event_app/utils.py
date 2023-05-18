from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mail_event_information(email,context):
    subject, from_email, to = 'Remainder For Tommarow Events', 'from@test.com', email
    html_content = render_to_string('event/event_information.html', context) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
