from rest_framework import serializers
from mainapp import models
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
import datetime
from datetime import date,timedelta
from pytz import timezone

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value 

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        #print ("value "+value)
        validate_password(value)
        return value  



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDetail
        fields = ('id','name','userid','username','password','email','contact_no','address','usertype','is_active','created_on')

    usertype = serializers.SerializerMethodField('get_usertype_type')
    

    def get_usertype_type(self, obj):
        return str(obj.get_usertype_display())


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site
        fields = ('id','user_is','site_id', 'site_name','address','is_active')

    user_is = serializers.SerializerMethodField('get_user_name')
    #site_type = serializers.SerializerMethodField('get_site_type_name')

    def get_user_name(self, obj):
        return str(obj.user_is.name)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ('id', 'site_is', 'device_id', 'device_name', 'topic', 'is_active')

    site_is = serializers.SerializerMethodField('get_site_name')

    def get_site_name(self, obj):
        return str(obj.site_is.site_name)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ['id','device_is' ,'device_id','title', 'video','created_on']

    device_is = serializers.SerializerMethodField('get_device_name')
    device_id = serializers.SerializerMethodField('get_deviceid')
    created_on=serializers.SerializerMethodField()

    def get_device_name(self, obj):
        return str(obj.device_is.device_name)

    def get_deviceid(self, obj):
        return obj.device_is.device_id
    
    def get_created_on(self,obj):
        return obj.created_on.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")


# class EvSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ElectricVehicle
#         fields = ('id','user_is','vehicle_id','vehicle_type','created_on','Total_Alarm','Active_Alarm','total_alarm_report','active_alarm_report') #,'total_alarm_report','active_alarm_report'

#     user_is = serializers.SerializerMethodField('get_user_name')
#     vehicle_type=serializers.SerializerMethodField()
#     created_on=serializers.SerializerMethodField()
#     Total_Alarm = serializers.SerializerMethodField()
#     Active_Alarm = serializers.SerializerMethodField()
#     total_alarm_report = serializers.SerializerMethodField()
#     active_alarm_report = serializers.SerializerMethodField()
#     #site_type = serializers.SerializerMethodField('get_site_type_name')

#     def get_user_name(self, obj):
#         return str(obj.user_is.name)
    
#     def get_vehicle_type(self, obj):
#         return str(obj.get_vehicle_type_display())
    
#     def get_created_on(self,obj):
#         return obj.created_on.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

    
#     def get_Total_Alarm(self,obj):
#         total_alarm=[]
#         #for x in obj:
#         alarm_obj=models.Alarm.objects.filter(vehicle_is=obj)
#         for data in alarm_obj:
#             total_alarm.append(data)
        
#         if len(total_alarm)>0:
#             return len(total_alarm)
#         else:
#             return 0

#     def get_Active_Alarm(self,obj):
#         total_alarm = []
#         #for x in obj:
#         alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,is_active=True)
#         for almmm in alarm_obj:
#             total_alarm.append(almmm)
#         if len(total_alarm) > 0:
#             return len(total_alarm)
#         else:
#             return 0

#     def get_total_alarm_report(self,obj):
#         alrm_list_daily=[]
#         alrm_list_weekly = []
#         alrm_list_monthly = []
#         yesterday = date.today() - timedelta(days=1)
#         weekly=date.today() - timedelta(days=7)
#         monthly=date.today() - timedelta(days=30)
#         #for x in obj:
#         if yesterday:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=yesterday)
#             if alarm_obj:
#                 for xx in alarm_obj:
#                     alrm_list_daily.append(xx)
#         if weekly:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=weekly)
#             if alarm_obj:
#                 for y in alarm_obj:
#                     alrm_list_weekly.append(y)
#         if monthly:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=monthly)
#             if alarm_obj:
#                 for z in alarm_obj:
#                     alrm_list_monthly.append(z)

#         if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
#             return {'daily':len(alrm_list_daily),
#                     'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
#         else:
#             return 0

#     def get_active_alarm_report(self,obj):
#         alrm_list_daily=[]
#         alrm_list_weekly = []
#         alrm_list_monthly = []
#         yesterday = date.today() - timedelta(days=1)
#         weekly=date.today() - timedelta(days=7)
#         monthly=date.today() - timedelta(days=30)
#         #for x in obj:
#         if yesterday:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=yesterday,is_active=True)
#             if alarm_obj:
#                 for xx in alarm_obj:
#                     alrm_list_daily.append(xx)
#         if weekly:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=weekly,is_active=True)
#             if alarm_obj:
#                 for y in alarm_obj:
#                     alrm_list_weekly.append(y)
#         if monthly:
#             alarm_obj=models.Alarm.objects.filter(vehicle_is=obj,his_datetime__gte=monthly,is_active=True)
#             if alarm_obj:
#                 for z in alarm_obj:
#                     alrm_list_monthly.append(z)

#         if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
#             return {'daily':len(alrm_list_daily),'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
#         else:
#             return 0

# class DeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Device
#         fields = ('id', 'vehicle_is', 'device_id', 'device_name', 'topic', 'is_active', 'created_on')

#     vehicle_is = serializers.SerializerMethodField('get_vehicle')

#     def get_vehicle(self, obj):
#         return str(obj.vehicle_is.vehicle_id)

# class DeviceNodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.DeviceNode
#         fields = ('id', 'device_is','device_id' ,'node_id', 'node_name', 'node_value','node_type','is_active','modified_on','Image_State','Total_Alarm','Active_Alarm','total_alarm_report','active_alarm_report')

#     device_is = serializers.SerializerMethodField('get_device_name')
#     device_id = serializers.SerializerMethodField('get_deviceid')
#     modified_on=serializers.SerializerMethodField()
#     Total_Alarm = serializers.SerializerMethodField()
#     Active_Alarm = serializers.SerializerMethodField()
#     total_alarm_report = serializers.SerializerMethodField()
#     active_alarm_report = serializers.SerializerMethodField()
#     #node_value=serializers.SerializerMethodField()

#     def get_device_name(self, obj):
#         return str(obj.device_is.device_name)

#     def get_deviceid(self, obj):
#         return obj.device_is.device_id
    
#     def get_modified_on(self,obj):
#         return obj.modified_on.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

#     def get_Total_Alarm(self,obj):
#         total_alarm=[]
#         #for x in obj:
#         alarm_obj=models.Alarm.objects.filter(node_is=obj)
#         for data in alarm_obj:
#             total_alarm.append(data)
        
#         if len(total_alarm)>0:
#             return len(total_alarm)
#         else:
#             return 0

#     def get_Active_Alarm(self,obj):
#         total_alarm = []
#         #for x in obj:
#         alarm_obj=models.Alarm.objects.filter(node_is=obj,is_active=True)
#         for almmm in alarm_obj:
#             total_alarm.append(almmm)
#         if len(total_alarm) > 0:
#             return len(total_alarm)
#         else:
#             return 0

#     def get_total_alarm_report(self,obj):
#         alrm_list_daily=[]
#         alrm_list_weekly = []
#         alrm_list_monthly = []
#         yesterday = date.today() - timedelta(days=1)
#         weekly=date.today() - timedelta(days=7)
#         monthly=date.today() - timedelta(days=30)
#         #for x in obj:
#         if yesterday:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=yesterday)
#             if alarm_obj:
#                 for xx in alarm_obj:
#                     alrm_list_daily.append(xx)
#         if weekly:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=weekly)
#             if alarm_obj:
#                 for y in alarm_obj:
#                     alrm_list_weekly.append(y)
#         if monthly:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=monthly)
#             if alarm_obj:
#                 for z in alarm_obj:
#                     alrm_list_monthly.append(z)

#         if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
#             return {'daily':len(alrm_list_daily),
#                     'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
#         else:
#             return 0

#     def get_active_alarm_report(self,obj):
#         alrm_list_daily=[]
#         alrm_list_weekly = []
#         alrm_list_monthly = []
#         yesterday = date.today() - timedelta(days=1)
#         weekly=date.today() - timedelta(days=7)
#         monthly=date.today() - timedelta(days=30)
#         #for x in obj:
#         if yesterday:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=yesterday,is_active=True)
#             if alarm_obj:
#                 for xx in alarm_obj:
#                     alrm_list_daily.append(xx)
#         if weekly:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=weekly,is_active=True)
#             if alarm_obj:
#                 for y in alarm_obj:
#                     alrm_list_weekly.append(y)
#         if monthly:
#             alarm_obj=models.Alarm.objects.filter(node_is=obj,his_datetime__gte=monthly,is_active=True)
#             if alarm_obj:
#                 for z in alarm_obj:
#                     alrm_list_monthly.append(z)

#         if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
#             return {'daily':len(alrm_list_daily),'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
#         else:
#             return 0

# class NewDeviceNodeSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = models.DeviceNode
    #     fields = ('id','node_type', 'Total_Alarm','Active_Alarm','total_alarm_report','active_alarm_report')

    # node_type = serializers.SerializerMethodField()
    # Total_Alarm = serializers.SerializerMethodField()
    # Active_Alarm = serializers.SerializerMethodField()
    # total_alarm_report = serializers.SerializerMethodField()
    # active_alarm_report = serializers.SerializerMethodField()

    # def get_node_type(self,obj):
    #     for x in obj:
    #         return x.get_node_type_display()


    # def get_Total_Alarm(self,obj):
    #     total_alarm=[]
    #     for x in obj:
    #         alarm_obj=models.Alarm.objects.filter(node_is=x)
    #         for data in alarm_obj:
    #             total_alarm.append(data)
        
    #     if len(total_alarm)>0:
    #         return len(total_alarm)
    #     else:
    #         return 0

    # def get_Active_Alarm(self,obj):
    #     total_alarm = []
    #     for x in obj:
    #         alarm_obj=models.Alarm.objects.filter(node_is=x,is_active=True)
    #         for almmm in alarm_obj:
    #             total_alarm.append(almmm)
    #     if len(total_alarm) > 0:
    #         return len(total_alarm)
    #     else:
    #         return 0

    # def get_total_alarm_report(self,obj):
    #     alrm_list_daily=[]
    #     alrm_list_weekly = []
    #     alrm_list_monthly = []
    #     yesterday = date.today() - timedelta(days=1)
    #     weekly=date.today() - timedelta(days=7)
    #     monthly=date.today() - timedelta(days=30)
    #     for x in obj:
    #         if yesterday:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=yesterday)
    #             if alarm_obj:
    #                 for xx in alarm_obj:
    #                     alrm_list_daily.append(xx)
    #         if weekly:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=weekly)
    #             if alarm_obj:
    #                 for y in alarm_obj:
    #                     alrm_list_weekly.append(y)
    #         if monthly:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=monthly)
    #             if alarm_obj:
    #                 for z in alarm_obj:
    #                     alrm_list_monthly.append(z)

    #     if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
    #         return {'daily':len(alrm_list_daily),
    #                 'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
    #     else:
    #         return 0

    # def get_active_alarm_report(self,obj):
    #     alrm_list_daily=[]
    #     alrm_list_weekly = []
    #     alrm_list_monthly = []
    #     yesterday = date.today() - timedelta(days=1)
    #     weekly=date.today() - timedelta(days=7)
    #     monthly=date.today() - timedelta(days=30)
    #     for x in obj:
    #         if yesterday:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=yesterday,is_active=True)
    #             if alarm_obj:
    #                 for xx in alarm_obj:
    #                     alrm_list_daily.append(xx)
    #         if weekly:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=weekly,is_active=True)
    #             if alarm_obj:
    #                 for y in alarm_obj:
    #                     alrm_list_weekly.append(y)
    #         if monthly:
    #             alarm_obj=models.Alarm.objects.filter(node_is=x,his_datetime__gte=monthly,is_active=True)
    #             if alarm_obj:
    #                 for z in alarm_obj:
    #                     alrm_list_monthly.append(z)

    #     if len(alrm_list_daily)>0 or len(alrm_list_weekly)>0 or len(alrm_list_monthly)>0:
    #         return {'daily':len(alrm_list_daily),'weekly':len(alrm_list_weekly),'monthly':len(alrm_list_monthly)}
    #     else:
    #         return 0




