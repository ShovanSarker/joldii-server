from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register
from joldii.views import UploadLocation
from joldii.views import AddVehicle
from joldii.views import GetRideInformation
from joldii.views import AddPromo
from joldii.views import RedeemPromo
from joldii.views import SearchRide

from joldii.views import Users
from joldii.views import SessionList

urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),
    url(r'^forgot_password', view=Login.as_view(), name="forgot_password"),
    url(r'^validate_registration', view=Login.as_view(), name="validate_registration"),

    url(r'^upload_position', view=UploadLocation.as_view(), name="upload_position"),
    url(r'^find_drivers', view=UploadLocation.as_view(), name="find_drivers"),
    url(r'^add_vehicle', view=AddVehicle.as_view(), name="add_vehicle"),
    url(r'^get_ride_info', view=GetRideInformation.as_view(), name="get_ride_info"),
    url(r'^add_promo', view=AddPromo.as_view(), name="add_promo"),
    url(r'^redeem_promo', view=RedeemPromo.as_view(), name="redeem_promo"),

    url(r'^order_ride', view=SearchRide.as_view(), name="order_ride"),


    url(r'^test/users', view=Users.as_view(), name="test_users"),
    url(r'^test/sessions', view=SessionList.as_view(), name="test_sessions"),
]
