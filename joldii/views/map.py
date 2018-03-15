from __future__ import unicode_literals

from django.http import HttpResponse
from django.views import View

from joldii.constants import consts
from joldii.models import SessionModel
from joldii.responses.response_update_location import UpdateLocationResponse


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
            user = SessionModel.get_user_by_session(sess_id)
            user.curr_lat = curr_lat
            user, curr_lng = curr_lng
            user.save()
        except:
            print "User save error"

            return HttpResponse(response.respond(), content_type="application/json")


class FindDrivers(View):
    @staticmethod
    def post(request):
        pass
