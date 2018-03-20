from base_response import Response
from ..constants import consts


class GetRideInfo(Response):
    """
    Response object for fail requests
    """
    def __init__(self, data):
        self.status = Response.STATE_SUCCESS
        self.response = {}
        self.get_ride_info()

    def incorrect_parameters(self):
        self.set_response(consts.PARAM_DATA, consts.ERROR_INCORRECT_PARAMETERS)
