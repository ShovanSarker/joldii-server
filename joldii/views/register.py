from __future__ import unicode_literals

from django.views import View

from django.http import HttpResponse

from joldii.constants import consts
from joldii.models import DriverModel
from joldii.models import UserModel
from joldii.responses import response_0003_register


class Register(View):
    @staticmethod
    def post(request):
        print request.POST
        optional = True
        type = None
        try:
            phone = request.POST[consts.PARAM_PHONE]
            name = request.POST[consts.PARAM_USER_NAME]
            email = request.POST[consts.PARAM_USER_MAIL]
            password = request.POST[consts.PARAM_PASSWORD]
            type = request.POST[consts.PARAM_USER_TYPE]


        except:
            print ("Parameter Exception")

        try:
            profile_pic = request.POST[consts.PARAM_USER_PIC]

        except:
            print ("Optional Parameter Exception")
        try:
            driving_license = request.POST[consts.PARAM_DRIVER_LICENSE]
        except:
            print ("Optional Parameter Exception")
            optional = False
        try:
            vehicle_name = request.POST[consts.PARAM_VEHICLE_NAME]
        except:
            print ("Optional Parameter Exception")
            optional = False
        try:
            vehicle_registration = request.POST[consts.PARAM_VEHICLE_NUMBER]
        except:
            print ("Optional Parameter Exception")
            optional = False

        verified = False
        try:
            user = UserModel()
            user.username = name
            user.phone = phone
            user.email = email
            user.password = UserModel.encrypt_password(password)
            user.user_type = type
            if type == consts.TYPE_USER_RIDER:
                verified = True
            user.is_active = 0
            user.save()

            if optional is True:
                try:
                    driver = DriverModel()
                    driver.user = user
                    driver.status = consts.STATUS_DRIVER_OFFLINE
                    driver.license_num = driving_license
                    driver.vehicle_num = vehicle_registration
                    driver.vehicle_name = vehicle_name
                    driver.save()
                    verified = True
                except:
                    print "Driver registration failed"

        except:
            print "User registration failed"
            user = None
        print verified, type
        response = response_0003_register.RegisterResponse(user, verified)
        return HttpResponse(response.respond(), content_type="application/json")