from base_response import Response
from ..constants import consts


class UpdateLocationResponse(Response):
    """
    Response object for forget_password requests
    """

    def __init__(self):
        self.status = Response.STATE_FAIL
        self.response = {}

    def parse_response(self, state):
        if state is True:
            self.set_status(Response.STATE_SUCCESS)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)

        print self.respond()
