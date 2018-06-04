from __future__ import unicode_literals

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import RideModel
from joldii.models import SessionModel
from joldii.models import VehicleClassModel
from joldii.models import DriverModel

from joldii.responses import common_response

import datetime, pytz
import math


class SearchRide(View):

    @staticmethod
    def post(request):
        print "*** SearchRide ***"
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
                    selected_driver.driver_status = consts.STATUS_DRIVER_APPROACHING_PICKUP
                    selected_driver.save()
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
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid ==> order id
            lat_from
            long_from
            pickup_place
    """

    @staticmethod
    def post(request):
        print "*** StartTrip ***"
        print request.POST
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")
        if SessionModel.objects.filter(session_id=request.POST[consts.PARAM_SESSION_ID],
                                       driver_status=consts.STATUS_DRIVER_APPROACHING_PICKUP).exists():
            try:
                ride_id = request.POST[consts.PARAM_ORDER_ID]
                pickup_lat = request.POST[consts.PARAM_LAT_FROM]
                pickup_lon = request.POST[consts.PARAM_LNG_FROM]
                if consts.PARAM_PICKUP_PLACE in request.POST:
                    pickup_place = request.POST[consts.PARAM_PICKUP_PLACE]
                else:
                    pickup_place = ''
            except:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Parameters',
                                                          error_code=consts.ERROR_INCORRECT_PARAMETERS)
                return HttpResponse(response.respond(), content_type="application/json")

            try:
                selected_trip = RideModel.objects.get(ride_id=ride_id)
                selected_trip.pickup_lat = pickup_lat
                selected_trip.pickup_lon = pickup_lon
                selected_trip.pickup_place = pickup_place
                selected_trip.order_status = consts.STATUS_ORDER_STARTED
                selected_trip.time_start = datetime.datetime.now()
                selected_trip.save()
                driver_session = SessionModel.objects.get(user=user)
                driver_session.driver_status = consts.STATUS_DRIVER_IN_RIDE
                driver_session.save()
                response = common_response.CommonResponse(success=True,
                                                          reason='Ride Successfully Started',
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            except:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Ride Information',
                                                          error_code=consts.ERROR_INCORRECT_RIDE_ID)
                return HttpResponse(response.respond(), content_type="application/json")
        else:
            response = common_response.CommonResponse(success=False,
                                                      reason='Driver Can Not Start Ride',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")


class EndTrip(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid ==> order id
            lat_to
            long_to
            distance
            distance
    """

    @staticmethod
    def post(request):
        print "*** EndTrip ***"
        print request.POST
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")
        if SessionModel.objects.filter(session_id=request.POST[consts.PARAM_SESSION_ID],
                                       driver_status=consts.STATUS_DRIVER_IN_RIDE).exists():
            try:
                ride_id = request.POST[consts.PARAM_ORDER_ID]
                drop_lat = request.POST[consts.PARAM_LAT_TO]
                drop_lon = request.POST[consts.PARAM_LNG_TO]
                distance = request.POST[consts.PARAM_DISTANCE]
                if consts.PARAM_DROP_PLACE in request.POST:
                    drop_place = request.POST[consts.PARAM_DROP_PLACE]
                else:
                    drop_place = ''
                try:
                    distance = float(distance)
                except:
                    distance = 0
            except:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Parameters',
                                                          error_code=consts.ERROR_INCORRECT_PARAMETERS)
                return HttpResponse(response.respond(), content_type="application/json")

            try:
                selected_trip = RideModel.objects.get(ride_id=ride_id)
                selected_trip.drop_lat = drop_lat
                selected_trip.drop_lon = drop_lon
                selected_trip.distance = float(distance)
                distance_in_km = float(distance) / float(1000)
                selected_trip.order_status = consts.STATUS_ORDER_COMPLETED
                time_end = datetime.datetime.now().replace(microsecond=0, tzinfo=pytz.UTC)
                time_start = selected_trip.time_start.replace(microsecond=0, tzinfo=pytz.UTC)
                selected_trip.duration = int((time_end-time_start).seconds)
                duration_in_min = (int((time_end-time_start).seconds) / 60) + 1
                selected_trip.base_fare = selected_trip.vehicle_class.base_fare
                total_bill = float(selected_trip.vehicle_class.base_fare)
                total_bill = total_bill + float(duration_in_min * selected_trip.vehicle_class.per_minute_fare)
                total_bill = total_bill + float(distance_in_km * selected_trip.vehicle_class.per_kilometer_fare)
                total_bill = math.ceil(total_bill - (total_bill / 100.00 * float(selected_trip.discount)))
                # print str(time_end-time_start)
                selected_trip.duration = int((time_end-time_start).seconds)
                selected_trip.total_bill = total_bill
                selected_trip.drop_place = drop_place
                selected_trip.save()
                driver_session = SessionModel.objects.get(user=user)
                driver_session.driver_status = consts.STATUS_DRIVER_ONLINE
                driver_session.save()

                order_data = {
                    'trip_order_id': selected_trip.ride_id,
                    'user': selected_trip.user.username,
                    'driver': selected_trip.driver.user.username,
                    'vehicle_class': selected_trip.vehicle_class.name,
                    'vehicle_class_base_fare': selected_trip.vehicle_class.base_fare,
                    'vehicle_class_per_kilometer_fare': selected_trip.vehicle_class.per_kilometer_fare,
                    'vehicle_class_per_minute_fare': selected_trip.vehicle_class.per_minute_fare,
                    # 'vehicle': selected_trip.vehicle.registration_number,
                    'pickup_lat': str(selected_trip.pickup_lat),
                    'pickup_lon': str(selected_trip.pickup_lon),
                    'drop_lat': str(selected_trip.drop_lat),
                    'drop_lon': str(selected_trip.drop_lon),
                    'distance': str(distance_in_km),
                    'duration': str(duration_in_min),
                    'total_bill': str(total_bill),
                    'discount': str(selected_trip.discount)
                }

                response = common_response.CommonResponse(success=True,
                                                          data=order_data,
                                                          reason='Ride Successfully Finished',
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            except:
                response = common_response.CommonResponse(success=False,
                                                          reason='Incorrect Ride Information',
                                                          error_code=consts.ERROR_INCORRECT_RIDE_ID)
                return HttpResponse(response.respond(), content_type="application/json")
        else:
            response = common_response.CommonResponse(success=False,
                                                      reason='Driver Can Not End Ride',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")


class PartnerPosition(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid ==> order id
    """

    @staticmethod
    def post(request):
        print "*** PartnerPosition ***"
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
            oid = request.POST[consts.PARAM_ORDER_ID]
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        # try:
        this_order = RideModel.objects.get(ride_id=oid)
        order_driver = SessionModel.objects.get(user=this_order.driver.user)
        order_user = SessionModel.objects.get(user=this_order.user)
        partner_data = {
            'ride_status': str(this_order.order_status),
            'driver_lat': str(order_driver.current_lat),
            'driver_lon': str(order_driver.current_lon),
            'user_lat': str(order_user.current_lat),
            'user_lon': str(order_user.current_lon)
        }
        response = common_response.CommonResponse(success=True,
                                                  reason='Updated Location',
                                                  data=partner_data,
                                                  error_code=consts.ERROR_NONE)
        return HttpResponse(response.respond(), content_type="application/json")
        # except:
        #     response = common_response.CommonResponse(success=False,
        #                                               reason='Incorrect Order',
        #                                               error_code=consts.ERROR_INCORRECT_RIDE_ID)
        #     return HttpResponse(response.respond(), content_type="application/json")


class ToggleDriverStatus(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            driver_status = online/offline
    """

    @staticmethod
    def post(request):
        print "*** ToggleDriverStatus ***"
        print request.POST
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user_session = SessionModel.objects.get(session_id=sess_id)
            if user_session.driver_status == 1 or user_session.driver_status == 0:
                driver_status = request.POST[consts.PARAM_DRIVER_STATUS]
                if driver_status == 'online':
                    user_session.driver_status = consts.STATUS_DRIVER_ONLINE
                    user_session.save()
                if driver_status == 'offline':
                    user_session.driver_status = consts.STATUS_DRIVER_OFFLINE
                    user_session.save()

                response = common_response.CommonResponse(success=True,
                                                          reason='Status Successfully Updated',
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
                response = common_response.CommonResponse(success=False,
                                                          reason='Driver In Ride or Not Driver',
                                                          error_code=consts.ERROR_USER_NOT_DRIVER)
                return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")


class NotifyDriver(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
    """

    @staticmethod
    def post(request):
        print "*** NotifyDriver ***"
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
            curr_lat = request.POST[consts.PARAM_LATITUDE]
            curr_lng = request.POST[consts.PARAM_LONGITUDE]
            sess = SessionModel.get_session_by_id(sess_id)
            sess.current_lat = curr_lat
            sess.current_lon = curr_lng
            sess.save()
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        try:
            driver_profile = DriverModel.objects.get(user=user)
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='User Not Driver',
                                                      error_code=consts.ERROR_USER_NOT_DRIVER)
            return HttpResponse(response.respond(), content_type="application/json")
        if RideModel.objects.filter(driver=driver_profile, order_status=consts.STATUS_ORDER_CONFIRMED).exists():
            current_trip = RideModel.objects.filter(driver=driver_profile,
                                                    order_status=consts.STATUS_ORDER_CONFIRMED)[0]
            trip_data = {
                'ride_id': current_trip.ride_id,
                'user_name': current_trip.user.username,
                'user_phone': current_trip.user.phone,
                'user_rating': current_trip.user.average_rating,
                'pickup_lat': str(current_trip.pickup_lat),
                'pickup_lon': str(current_trip.pickup_lon),
                'drop_lat': str(current_trip.drop_lat),
                'drop_lon': str(current_trip.drop_lon)
            }
            response = common_response.CommonResponse(success=True,
                                                      reason='New Order',
                                                      data=trip_data,
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        elif RideModel.objects.filter(driver=driver_profile, order_status=consts.STATUS_ORDER_STARTED).exists():
            current_trip = RideModel.objects.get(driver=driver_profile,
                                                 order_status=consts.STATUS_ORDER_STARTED)
            trip_data = {
                'ride_id': current_trip.ride_id,
                'user_name': current_trip.user.username,
                'user_phone': current_trip.user.phone,
                'user_rating': current_trip.user.average_rating,
                'pickup_lat': str(current_trip.pickup_lat),
                'pickup_lon': str(current_trip.pickup_lon),
                'drop_lat': str(current_trip.drop_lat),
                'drop_lon': str(current_trip.drop_lon)
            }
            response = common_response.CommonResponse(success=True,
                                                      reason='In Ride',
                                                      data=trip_data,
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        else:
            response = common_response.CommonResponse(success=True,
                                                      reason='No Ride Assigned',
                                                      error_code=consts.ERROR_UNKNOWN)
            return HttpResponse(response.respond(), content_type="application/json")


class NotifyUser(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid => order id
    """

    @staticmethod
    def post(request):
        print "*** NotifyUser ***"
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
            this_order = RideModel.objects.get(ride_id=request.POST[consts.PARAM_ORDER_ID])
            order_driver = SessionModel.objects.get(user=this_order.driver.user)
            trip_data = {
                'trip_status': this_order.order_status,
                'driver_lat': str(order_driver.current_lat),
                'driver_lon': str(order_driver.current_lon)
            }
            response = common_response.CommonResponse(success=True,
                                                      reason='New Order',
                                                      data=trip_data,
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Order',
                                                      error_code=consts.ERROR_INCORRECT_RIDE_ID)
            return HttpResponse(response.respond(), content_type="application/json")


class UserCancelRide(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid ==> order id
    """

    @staticmethod
    def post(request):
        print "*** UserCancelRide ***"
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
            oid = request.POST[consts.PARAM_ORDER_ID]
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        try:
            this_order = RideModel.objects.get(ride_id=oid)
            this_order.order_status = consts.STATUS_ORDER_CANCELLED_USER
            this_order.save()
            response = common_response.CommonResponse(success=True,
                                                      reason='Order Successfully Cancelled',
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Order',
                                                      error_code=consts.ERROR_INCORRECT_RIDE_ID)
            return HttpResponse(response.respond(), content_type="application/json")


class DriverCancelRide(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            oid ==> order id
    """

    @staticmethod
    def post(request):
        print "*** DriverCancelRide ***"
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
            oid = request.POST[consts.PARAM_ORDER_ID]
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
        try:
            this_order = RideModel.objects.get(ride_id=oid)
            this_order.order_status = consts.STATUS_ORDER_CANCELLED_DRIVER
            this_order.save()
            response = common_response.CommonResponse(success=True,
                                                      reason='Order Successfully Cancelled',
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Order',
                                                      error_code=consts.ERROR_INCORRECT_RIDE_ID)
            return HttpResponse(response.respond(), content_type="application/json")


class GetHistory(View):
    """
    todo add this to wiki
    Quick Doc
    param   sid
            app_type = driver/user
    """

    @staticmethod
    def post(request):
        print "*** GetHistory ***"
        print request.POST
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)
            app_type = request.POST[consts.PARAM_APP_TYPE]
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Invalid Session',
                                                      error_code=consts.ERROR_INCORRECT_SESSION)
            return HttpResponse(response.respond(), content_type="application/json")
        trip_data = []
        if app_type == 'driver':
            driver_profile = DriverModel.objects.get(user=user)
            all_trips_of_this_driver = RideModel.objects.filter(driver=driver_profile, order_status=3)
            for selected_trip in all_trips_of_this_driver:
                order_data = {
                    'trip_order_id': selected_trip.ride_id,
                    'user': selected_trip.user.username,
                    'vehicle_class': selected_trip.vehicle_class.name,
                    'vehicle_class_base_fare': selected_trip.vehicle_class.base_fare,
                    'vehicle_class_per_kilometer_fare': selected_trip.vehicle_class.per_kilometer_fare,
                    'vehicle_class_per_minute_fare': selected_trip.vehicle_class.per_minute_fare,
                    'pickup_lat': str(selected_trip.pickup_lat),
                    'pickup_lon': str(selected_trip.pickup_lon),
                    'drop_lat': str(selected_trip.drop_lat),
                    'drop_lon': str(selected_trip.drop_lon),
                    'distance': str(float(selected_trip.distance) / float(1000)),
                    'duration': str((int(selected_trip.duration) / 60) + 1),
                    'total_bill': str(selected_trip.total_bill),
                    'discount': str(selected_trip.discount)
                }
                trip_data.append(order_data)
        else:
            all_trips_of_this_user = RideModel.objects.filter(user=user, order_status=3)
            for selected_trip in all_trips_of_this_user:
                order_data = {
                    'trip_order_id': selected_trip.ride_id,
                    'driver': selected_trip.driver.user.username,
                    'vehicle_class': selected_trip.vehicle_class.name,
                    'vehicle_class_base_fare': selected_trip.vehicle_class.base_fare,
                    'vehicle_class_per_kilometer_fare': selected_trip.vehicle_class.per_kilometer_fare,
                    'vehicle_class_per_minute_fare': selected_trip.vehicle_class.per_minute_fare,
                    'pickup_lat': str(selected_trip.pickup_lat),
                    'pickup_lon': str(selected_trip.pickup_lon),
                    'drop_lat': str(selected_trip.drop_lat),
                    'drop_lon': str(selected_trip.drop_lon),
                    'distance': str(float(selected_trip.distance) / float(1000)),
                    'duration': str((int(selected_trip.duration) / 60) + 1),
                    'total_bill': str(selected_trip.total_bill),
                    'discount': str(selected_trip.discount)
                }
                trip_data.append(order_data)

        response = common_response.CommonResponse(success=True,
                                                  data=trip_data,
                                                  reason='History Successfully Sent',
                                                  error_code=consts.ERROR_NONE)
        return HttpResponse(response.respond(), content_type="application/json")


