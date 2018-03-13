from __future__ import unicode_literals

from django.views import View

from django.http import HttpResponse

from joldii.constants import consts
from joldii.models import UserModel
from joldii.responses import response_0001_login


class Login(View):
    @staticmethod
    def post(request):
        phone = None
        password = None
        try:
            phone = request.POST[consts.PARAM_PHONE]
            password = request.POST[consts.PARAM_PASSWORD]
        except:
            print ("Parameter Exception")
        user = UserModel.get_user_by_phone_password(phone, password)
        response = response_0001_login.LoginResponse(user)
        return HttpResponse(response.respond(), content_type="application/json")
