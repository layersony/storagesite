from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decouple import config

def send_feedback(name, message, user_email):
    subject = 'New feedback from ' + name + "."
    sender = config('EMAIL_HOST_USER')

    text_content = render_to_string('email/feedback.txt',{"message": message,
    "user_email":user_email,
    "name":name})
    html_content = render_to_string('email/feedback.html',{"message": message, 
    "user_email":user_email,
    "name":name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[sender])
    msg.attach_alternative(html_content,'text/html')
    msg.send()