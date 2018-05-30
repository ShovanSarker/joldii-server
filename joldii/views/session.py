from django.http import HttpResponse
from django.views import View

from random import randint

from joldii.constants import consts

from joldii.models import DriverModel
from joldii.models import UserModel
from joldii.models import RideModel
from joldii.models import DriverRatingModel
from joldii.models import UserRatingModel
from joldii.models import SessionModel
from joldii.models import VehicleModel
from joldii.models import VehicleClassModel

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
                if DriverModel.objects.filter(user=user).exists():
                    session = SessionModel(
                        user=user,
                        is_driver=is_driver,
                        driver_profile=DriverModel.objects.get(user=user)
                    )
                else:
                    session = SessionModel(
                        user=user,
                        is_driver=is_driver,

                    )
                session.save()
                if is_driver:
                    if DriverModel.objects.filter(user=user).exists():
                        driver = DriverModel.objects.get(user=user)
                        session.driver_profile = driver
                        session.save()
                        if VehicleModel.objects.filter(driver=driver).exists():
                            driver_data = {
                                'driver_nid': driver.national_id,
                                'driver_dl': driver.driving_license,
                                'driver_rating': driver.average_rating,
                                'driver_ride_count': driver.number_of_rides
                            }
                            all_vehicles = VehicleModel.objects.filter(driver=driver)
                            vehicle_array = []
                            for one_vehicle in all_vehicles:
                                vehicle_data = {
                                    'registration_number': one_vehicle.registration_number,
                                    'vehicle_type': one_vehicle.ride_class.name,
                                    'vehicle_type_id': one_vehicle.ride_class.pk,
                                    'vehicle_color': one_vehicle.color
                                }
                                vehicle_array.append(vehicle_data)
                            user_data = {
                                'session_id': session.session_id,
                                'user_name': session.user.username,
                                'user_email': session.user.email,
                                'user_rating': session.user.average_rating,
                                'user_phone': session.user.phone,
                                'user_photo_url': str(session.user.user_picture),
                                'driver': driver_data,
                                'vehicle': vehicle_array
                            }
                            session.driver_status = consts.STATUS_DRIVER_ONLINE
                            session.driver_profile = driver
                            session.save()
                            response = common_response.CommonResponse(success=True,
                                                                      data=user_data,
                                                                      error_code=consts.ERROR_NONE)
                            return HttpResponse(response.respond(), content_type="application/json")
                        else:
                            driver_data = {
                                'driver_nid': driver.national_id,
                                'driver_dl': driver.driving_license,
                                'driver_rating': driver.average_rating,
                                'driver_ride_count': driver.number_of_rides
                            }
                            user_data = {
                                'session_id': session.session_id,
                                'user_name': session.user.username,
                                'user_email': session.user.email,
                                'user_rating': session.user.average_rating,
                                'user_phone': session.user.phone,
                                'user_photo_url': str(session.user.user_picture),
                                'driver': driver_data,
                                'vehicle': None
                            }
                            session.driver_profile = driver
                            session.driver_status = consts.STATUS_DRIVER_OFFLINE
                            session.save()
                            response = common_response.CommonResponse(success=True,
                                                                      data=user_data,
                                                                      reason='Vehicle Not Selected',
                                                                      error_code=consts.ERROR_NONE)
                            return HttpResponse(response.respond(), content_type="application/json")
                    else:
                        user_data = {
                            'session_id': session.session_id,
                            'user_name': session.user.username,
                            'user_email': session.user.email,
                            'user_rating': session.user.average_rating,
                            'user_phone': session.user.phone,
                            'user_photo_url': str(session.user.user_picture),
                            'driver': None,
                            'vehicle': None
                        }
                        session.driver_status = consts.STATUS_DRIVER_OFFLINE
                        session.save()
                        response = common_response.CommonResponse(success=True,
                                                                  data=user_data,
                                                                  reason='Driver Profile Not Added',
                                                                  error_code=consts.ERROR_NONE)
                        return HttpResponse(response.respond(), content_type="application/json")
                else:
                    user_data = {
                        'session_id': session.session_id,
                        'user_name': session.user.username,
                        'user_email': session.user.email,
                        'user_rating': session.user.average_rating,
                        'user_phone': session.user.phone,
                        'user_photo_url': str(session.user.user_picture)
                    }
                    session.driver_status = consts.STATUS_NOT_DRIVER
                    session.save()
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


class UploadDriverInfo(View):

    @staticmethod
    def post(request):
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")
        try:

            driver = DriverModel(user=user,
                                 national_id=request.POST[consts.PARAM_DRIVER_NATIONAL_ID],
                                 national_id_image=request.FILES[consts.PARAM_DRIVER_NATIONAL_ID_IMAGE],
                                 driving_license=request.FILES[consts.PARAM_DRIVER_LICENSE],
                                 driving_license_image=request.POST[consts.PARAM_DRIVER_LICENSE_IMAGE])

            driver.save()
            response = common_response.CommonResponse(success=True,
                                                      reason='Driver Profile Successfully Added',
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")


class UploadVehicleInfo(View):

    @staticmethod
    def post(request):
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")
        try:
            driver = DriverModel.objects.get(user=user)
            vehicle_class = VehicleClassModel.objects.get(pk=request.POST[consts.PARAM_VEHICLE_TYPE_ID])
            new_vehicle = VehicleModel(registration_number=request.POST[consts.PARAM_VEHICLE_NUMBER],
                                       color=request.POST[consts.PARAM_VEHICLE_COLOR],
                                       model=request.POST[consts.PARAM_VEHICLE_NAME],
                                       ride_class=vehicle_class,
                                       registration_certificate_image=request.FILES[consts.PARAM_VEHICLE_NUMBER_PHOTO],
                                       driver=driver)
            new_vehicle.save()
            response = common_response.CommonResponse(success=True,
                                                      reason='Vehicle Successfully Added',
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")


class GetVehicleInfo(View):

    @staticmethod
    def post(request):
        all_vehicle_type = VehicleClassModel.objects.all()
        all_vehicle_type_array = []
        for one_vehicle_type in all_vehicle_type:
            one_vehicle = {
                'vehicle_type': one_vehicle_type.name,
                'vehicle_type_id': one_vehicle_type.pk
            }
            all_vehicle_type_array.append(one_vehicle)
        response = common_response.CommonResponse(success=True,
                                                  data=all_vehicle_type_array,
                                                  reason='All Vehicle Type List',
                                                  error_code=consts.ERROR_NONE)
        return HttpResponse(response.respond(), content_type="application/json")


class RateDriver(View):

    @staticmethod
    def post(request):
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")

        try:
            ride_id = request.POST[consts.PARAM_ORDER_ID]
            ride = RideModel.objects.get(ride_id=ride_id)
            ride_user = ride.user
            ride_driver = ride.driver
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Ride ID',
                                                      error_code=consts.ERROR_INCORRECT_RIDE_ID)
            return HttpResponse(response.respond(), content_type="application/json")
        if consts.PARAM_COMMENT in request.POST:
            comment = request.POST[consts.PARAM_COMMENT]
        else:
            comment = ''
        try:
            rating = int(request.POST[consts.PARAM_RATING])
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Parameter',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        new_rating = DriverRatingModel(
            user=ride_user,
            driver=ride_driver,
            rating=rating,
            ride=ride,
            comment=comment
        )
        new_rating.save()

        current_rating = ride_driver.average_rating
        current_ride_count = ride_driver.number_of_rides
        updated_rating = ((current_rating * float(current_ride_count)) + float(rating)) / float(current_ride_count + 1)
        updated_ride_count = current_ride_count + 1
        ride_driver.average_rating = updated_rating
        ride_driver.number_of_rides = updated_ride_count
        ride_driver.save()
        response = common_response.CommonResponse(success=True,
                                                  reason='Rating Successfully Updated',
                                                  error_code=consts.ERROR_NONE)
        return HttpResponse(response.respond(), content_type="application/json")


class RateUser(View):

    @staticmethod
    def post(request):
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")

        try:
            ride_id = request.POST[consts.PARAM_ORDER_ID]
            ride = RideModel.objects.get(ride_id=ride_id)
            ride_user = ride.user
            ride_driver = ride.driver
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Ride ID',
                                                      error_code=consts.ERROR_INCORRECT_RIDE_ID)
            return HttpResponse(response.respond(), content_type="application/json")
        if consts.PARAM_COMMENT in request.POST:
            comment = request.POST[consts.PARAM_COMMENT]
        else:
            comment = ''
        try:
            rating = int(request.POST[consts.PARAM_RATING])
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Parameter',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        new_rating = UserRatingModel(
            user=ride_user,
            driver=ride_driver,
            rating=rating,
            ride=ride,
            comment=comment
        )
        new_rating.save()

        current_rating = ride_user.average_rating
        current_ride_count = ride_user.number_of_rides
        updated_rating = ((current_rating * float(current_ride_count)) + float(rating)) / float(current_ride_count + 1)
        updated_ride_count = current_ride_count + 1
        ride_user.average_rating = updated_rating
        ride_user.number_of_rides = updated_ride_count
        ride_user.save()
        response = common_response.CommonResponse(success=True,
                                                  reason='Rating Successfully Updated',
                                                  error_code=consts.ERROR_NONE)
        return HttpResponse(response.respond(), content_type="application/json")
