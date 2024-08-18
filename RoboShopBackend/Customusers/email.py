from django.core.mail import send_mail
import random
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
session_otp_store = {}


# def generate_otp():
#     return str(random.randint(10000, 99999))

def send_otp_via_mail(email, otp):
    subject = "Your account verification Code."
    otp = otp
    session_otp_store[email] = {'otp': otp, 'created_at': timezone.now(), 'user_data': {}}
    message = f"Your OTP code is {otp}. It will expire in 5 minutes."
    from_email = settings.EMAIL_HOST
    send_mail(subject, message, from_email, [email])
    print(otp)
    
    return otp