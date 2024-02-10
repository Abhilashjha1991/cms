from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime
# from django.core.mail import EmailMultiAlternatives
import random



class User(AbstractUser):
    #name = models.CharField(max_length=100,null=True,blank=True)
    contact_no = models.IntegerField( null=True, blank=True)
    user_type = ((0, "Admin"), (1, "Super User"), (2, "Normal User"))
    usertype = models.PositiveIntegerField(default=0, choices=user_type)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserDetail(models.Model):
    name = models.CharField(max_length=100)
    userid = models.PositiveIntegerField(null=True, blank=True)
    username=models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50)
    contact_no = models.IntegerField( null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    user_type = ((0, "Admin"), (1, "Super User"), (2, "Normal User"))
    usertype = models.PositiveIntegerField(default=0, choices=user_type)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class UserOtp(models.Model):
    OTP = models.CharField(max_length=6, null=True, blank=True)
    status = models.CharField(max_length=20, null=True,blank=True, default="PENDING")
    which_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.OTP+"  "+self.which_user.username
    
def random_id():
    res = random.randint(100000000, 999999999)
    if Site.objects.filter(site_id=str(res)):
        random_id()
    return str(res)


class Site(models.Model):
    user_is=models.ForeignKey(UserDetail,on_delete=models.CASCADE, null=True, blank=True)
    site_id = models.CharField(max_length=50, default=random_id)
    site_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True, null=True)
    # ip_address = models.GenericIPAddressField(max_length=30, default="192.168.1.1")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name


def random_id_device():
    res = random.randint(100000000, 999999999)
    if Device.objects.filter(device_id=str(res)):
        random_id_device()
    return str(res)


class Device(models.Model):
    site_is = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.CharField(max_length=50, default=random_id_device)
    device_name = models.CharField(max_length=50)
    topic = models.CharField(max_length=100, default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.device_name)


class Video(models.Model):
    # user_is=models.ForeignKey(UserDetail,on_delete=models.CASCADE, null=True, blank=True)
    device_is = models.ForeignKey(Device, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title