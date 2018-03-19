from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register
from joldii.views import UploadLocation

urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),
    url(r'^forgot_password', view=Login.as_view(), name="forgot_password"),
    url(r'^validate_registration', view=Login.as_view(), name="validate_registration"),

    url(r'^upload_position', view=UploadLocation.as_view(), name="upload_position"),
    url(r'^find_drivers', view=UploadLocation.as_view(), name="find_drivers"),
]
