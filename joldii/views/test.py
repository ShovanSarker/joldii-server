from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views import View

from joldii.models import UserModel


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
        return HttpResponse(json.dumps(user_array), content_type="application/json")
