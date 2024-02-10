import email
from django.contrib.auth import get_user_model
from mainapp.models import *
from django.core.mail import EmailMultiAlternatives
#from mainapp.sms import *
#from mainapp.push_notification import *
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from cms import settings
import datetime
from datetime import datetime as date, timedelta
from pytz import timezone
import time



def add_customuser_to_user(sender, instance, *args, **kwargs):
    if instance._state.adding is True:
        user = get_user_model().objects.create_user(username=instance.username, email=instance.email, usertype=instance.usertype,
                                                    password=instance.password,contact_no=instance.contact_no)
        instance.userid = user.id  # this is used auto save UserId by userid

    else:
        auth_user = get_user_model().objects.get(id=instance.userid)
        auth_user.username = instance.username
        auth_user.email = instance.email
        auth_user.is_active = instance.is_active
        auth_user.usertype=instance.usertype
        auth_user.contact_no=instance.contact_no
        auth_user.save()

def Remove_customuser_from_user(sender, instance, *args, **kwargs):
    get_user_model().objects.filter(username=instance.username).update(is_active=False)
    inactive_user=get_user_model().objects.filter(is_active=False)
    inactive_user.delete()



def device_topic_creation(sender, instance, *args, **kwargs):
    if instance._state.adding is True:
        sit_id = instance.site_is.site_id
        topic_is = "sit" + sit_id + "/dev" + instance.device_id
        instance.topic = topic_is

    else:
        sit_id = instance.site_is.site_id
        topic_is = "sit" + sit_id + "/dev" + instance.device_id
        print(topic_is,'topic update')
        instance.topic = topic_is

def otp_send(sender, instance, *args, **kwargs):
    msg = EmailMultiAlternatives(
        # title:
        ("OTP Verification for {title}".format(
            title=instance.which_user.username)),
        # message:
        "Dear User, your otp is : "+instance.OTP,
        # email_plaintext_message,
        # from:
        "noreply@globaiot.com",
        # to:
        [instance.which_user.email])
    msg.send()
    # c_num = get_contact(instance.which_user.username)
    # if c_num is not None:
    #     if len(str(c_num)) < 11:
    #         # 9919800514,#9871295345,#gajendra.chaturvedi@denonline.in
    #         c_num = "+91" + str(c_num)

    #     sms_msg = "OTP Verification for " + instance.which_user.username + \
    #         ". Your " + " OTP is  " + str(instance.OTP)
    #     send_sms(c_num, sms_msg)

    
#