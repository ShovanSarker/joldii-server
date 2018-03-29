from __future__ import unicode_literals

import json

from joldii.constants import consts

from django.http import HttpResponse
from django.views import View

from joldii.models import UserModel
from joldii.models import SessionModel

from joldii.responses import common_response


class Users(View):

    @staticmethod
    def post(request):
        all_users = UserModel.objects.all()
        user_array = []
        for one_user in all_users:
            one_user_info = {'user name': one_user.username,
                             'phone': one_user.phone,
                             'user_type': one_user.user_type,
                             'is_active': one_user.is_active,
                             'pin': one_user.pin
                             }
            user_array.append(one_user_info)
        response = common_response.CommonResponse(success=True,
                                                  reason='ALL USERS',
                                                  error_code=consts.ERROR_USER_PRESENT,
                                                  data=user_array)
        # print(response)
        return HttpResponse(response.respond(), content_type="application/json")


class SessionList(View):

    @staticmethod
    def post(request):
        all_sessions = SessionModel.objects.all()
        user_array = []
        for one_session in all_sessions:
            one_user_info = {'username': one_session.user.username,
                             'session_id': one_session.session_id,
                             'current_lat': str(one_session.current_lat),
                             'current_lon': str(one_session.current_lon),
                             'current_ride': one_session.current_ride,
                             'is_driver': one_session.is_driver,
                             'driver_status': one_session.driver_status
                             }
            user_array.append(one_user_info)
        response = common_response.CommonResponse(success=True,
                                                  reason='ALL SESSIONS',
                                                  error_code=consts.ERROR_USER_PRESENT,
                                                  data=user_array)
        # print(response)
        return HttpResponse(response.respond(), content_type="application/json")
