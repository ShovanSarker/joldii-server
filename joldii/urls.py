from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register

from joldii.views import UploadLocation
from joldii.views import AddVehicle
from joldii.views import GetRideInformation
from joldii.views import AddPromo
from joldii.views import RedeemPromo
from joldii.views import SearchRide
from joldii.views import StartTrip
from joldii.views import EndTrip
from joldii.views import UserCancelRide
from joldii.views import DriverCancelRide
from joldii.views import PartnerPosition
from joldii.views import ToggleDriverStatus
from joldii.views import UploadDriverInfo
from joldii.views import UploadVehicleInfo
from joldii.views import NotifyDriver
from joldii.views import NotifyUser
from joldii.views import GetVehicleInfo
from joldii.views import GetHistory
from joldii.views import RateUser
from joldii.views import RateDriver

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
    url(r'^upload_driver_info', view=UploadDriverInfo.as_view(), name="upload_driver_info"),
    url(r'^upload_vehicle_info', view=UploadVehicleInfo.as_view(), name="upload_vehicle_info"),
    url(r'^notify_driver', view=NotifyDriver.as_view(), name="notify_driver"),
    url(r'^notify_user', view=NotifyUser.as_view(), name="notify_user"),
    url(r'^get_vehicle_info', view=GetVehicleInfo.as_view(), name="get_vehicle_info"),
    url(r'^rate_user', view=RateUser.as_view(), name="rate_user"),
    url(r'^rate_driver', view=RateDriver.as_view(), name="rate_driver"),

    url(r'^order_ride', view=SearchRide.as_view(), name="order_ride"),
    url(r'^start_ride', view=StartTrip.as_view(), name="start_ride"),
    url(r'^end_ride', view=EndTrip.as_view(), name="end_ride"),
    url(r'^get_history', view=GetHistory.as_view(), name="get_history"),
    url(r'^user_cancel_ride', view=UserCancelRide.as_view(), name="user_cancel_ride"),
    url(r'^driver_cancel_ride', view=DriverCancelRide.as_view(), name="driver_cancel_ride"),
    url(r'^partner_position', view=PartnerPosition.as_view(), name="partner_position"),
    url(r'^driver_status', view=ToggleDriverStatus.as_view(), name="driver_status"),
    url(r'^test/users', view=Users.as_view(), name="test_users"),
    url(r'^test/sessions', view=SessionList.as_view(), name="test_sessions"),

]
