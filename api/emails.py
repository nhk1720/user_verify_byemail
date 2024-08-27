from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
def send_otp_via_email(email):
    subject='Your account verification email'
    otp=random.randint(1000,9999)
    message=f'Your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    print(email_from,email)
    msg_html =None
    user_obj=User.objects.filter(email=email)
    user_obj.otp=otp
    user_obj.save()
    send_mail(subject,message,email_from,[email],html_message=msg_html)
    print('------0000000---------')
    return otp