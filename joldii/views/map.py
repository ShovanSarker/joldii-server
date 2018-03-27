from __future__ import unicode_literals

from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import SessionModel
from joldii.models import VehicleClassModel

from joldii.responses.response_update_location import UpdateLocationResponse
from joldii.responses.response_get_ride_info import GetRideInfoResponse


class UploadLocation(View):
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
        all_ride_type = VehicleClassModel.objects.all()
        all_ride_type_array = []
        for ride_type in all_ride_type:
            one_ride = {'type': ride_type.name,
                        'base_fare': ride_type.base_fare,
                        'per_kilometer_fare': ride_type.per_kilometer_fare,
                        'per_minute_fare': ride_type.per_minute_fare,
                        'maximum_passenger': ride_type.maximum_passenger,
                        'discount': ride_type.maximum_passenger}
            all_ride_type_array.append(one_ride)
        # todo use sid to avail discount for the user
        sess_id = request.POST[consts.PARAM_SESSION_ID]
        response = GetRideInfoResponse(all_ride_type_array)
        return HttpResponse(response.respond(), content_type="application/json")
