from base_response import Response
from ..constants import consts


class ChangePhoneResponse(Response):
    """
    Response object for pin_verification requests
    """

    def __init__(self, state=False):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_CHANGE_PHONE)
        self.parse_response(pin)

    def parse_response(self, state):
        if state is True:
            self.set_status(Response.STATE_SUCCESS)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)

        print self.respond()
