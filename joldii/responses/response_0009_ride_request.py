from base_response import Response
from ..constants import consts


class RideRequestResponse(Response):
    """
    Response object for ride requests
    """

    def __init__(self, driver=None, error_code=None):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_RIDE_REQUEST)
        self.parse_response(driver, error_code)

    def parse_response(self, driver, error_code):
        if driver is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_DRIVER_NAME, consts.ERROR_UNKNOWN)
            self.set_response(consts.PARAM_DRIVER_PHONE, consts.ERROR_UNKNOWN)
            self.set_response(consts.PARAM_VEHICLE_NAME, consts.ERROR_UNKNOWN)
            self.set_response(consts.PARAM_VEHICLE_NUMBER, consts.ERROR_UNKNOWN)
        else:
            if error_code is None:
                self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
            else:
                self.set_response(consts.PARAM_ERROR_CODE, error_code)

        print self.respond()
