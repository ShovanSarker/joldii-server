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
from joldii.views.session import UploadVehicleInfo
from joldii.views.session import GetVehicleInfo

from joldii.views.test import Users
from joldii.views.test import SessionList

__all__ = ["Register",
           "Login",
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
           "UploadVehicleInfo",
           "GetVehicleInfo",
           "NotifyDriver",
           "NotifyUser",

           "Users",
           "SessionList"
           ]
