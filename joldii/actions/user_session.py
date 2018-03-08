from django.http import HttpResponse

from joldii.constants import consts
from joldii.models import UserModel
from joldii.responses import response_0001_login
from joldii.responses import response_0003_register


def login(request):
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


def register(request):
    try:
        phone = request.POST[consts.PARAM_PHONE]
        name = request.POST[consts.PARAM_USER_NAME]
        email = request.POST[consts.PARAM_USER_MAIL]
        password = request.POST[consts.PARAM_PASSWORD]
    except:
        print ("Parameter Exception")
    try:
        user = UserModel()
        user.username = name
        user.phone = phone
        user.email = email
        user.password = UserModel.encrypt_password(password)
        user.user_type = consts.TYPE_USER_RIDER
        user.is_active = 0
        user.save()
    except:
        print "User registration failed"
        user = None
    response = response_0003_register.RegisterResponse(user)
    return HttpResponse(response.respond(), content_type="application/json")


def pin_verification(request):
    phone = request.POST[consts.PARAM_PHONE]
