from base_response import Response
from ..constants import consts


class PromoResponse(Response):
    """
    Response object for pin_verification requests
    """

    def __init__(self, promo=None, error_code=None):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_PROMO)
        self.parse_response(promo, error_code)

    def parse_response(self, promo, error_code):
        if promo is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_MESSAGE, promo)
        else:
            if error_code is None:
                self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
            else:
                self.set_response(consts.PARAM_ERROR_CODE, error_code)

        print self.respond()
