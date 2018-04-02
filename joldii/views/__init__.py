from joldii.views.map import UploadLocation
from joldii.views.session import Login
from joldii.views.session import Register
from joldii.views.vehicle import AddVehicle
from joldii.views.map import GetRideInformation
from joldii.views.promo import AddPromo
from joldii.views.promo import RedeemPromo
from joldii.views.trip import SearchRide
from joldii.views.trip import StartTrip
from joldii.views.trip import EndTrip
from joldii.views.trip import PartnerPosition
from joldii.views.trip import ToggleDriverStatus
from joldii.views.trip import NotifyDriver
from joldii.views.trip import NotifyUser
from joldii.views.session import UploadDriverInfo

from joldii.views.test import Users
from joldii.views.test import SessionList

from joldii.views.web import dashboard
from joldii.views.web import login
from joldii.views.web import users
from joldii.views.web import rides
from joldii.views.web import ride_detail
from joldii.views.web import ride_settings
from joldii.views.web import promo
from joldii.views.web import accounts
from joldii.views.web import user_directory
from joldii.views.web import vehicle_list

__all__ = ["Register",
           "Login",
           "dashboard",
           "login",
           "users",
           "rides",
           "ride_detail",
           "ride_settings",
           "promo",
           "accounts",
           "user_directory",
           "vehicle_list",
           "UploadLocation",
           "AddVehicle",
           "GetRideInformation",
           "AddPromo",
           "RedeemPromo",
           "SearchRide",
           "StartTrip",
           "EndTrip",
           "PartnerPosition",
           "ToggleDriverStatus",
           "UploadDriverInfo",
           "NotifyDriver",
           "NotifyUser",
           "Users",
           "SessionList"
           ]
