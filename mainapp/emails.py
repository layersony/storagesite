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

def send_welcome_email(name, user_email):
    subject = 'Welcome to StorageSite'
    sender = config('EMAIL_HOST_USER')

    text_content = render_to_string('email/welcome.txt',{   "name":name})
    html_content = render_to_string('email/welcome.html',{
    "name":name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[user_email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

def booking_email(name, user_email, unit):
    subject = 'Unit Booking Successful'
    sender = config('EMAIL_HOST_USER')

    text_content = render_to_string('email/booking.txt',{   "name":name, "unit":unit})
    html_content = render_to_string('email/booking.html',{
    "name":name, "unit":unit})

    msg = EmailMultiAlternatives(subject,text_content,sender,[user_email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

