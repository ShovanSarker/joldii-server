from django.http import HttpResponse
from django.views import View

from random import randint

from joldii.constants import consts

from joldii.models import DriverModel
from joldii.models import UserModel
from joldii.models import SessionModel

from joldii.responses import response_login
from joldii.responses import response_register
from joldii.responses import response_incorrect_parameters
from joldii.responses import common_response


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
                    is_driver = True
                else:
                    is_driver = False
                if SessionModel.objects.filter(user=user).exists():
                    existing_sessions = SessionModel.objects.filter(user=user)
                    for existing_session in existing_sessions:
                        existing_session.delete()

                session = SessionModel(
                    user=user,
                    is_driver=is_driver

                )

                session.save()
                user_data = {
                    'session_id': session.session_id,
                    'user_name': session.user.username,
                    'user_rating': session.user.average_rating,
                    'user_phone': session.user.phone,
                    'user_photo_url': str(session.user.user_picture)
                }
                response = common_response.CommonResponse(success=True,
                                                          data=user_data,
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Phone Number or Password',
                                                          error_code=consts.ERROR_INCORRECT_PHONE_OR_PASSWORD)
                return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")


class Register(View):

    @staticmethod
    def post(request):
        print request.POST
        optional = True
        user_type = None
        try:
            phone = request.POST[consts.PARAM_PHONE]
            name = request.POST[consts.PARAM_USER_NAME]
            password = request.POST[consts.PARAM_PASSWORD]

            if consts.PARAM_APP_TYPE in request.POST:
                app_type = request.POST[consts.PARAM_APP_TYPE]
            else:
                app_type = 'user'

            if consts.PARAM_USER_MAIL in request.POST:
                email = request.POST[consts.PARAM_USER_MAIL]
            else:
                email = ''

            if consts.PARAM_USER_ADDRESS in request.POST:
                address = request.POST[consts.PARAM_USER_ADDRESS]
            else:
                address = ''

            if app_type == 'driver':
                user_type = 2
            else:
                user_type = 1
            if UserModel.objects.filter(phone=phone).exists():
                response = common_response.CommonResponse(success=False,
                                                          reason='Phone Number Already Registered',
                                                          error_code=consts.ERROR_USER_PRESENT)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
                user = UserModel(
                    username=name,
                    email=email,
                    phone=phone,
                    password=UserModel.encrypt_password(password),
                    address=address,
                    user_type=user_type,
                    is_active=True
                )
                user.save()

            if consts.PARAM_USER_PIC in request.FILES:
                user.user_picture = request.FILES[consts.PARAM_USER_PIC]
                user.save()

            """
            for pin
            """
            # pin = str(randint(1001, 9999))
            # user.pin = pin
            # user.save()
            #
            # #todo add sms api to send user the pin for account verification

            """
            for pin
            """

            response = common_response.CommonResponse(success=True,
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")


class PinVerification(View):

    @staticmethod
    def post(request):
        phone = request.POST[consts.PARAM_PHONE]
