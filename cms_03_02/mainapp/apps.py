from django.apps import AppConfig
from django.db.models.signals import pre_save,post_save,post_delete


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        custome_user_model=self.get_model("UserDetail")
        #site_model = self.get_model("Site")
        device_model = self.get_model("Device")
        # device_node_model = self.get_model("devicenode")
        user_otp_model = self.get_model("UserOtp")
        # alarm_model = self.get_model("Alarm")
        
        from mainapp.signals import (add_customuser_to_user,
                                     Remove_customuser_from_user,

                                    #device_inactive_onsite,
                                    #  node_inactive_ondevice,
                                    device_topic_creation,
                                    otp_send,
                                    #  email_on_alarm
                                     )
        pre_save.connect(receiver=add_customuser_to_user, sender=custome_user_model)
        post_delete.connect(receiver=Remove_customuser_from_user, sender=custome_user_model)
        # #post_save.connect(receiver=assign_site_to_user,sender=custome_user_model)
        # post_save.connect(receiver= device_inactive_onsite, sender=site_model)
        # post_save.connect(receiver=node_inactive_ondevice, sender=device_model)
        pre_save.connect(receiver=device_topic_creation, sender=device_model)
        post_save.connect(receiver=otp_send, sender=user_otp_model)
        # post_save.connect(receiver=email_on_alarm, sender=alarm_model)
        