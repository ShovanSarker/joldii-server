from __future__ import unicode_literals

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
                order_data = {
                    'trip_order_id': previous_incomplete_ride.ride_id
                }
                response = common_response.CommonResponse(success=True,
                                                          reason='Order Data Retrieved',
                                                          data=order_data,
                                                          error_code=consts.ERROR_NONE)
                return HttpResponse(response.respond(), content_type="application/json")
            else:
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
                order_data = {
                    'trip_order_id': new_order.ride_id
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
