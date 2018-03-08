from base_response import Response
from ..constants import consts


class UpdateFareResponse(Response):
    """
    Response object for ride requests
    """

    def __init__(self, fares=None):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_UPDATE_FARE)
        self.parse_response(fares)

    def parse_response(self, fares):
        if fares is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_FARE_LIST, fares)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)

        print self.respond()
