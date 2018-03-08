from base_response import Response
from ..constants import consts


class PinVerificationResponse(Response):
    """
    Response object for pin_verification requests
    """

    def __init__(self, pin=None, error_code=None):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_PIN_VERIFICATION)
        self.parse_response(pin, error_code)

    def parse_response(self, pin, error_code):
        if pin is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_USER_PIN, pin)
        else:
            if error_code is None:
                self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
            else:
                self.set_response(consts.PARAM_ERROR_CODE, error_code)

        print self.respond()
