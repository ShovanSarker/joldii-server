from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register
from joldii.views import dashboard
from joldii.views import login
from joldii.views import users
from joldii.views import rides
from joldii.views import ride_detail
from joldii.views import ride_settings
from joldii.views import promo
from joldii.views import accounts
from joldii.views import user_directory
from joldii.views import vehicle_list

from joldii.views import UploadLocation
from joldii.views import AddVehicle
from joldii.views import GetRideInformation
from joldii.views import AddPromo
from joldii.views import RedeemPromo
from joldii.views import SearchRide
from joldii.views import StartTrip
from joldii.views import EndTrip
from joldii.views import PartnerPosition
from joldii.views import ToggleDriverStatus
from joldii.views import UploadDriverInfo
from joldii.views import UploadVehicleInfo
from joldii.views import NotifyDriver
from joldii.views import NotifyUser
from joldii.views import GetVehicleInfo

from joldii.views import Users
from joldii.views import SessionList

urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),

    url(r'^dashboard', view=dashboard, name="dashboard"),
    url(r'^log', view=login, name="login"),
    url(r'^users', view=users, name="users"),
    url(r'^rides', view=rides, name="rides"),
    url(r'^ride_detail', view=ride_detail, name="ride_detail"),
    url(r'^ride_settings', view=ride_settings, name="ride_settings"),
    url(r'^promo', view=promo, name="promo"),
    url(r'^accounts', view=accounts, name="accounts"),
    url(r'^user_directory', view=user_directory, name="user_directory"),
    url(r'^vehicle_list', view=vehicle_list, name="vehicle_list"),

    url(r'^forgot_password', view=Login.as_view(), name="forgot_password"),
    url(r'^validate_registration', view=Login.as_view(), name="validate_registration"),

    url(r'^upload_position', view=UploadLocation.as_view(), name="upload_position"),
    url(r'^find_drivers', view=UploadLocation.as_view(), name="find_drivers"),
    url(r'^add_vehicle', view=AddVehicle.as_view(), name="add_vehicle"),
    url(r'^get_ride_info', view=GetRideInformation.as_view(), name="get_ride_info"),
    url(r'^add_promo', view=AddPromo.as_view(), name="add_promo"),
    url(r'^redeem_promo', view=RedeemPromo.as_view(), name="redeem_promo"),
    url(r'^upload_driver_info', view=UploadDriverInfo.as_view(), name="upload_driver_info"),
    url(r'^upload_vehicle_info', view=UploadVehicleInfo.as_view(), name="upload_vehicle_info"),
    url(r'^notify_driver', view=NotifyDriver.as_view(), name="notify_driver"),
    url(r'^notify_user', view=NotifyUser.as_view(), name="notify_user"),
    url(r'^get_vehicle_info', view=GetVehicleInfo.as_view(), name="get_vehicle_info"),

    url(r'^order_ride', view=SearchRide.as_view(), name="order_ride"),
    url(r'^start_ride', view=StartTrip.as_view(), name="start_ride"),
    url(r'^end_ride', view=EndTrip.as_view(), name="end_ride"),
    url(r'^partner_position', view=PartnerPosition.as_view(), name="partner_position"),
    url(r'^update_driver_position', view=ToggleDriverStatus.as_view(), name="update_driver_position"),
    url(r'^test/users', view=Users.as_view(), name="test_users"),
    url(r'^test/sessions', view=SessionList.as_view(), name="test_sessions"),

]
