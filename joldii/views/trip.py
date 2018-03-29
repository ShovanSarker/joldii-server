from __future__ import unicode_literals

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import RideModel
from joldii.models import SessionModel
from joldii.models import VehicleClassModel

from joldii.responses import common_response


class SearchRide(View):

    @staticmethod
    def post(request):
        print request.POST
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")

        try:
            vehicle_class = VehicleClassModel.objects.get(pk=request.POST[consts.PARAM_VEHICLE_TYPE])
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Vehicle Type',
                                                      error_code=consts.ERROR_INCORRECT_VEHICLE_TYPE)
            return HttpResponse(response.respond(), content_type="application/json")
        try:
            if RideModel.objects.filter(user=user, order_status__lte=2).exists():
                previous_incomplete_ride = RideModel.objects.filter(user=user, order_status__lte=2)[0]
                driver_information = {
                    'driver_name': previous_incomplete_ride.driver.user.username,
                    'driver_phone': previous_incomplete_ride.driver.user.phone
                    # 'driver_rating': selected_driver.driver_profile.average_rating,
                    # 'driver_trip_count': selected_driver.driver_profile.number_of_rides
                }
                vehicle_information = {
                    # 'model': selected_driver.current_vehicle.model,
                    # 'registration_number': selected_driver.current_vehicle.registration_number
                }

                order_data = {
                    'trip_order_id': previous_incomplete_ride.ride_id,
                    'driver_information': driver_information,
                    'vehicle_information': vehicle_information
                }
                response = common_response.CommonResponse(success=True,
                                                          reason='Order Data Retrieved',
                                                          data=order_data,
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
                print "Finding new ride"
                new_order = RideModel(
                    user=user,
                    vehicle_class=vehicle_class,
                    pickup_lat=request.POST[consts.PARAM_LAT_FROM],
                    pickup_lon=request.POST[consts.PARAM_LNG_FROM],
                    drop_lat=request.POST[consts.PARAM_LAT_TO],
                    drop_lon=request.POST[consts.PARAM_LNG_FROM],
                    order_status=consts.STATUS_ORDER_PLACED
                )
                new_order.save()
                print "Finding Drivers"
                selected_driver = SearchRide.find_driver(request.POST[consts.PARAM_LAT_FROM],
                                                         request.POST[consts.PARAM_LNG_FROM])
                if selected_driver is None:
                    new_order.order_status = consts.STATUS_ORDER_NO_DRIVER_FOUND
                    new_order.save()
                    response = common_response.CommonResponse(success=False,
                                                              reason='No Driver Found',
                                                              error_code=consts.ERROR_NO_DRIVER_FOUND)
                    return HttpResponse(response.respond(), content_type="application/json")
                else:
                    print()
                    new_order.driver = selected_driver.driver_profile
                    # new_order.vehicle = selected_driver.current_vehicle
                    new_order.order_status = consts.STATUS_ORDER_CONFIRMED
                    new_order.save()
                    driver_information = {
                        'driver_name': selected_driver.user.username,
                        'driver_phone': selected_driver.user.phone
                        # 'driver_rating': selected_driver.driver_profile.average_rating,
                        # 'driver_trip_count': selected_driver.driver_profile.number_of_rides
                    }
                    vehicle_information = {
                        # 'model': selected_driver.current_vehicle.model,
                        # 'registration_number': selected_driver.current_vehicle.registration_number
                    }

                    order_data = {
                        'trip_order_id': new_order.ride_id,
                        'driver_information': driver_information,
                        'vehicle_information': vehicle_information
                    }
                    response = common_response.CommonResponse(success=True,
                                                              reason='Order Successfully Received',
                                                              data=order_data,
                                                              error_code=consts.ERROR_NONE)
                    return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")

    @staticmethod
    def find_driver(lat, lng):
        rad = 0.0
        tries = 0
        drivers = None
        while (drivers is None or len(drivers) < 1) and tries < 10:
            rad += 0.5
            tries += 1
            min_lat = float(lat) - (rad/111)
            min_lng = float(lng) - (rad / 111)
            max_lat = float(lat) + (rad / 111)
            max_lng = float(lng) + (rad / 111)
            try:
                drivers = SessionModel.objects.filter(driver_status=consts.STATUS_DRIVER_ONLINE,
                                                      current_lat__range=(min_lat, max_lat),
                                                      current_lon__range=(min_lng, max_lng))
                for driver in drivers:
                    return driver
                print "Radius: %s %s, Drivers: %s" % (rad, (rad/111), drivers)
            except MultiValueDictKeyError:
                drivers = None
                print "No drivers found"
        return None


class StartTrip(View):

    @staticmethod
    def post(request):
        request