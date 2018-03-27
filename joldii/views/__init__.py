from joldii.views.map import UploadLocation
from joldii.views.session import Login
from joldii.views.session import Register
from joldii.views.vehicle import AddVehicle
from joldii.views.map import GetRideInformation
from joldii.views.promo import AddPromo
from joldii.views.promo import RedeemPromo

from joldii.views.test import Users
from joldii.views.test import SessionList

__all__ = ["Register",
           "Login",
           "UploadLocation",
           "AddVehicle",
           "GetRideInformation",
           "AddPromo",
           "RedeemPromo",

           "Users",
           "SessionList"
           ]
