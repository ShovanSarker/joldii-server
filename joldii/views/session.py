from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import DriverModel
from joldii.models import UserModel
from joldii.models import SessionModel

from joldii.responses import response_login
from joldii.responses import response_register
from joldii.responses import response_incorrect_parameters


class Login(View):

    @staticmethod
    def post(request):
        phone = None
        password = None
        try:
            phone = request.POST[consts.PARAM_PHONE]
            password = request.POST[consts.PARAM_PASSWORD]
            '''mention the app type[driver ]'''
            app_type = request.POST[consts.PARAM_APP_TYPE]
            user = UserModel.get_user_by_phone_password(phone, password)
            if user is not None:
                if app_type == 'driver':
                    is_driver = 1
                else:
                    is_driver = 0
                session = SessionModel(
                    user=user,
                    is_driver=is_driver

                )
            response = response_login.LoginResponse(user)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = response_incorrect_parameters.IncorrectParametersResponse()
            return HttpResponse(response.respond(), content_type="application/json")



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
            optional = False
        except:
            print ("Optional Parameter Exception")
        try:
            driving_license = request.POST[consts.PARAM_DRIVER_LICENSE]
            optional = False
        except:
            print ("Optional Parameter Exception")
        try:
            vehicle_name = request.POST[consts.PARAM_VEHICLE_NAME]
            optional = False
        except:
            print ("Optional Parameter Exception")
        try:
            vehicle_registration = request.POST[consts.PARAM_VEHICLE_NUMBER]
            optional = False
        except:
            print ("Optional Parameter Exception")

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
        response = response_register.RegisterResponse(user, verified)
        return HttpResponse(response.respond(), content_type="application/json")


class PinVerification(View):

    @staticmethod
    def post(request):
        phone = request.POST[consts.PARAM_PHONE]