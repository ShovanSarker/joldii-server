from __future__ import unicode_literals

from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import SessionModel
from joldii.models import VehicleClassModel
from joldii.models import UserPromoModel
from joldii.models import PromoModel

from joldii.responses.response_update_location import UpdateLocationResponse
from joldii.responses import common_response


class AddPromo(View):
    @staticmethod
    def post(request):
        response = UpdateLocationResponse()
        try:
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            curr_lat = request.POST[consts.PARAM_LATITUDE]
            curr_lng = request.POST[consts.PARAM_LONGITUDE]
        except:
            print request.POST
            print "Required parameter exception"

        try:
            sess = SessionModel.get_session_by_id(sess_id)
            print sess.current_lat
            sess.current_lat = curr_lat
            sess.current_lon = curr_lng
            sess.save()

            response.set_status(UpdateLocationResponse.STATE_SUCCESS)
        except:
            print "User save error"

        return HttpResponse(response.respond(), content_type="application/json")


class FindDrivers(View):
    @staticmethod
    def post(request):
        pass


class GetRideInformation(View):

    @staticmethod
    def post(request):
        try:
            all_ride_type = VehicleClassModel.objects.all()
            all_ride_type_array = []
            sess_id = request.POST[consts.PARAM_SESSION_ID]
            user = SessionModel.get_user_by_session(sess_id)

            for ride_type in all_ride_type:
                discount = 0
                if PromoModel.objects.filter(vehicle_type=ride_type).exists():
                    for on_going_promo in PromoModel.objects.filter(vehicle_type=ride_type):
                        if UserPromoModel.objects.filter(promo=on_going_promo, user=user).exists():
                            if UserPromoModel.objects.filter(promo=on_going_promo, user=user)[0].remaining_ride > 0:
                                discount = on_going_promo.discount
                one_ride = {'type': ride_type.name,
                            'base_fare': ride_type.base_fare,
                            'per_kilometer_fare': ride_type.per_kilometer_fare,
                            'per_minute_fare': ride_type.per_minute_fare,
                            'maximum_passenger': ride_type.maximum_passenger,
                            'discount': discount}
                all_ride_type_array.append(one_ride)
            response = common_response.CommonResponse(success=True,
                                                      reason='All Type of Rides',
                                                      data=all_ride_type_array,
                                                      error_code=consts.ERROR_NONE)
            return HttpResponse(response.respond(), content_type="application/json")
        except:
            response = common_response.CommonResponse(success=False,
                                                      reason='Incorrect Parameters',
                                                      error_code=consts.ERROR_INCORRECT_PARAMETERS)
            return HttpResponse(response.respond(), content_type="application/json")
