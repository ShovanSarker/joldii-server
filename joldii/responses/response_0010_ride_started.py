from base_response import Response
from ..constants import consts


class RideStartedResponse(Response):
    """
    Response object for ride requests
    """

    def __init__(self, status=False):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_RIDE_STARTED)
        self.parse_response(status)

    def parse_response(self, status):
        if status is True:
            self.set_status(Response.STATE_SUCCESS)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)

        print self.respond()
