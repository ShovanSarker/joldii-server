from base_response import Response
from ..constants import consts


class GetRideInfoResponse(Response):
    """
    Response object for fail requests
    """
    def __init__(self, data):
        self.status = Response.STATE_SUCCESS
        self.response = {}
        self.get_ride_info(data)

    def get_ride_info(self, data):
        self.set_response(consts.PARAM_DATA, data)
