#from import_export.admin import ImportExportModelAdmin
#from import_export import resources
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.site_header = "ADMIN: Electric Vehicle"

class UserModelAdmin(UserAdmin):
    list_display = ['id','username','email','usertype','is_active']
    ordering = ("-id",)


class UserDetailAdmin(admin.ModelAdmin):
    list_display=('id','name','userid','username','password','email','contact_no','address','usertype','is_active','created_on')
    search_fields = ('name','username','email','contact_no','address','usertype','is_active')


class SiteAdmin(admin.ModelAdmin):
    list_display=('id','user_is','site_id','site_name','address','is_active','created_on')
    search_fields = ('user_is__name', 'site_id', 'site_name', 'address')
    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['customuser_is'].queryset = CustomUser.objects.filter(UserType=4)
    #     return super(SiteAdmin, self).render_change_form(request, context, *args, **kwargs)

class DeviceAdmin(admin.ModelAdmin):
    list_display=('id','site_is','device_id','device_name','topic','is_active','created_on')


class VideoAdmin(admin.ModelAdmin):
    list_display=('id','device_is','title','video','created_on')


# class ElectricVehicleAdmin(admin.ModelAdmin):
#     list_display=('id','user_is','vehicle_id','vehicle_type','created_on')
#     search_fields = ('user_is__name', 'vehicle_id','vehicle_type')
#     # def render_change_form(self, request, context, *args, **kwargs):
#     #     context['adminform'].form.fields['customuser_is'].queryset = CustomUser.objects.filter(UserType=4)
#     #     return super(SiteAdmin, self).render_change_form(request, context, *args, **kwargs)

# class DeviceAdmin(admin.ModelAdmin):
#     list_display=('id','vehicle_is','device_id','device_name','topic','is_active','created_on')


# class DeviceNodeAdmin(admin.ModelAdmin):
#     list_display=('id','device_is','node_id','node_name','node_value','node_type','is_active','created_on','modified_on','Image_State')
#     search_fields = ('device_is__device_name','device_is__device_id')
#     readonly_fields=('created_on',)

# class AlarmAdmin(admin.ModelAdmin):
#     list_display=('id','vehicle_is','device_is','node_is','node_type','node_value','topic','his_datetime','is_active')
#     readonly_fields=('his_datetime',)


# class AlarmHistoryAdmin(admin.ModelAdmin):
#     list_display=('id','vehicle_is','alarm_is','created_on','resolved_on','is_active')
#     readonly_fields=('created_on','resolved_on')


admin.site.register(User,UserModelAdmin)
admin.site.register(UserDetail,UserDetailAdmin)
admin.site.register(Site,SiteAdmin)
admin.site.register(Device,DeviceAdmin)

# admin.site.register(ElectricVehicle,ElectricVehicleAdmin)
# admin.site.register(Device,DeviceAdmin)
# admin.site.register(DeviceNode,DeviceNodeAdmin)
# admin.site.register(Alarm,AlarmAdmin)
admin.site.register(UserOtp)
admin.site.register(Video,VideoAdmin)
# admin.site.register(AlarmHistory,AlarmHistoryAdmin)