# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View

from joldii.actions import user_session
from joldii.constants import consts


# Create your views here.
class APIRouter(View):
    @staticmethod
    def post(request):
        action = request.POST[consts.PARAM_ACTION]
        print action
        if action == consts.ACTION_LOGIN:
            print "Login Request"
            return user_session.login(request)
        # elif action is consts.ACTION_PIN_VERIFICATION:
        #     pin_verification(request)
        elif action == consts.ACTION_REGISTER:
            print "Register Request"
            return user_session.register(request)
            # elif action is consts.ACTION_FORGET_PASSWORD:
            #     forget_password(request)
            # elif action is consts.ACTION_PROMO:
            #     promo(request)
            # elif action is consts.ACTION_CHANGE_NAME:
            #     change_name(request)
            # elif action is consts.ACTION_CHANGE_EMAIL:
            #     change_email(request)
            # elif action is consts.ACTION_CHANGE_PHONE:
            #     change_phone(request)
            # elif action is consts.ACTION_RIDE_REQUEST:
            #     ride_request(request)
            # elif action is consts.ACTION_RIDE_STARTED:
            #     ride_started(request)
            # elif action is consts.ACTION_RIDE_ENDED:
            #     ride_ended(request)
            # elif action is consts.ACTION_UPDATE_FARE:
            #     action_fare(request)
            # elif action is consts.ACTION_VIEW_HISTORY:
            #     view_history(request)
