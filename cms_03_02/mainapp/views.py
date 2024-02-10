import uuid
# from django.shortcuts import render, redirect
from mainapp import models
from django.contrib.auth import authenticate, login, logout
import requests
from django.urls import reverse
from . import serializers
from django.core.serializers import serialize
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import generics
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import random
import datetime
from datetime import datetime as date, timedelta
from pytz import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from cms import settings
import cv2
import os



@api_view(['POST'])
def login_user(request):
    print("hello world")
    #try:
    if request.method == "POST":
        password=request.data["password"]
        if "username" in request.data.keys():
            print('hello')
            user=models.User.objects.get(username=request.data["username"])
            user_obj=models.UserDetail.objects.get(username=request.data["username"])
            if user_obj is not None:
                if (request.data["username"]==user_obj.username) and (password==user_obj.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'usertype': user.usertype
                    })
        elif "contact" in request.data.keys():
            user=models.User.objects.get(contact_no=request.data["contact"])
            user_obj=models.UserDetail.objects.get(contact_no=request.data["contact"])
            if user_obj is not None:
                if (int(request.data["contact"])==user_obj.contact_no) and (password==user_obj.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'usertype': user.usertype
                    })

        else:
            print(user.errors, '*****')

def get_user_from_token(token):
    tmpT = token.split(" ")[1]
    user_obj = Token.objects.get(key=tmpT.strip()).user
    return user_obj

@api_view(['GET'])
def user_detail(request):
    if request.method=='GET':
        valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
        try:
            queryset=models.UserDetail.objects.filter(userid=valid_user.id)
            if not queryset.exists():
                raise ObjectDoesNotExist()
        except ObjectDoesNotExist:
            return Response({"message": "No User Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserListSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


def generate_otp():
    res = random.randint(100000, 999999)
    otp_object = models.UserOtp.objects.filter(OTP=str(res))
    if not otp_object.exists():
        return str(res)


@api_view(['POST'])
def create_otp(request):
    if request.method == 'POST':
        new_otp = generate_otp()
        user_obj = models.User.objects.filter(
            username=request.data['username'], email=request.data['email'])
        if user_obj:
            otp_obj = models.UserOtp.objects.filter(which_user__username=request.data['username'],
                                                     which_user__email=request.data['email'])
            if otp_obj:
                otp_obj.delete()
            print(user_obj[0],'************')
            models.UserOtp.objects.create(OTP=new_otp, which_user=user_obj[0])
            print('hello')
            return Response({"message": "OTP Created"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Otp_verification(request):
    if request.method == 'POST':
        otp_obj = models.UserOtp.objects.filter(OTP=request.data['OTP'])
        print(otp_obj, 'otp found')
        if otp_obj:
            otp_obj.update(status='VERIFIED')
            return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"status": "Enter correct OTP"})

@api_view(['PUT'])
def forget_password(request):
    user_obj = models.User.objects.get(username=request.data['username'])
    if request.method == "PUT":
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            try:
                custom_obj = models.UserDetail.objects.get(username=request.data['username'])
                if custom_obj:
                    custom_obj.password = serializer.data.get("new_password")
                    custom_obj.save()
            except:
                return Response({"message": "No CustomUser Found"}, status=status.HTTP_404_NOT_FOUND)
            otp_obj = models.UserOtp.objects.filter(
                which_user__username=request.data['username'])
            if otp_obj:
                otp_obj.delete()
            return Response({"message": "New Password Created Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_password(request):
    user_obj = request.user
    if request.method == "PUT":
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            # print(old_password, 'old password')
            if not user_obj.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            try:
                custom_obj = models.UserDetail.objects.get(username=request.user.username)
                if custom_obj:
                    custom_obj.password = serializer.data.get("new_password")
                    custom_obj.save()
            except:
                return Response({"message": "No CustomUser Found"}, status=status.HTTP_404_NOT_FOUND)

            token = Token.objects.get(user=user_obj)
            token.delete()
            Token.objects.create(user=user_obj)

            return Response({"message": "Password Updated Successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def site_by_user(request):
    print('hello')
    if request.method == "GET":
        valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
        #if valid_user.UserType == 1 or valid_user.UserType == 2 or valid_user.UserType == 3 or valid_user.UserType == 4:
        try:
            dev_obj = models.Site.objects.filter(user_is__username=valid_user.username)
            if not dev_obj.exists():
                raise ObjectDoesNotExist()
        except ObjectDoesNotExist:
            return Response({"message": "No Site Found "}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.SiteSerializer(dev_obj, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def device_from_siteid(request):
    if request.method == 'GET':
        valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
        if valid_user:
            try:
                dev_obj = models.Device.objects.filter(site_is__site_id=request.GET['site_id'])
                if not dev_obj.exists():
                    raise ObjectDoesNotExist()
            except ObjectDoesNotExist:
                return Response({"message": "No Device Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.DeviceSerializer(dev_obj, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return Response({"message": "Unauthorized User"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET','POST'])
def get_upload_video(request):
    if request.method=='GET':
        valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
        if valid_user:
            try:
                print(request.GET['device_id'])
                video_obj=models.Video.objects.filter(device_is__device_id=request.GET['device_id'])
                print(video_obj,"********")
                if not video_obj.exists():
                    raise ObjectDoesNotExist()
            except ObjectDoesNotExist:
                return Response({"message": "No Device Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.VideoSerializer(video_obj, many=True)
            return JsonResponse(serializer.data, safe=False)

        
    elif request.method == 'POST':
        device_obj=models.Device.objects.get(device_id=request.data['device_id'])
        if device_obj:
            video=models.Video.objects.create(device_is=device_obj,
                                              title=request.data['title'],
                                              video=request.data['video_file'])
            # print(video.video.path,'***********')
            # Process the video file (e.g., capture screenshots)
            # process_video(video.video.path)

            return Response({"message": "Video Uploaded Successfully"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# def process_video(video_path):
#     print('helo')
#     # Use OpenCV to capture screenshots from the video
#     cap = cv2.VideoCapture(video_path)
#     print(cap,'Hiiiiii')
#     # Create a directory to save screenshots
#     screenshot_dir = os.path.join(os.path.dirname(video_path), 'screenshots')
#     os.makedirs(screenshot_dir, exist_ok=True)

#     # Capture screenshots at regular intervals
#     frame_count = 0
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_count % 30 == 0:  # Capture every 30 frames (adjust as needed)
#             screenshot_path = os.path.join(screenshot_dir, f'screenshot_{frame_count}.png')
#             print(screenshot_path,'*&&&&&&&&&&&&&')
#             cv2.imwrite(screenshot_path, frame)

#         frame_count += 1

#     cap.release()






# @api_view(['GET', 'POST'])
# def ev_by_user(request):
#     if request.method == "GET":
#         valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
#         if valid_user:
#         #if valid_user.UserType == 1 or valid_user.UserType == 2 or valid_user.UserType == 3 or valid_user.UserType == 4:
#             try:
#                 ev_obj = models.ElectricVehicle.objects.filter(user_is__username=valid_user.username)
#                 if not ev_obj.exists():
#                     raise ObjectDoesNotExist()
#             except ObjectDoesNotExist:
#                 return Response({"message": "No Site Found "}, status=status.HTTP_404_NOT_FOUND)

#         serializer = serializers.EvSerializer(ev_obj, many=True)
#         return JsonResponse(serializer.data, safe=False)


# @api_view(['GET', 'POST'])
# def device_by_user(request):
#     if request.method == "GET":
#         valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
#         #if valid_user.UserType == 1 or valid_user.UserType == 2 or valid_user.UserType == 3 or valid_user.UserType == 4:
#         try:
#             dev_obj = models.Device.objects.filter(vehicle_is__user_is__username=valid_user.username)
#             if not dev_obj.exists():
#                 raise ObjectDoesNotExist()
#         except ObjectDoesNotExist:
#             return Response({"message": "No Devices Found "}, status=status.HTTP_404_NOT_FOUND)

#         serializer = serializers.DeviceSerializer(dev_obj, many=True)
#         return JsonResponse(serializer.data, safe=False)


# @api_view(['GET'])
# def device_by_ev(request):
#     if request.method == 'GET':
#         valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
#         if valid_user:
#             try:
#                 dev_obj = models.Device.objects.filter(vehicle_is__vehicle_id=request.GET['ev_id'])
#                 if not dev_obj.exists():
#                     raise ObjectDoesNotExist()
#             except ObjectDoesNotExist:
#                 return Response({"message": "No Device Found"}, status=status.HTTP_404_NOT_FOUND)

#             serializer = serializers.DeviceSerializer(dev_obj, many=True)
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             return Response({"message": "Unauthorized User"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def node_by_ev(request):
#     if request.method == 'GET':
#         valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
#         if valid_user:
#             try:
#                 nod_obj = models.DeviceNode.objects.filter(device_is__vehicle_is__vehicle_id=request.GET['ev_id'])
#                 if not nod_obj.exists():
#                     raise ObjectDoesNotExist()
#             except ObjectDoesNotExist:
#                 return Response({"message": "No Node Found"}, status=status.HTTP_404_NOT_FOUND)

#             serializer = serializers.DeviceNodeSerializer(nod_obj, many=True)
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             return Response({"message": "Unauthorized User"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def node_by_device(request):
#     if request.method == 'GET':
#         valid_user = get_user_from_token(request.META['HTTP_AUTHORIZATION'])
#         if valid_user:
#             try:
#                 nod_obj = models.DeviceNode.objects.filter(device_is__device_id=request.GET['device_id'])
#                 if not nod_obj.exists():
#                     raise ObjectDoesNotExist()
#             except ObjectDoesNotExist:
#                 return Response({"message": "No Node Found"}, status=status.HTTP_404_NOT_FOUND)

#             serializer = serializers.DeviceNodeSerializer(nod_obj, many=True)
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             return Response({"message": "Unauthorized User"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET', 'POST'])
# def alarm_history(request):
#     if request.method == 'GET':
#         start_date = request.GET['start_date']
#         end_date = request.GET['end_date']
#         start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
#         end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

#         if "start_date" in request.GET.keys() and "end_date" in request.GET.keys() and \
#             "node_type" in request.GET.keys() and "ev_id" in request.GET.keys():
#             ev_id = request.GET['ev_id']
#             device_id = request.GET['device_id']
#             #if site_id != 'all_site':
#             dev_obj = models.Device.objects.filter(vehicle_is__vehicle_id=ev_id,
#                                                     device_id=device_id)
#             for dev in dev_obj:
#                 try:
#                     queryset = models.AlarmHistory.objects.filter(alarm_is__device_is__device_id=dev.device_id,
#                                                                 alarm_is__node_type=request.GET['node_type'],
#                                                                 created_on__range=(start_date_obj, end_date_obj))
                        
#                     if not queryset.exists():
#                         raise ObjectDoesNotExist()
#                 except ObjectDoesNotExist:
#                     return Response({"message": "No Data Found"}, status=status.HTTP_404_NOT_FOUND)

#                 li = []
#                 count = 0
#                 for i in range(0, len(queryset)):
#                     if int(queryset[i].alarm_is.node_type) == 401 or int(queryset[i].alarm_is.node_type) == 402 or int(queryset[i].alarm_is.node_type) == 403 or int(queryset[i].alarm_is.node_type) == 404 or int(queryset[i].alarm_is.node_type) == 406 or int(queryset[i].alarm_is.node_type) == 407 :
#                         if queryset[i].is_active == True and i >= count: #if need to run else condition please change 1 to 0 in current line after ==
#                             for j in range(i + 1, len(queryset)):
#                                 if queryset[i].is_active == queryset[j].is_active:
#                                     continue
#                                 else:
#                                     li.append(str(i) + "_" + str(j))
#                                     count = j
#                                     break
                    

#                 x = []
#                 for i in li:
#                     false_obj = queryset[int(i.split("_")[0])]
#                     true_obj = queryset[int(i.split("_")[1])]
#                     start_date_st = false_obj.created_on.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
#                     end_date_st = true_obj.created_on.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
#                     time_diff = (datetime.datetime.strptime(end_date_st, "%Y-%m-%d %H:%M:%S") -
#                                     datetime.datetime.strptime(start_date_st, "%Y-%m-%d %H:%M:%S"))
#                     a = {"start_time": start_date_st,"end_time":end_date_st,"duration":str(time_diff)+' minutes',
#                         'Vehicle_id':queryset[0].vehicle_is.vehicle_id,'node_type':queryset[0].alarm_is.node_is.get_node_type_display() }
#                     x.append(a)
                
#                 return Response(x,status=status.HTTP_200_OK)


