"""
Parameters
"""
PARAM_ACTION = "action"
PARAM_SUCCESS = "success"
PARAM_ERROR_CODE = "rc"
PARAM_PHONE = "phone"
PARAM_PASSWORD = "password"
PARAM_NEW_PASSWORD = "new_password"
PARAM_SESSION_ID = "sid"
PARAM_USER_TYPE = "utype"
PARAM_USER_PIN = "pin"
PARAM_USER_NAME = "name"
PARAM_USER_MAIL = "email"
PARAM_USER_ADDRESS = "user_address"
PARAM_USER_PIC = "user_pic"
PARAM_USER_VERIFIED = "is_verified"
PARAM_PROMO_CODE = "promo_code"
PARAM_MESSAGE = "msg"
PARAM_LATITUDE = "lat"
PARAM_LONGITUDE = "lng"
PARAM_LAT_FROM = "lat_from"
PARAM_LAT_TO = "lat_to"
PARAM_LNG_FROM = "long_from"
PARAM_LNG_TO = "long_to"
PARAM_DRIVER_NAME = "driver_name"
PARAM_DRIVER_PHONE = "driver_phone"
PARAM_DRIVER_LICENSE = "driver_license"
PARAM_VEHICLE_NAME = "vehicle_name"
PARAM_VEHICLE_NUMBER = "vehicle_number"
PARAM_VEHICLE_TYPE = "vehicle_type"
PARAM_VEHICLE_CAPACITY = "vehicle_capacity"
PARAM_RIDE_FARE = "fair"
PARAM_FARE_LIST = "fairs"
PARAM_HISTORY = "histories"
PARAM_DRIVER_SESSION = "d_sid"
PARAM_DATE = "date"
PARAM_HISTORICAL_FARE = "fair"
PARAM_LOCATION_FROM = "from"
PARAM_LOCATION_TO = "to"
PARAM_TRIP_SNAP = "trip_snap"
PARAM_APP_TYPE = "app_type"
PARAM_DATA = "data"

"""
Actions
"""
ACTION_LOGIN = "0001"
ACTION_PIN_VERIFICATION = "0002"
ACTION_REGISTER = "0003"
ACTION_FORGET_PASSWORD = "0004"
ACTION_PROMO = "0005"
ACTION_CHANGE_NAME = "0006"
ACTION_CHANGE_EMAIL = "0007"
ACTION_CHANGE_PHONE = "0008"
ACTION_RIDE_REQUEST = "0009"
ACTION_RIDE_STARTED = "0010"
ACTION_RIDE_ENDED = "0011"
ACTION_UPDATE_FARE = "0012"
ACTION_VIEW_HISTORY = "0013"

"""
Error Codes
"""
ERROR_UNKNOWN = 5000
ERROR_USER_PRESENT = 5001
ERROR_PROMO_ALREADY_USED = 5002
ERROR_PROMO_INVALID = 5003
ERROR_SESSION_INVALID = 5004
ERROR_DRIVER_NOT_FOUND = 5005
ERROR_NO_HISTORY = 5006
ERROR_INCORRECT_PARAMETERS = 5007

"""
User Tyoe
"""
TYPE_USER_ADMIN = 0
TYPE_USER_RIDER = 1
TYPE_USER_DRIVER = 2
TYPE_USER_RIDER_DRIVER = 3

"""
Driver Status
"""
STATUS_NOT_DRIVER = -1
STATUS_DRIVER_OFFLINE = 0
STATUS_DRIVER_IN_RIDE = 1
STATUS_DRIVER_BOOKED = 2
STATUS_DRIVER_ONLINE = 3

"""
Order Status
"""
STATUS_ORDER_UNCONFIRMED = 0
STATUS_ORDER_CONFIRMED = 1
STATUS_ORDER_STARTED = 2
STATUS_ORDER_COMPLETED = 3
STATUS_ORDER_REJECTED = 4
STATUS_ORDER_CANCEL_REQ = 5
STATUS_ORDER_CANCELLED = 6

"""
Ride Class
"""
RIDE_CLASS_BIKE = 0
RIDE_CLASS_CAR_PREMIUM = 1
RIDE_CLASS_CAR_NORMAL = 2


# class RideClass():
#
#     ride_class = {
#         'Bike': 1,
#         'Premium Car': 2,
#         'Normal Car': 3
#     }
