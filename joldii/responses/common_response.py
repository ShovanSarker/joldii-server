from base_response import Response
from joldii.models import SessionModel
from ..constants import consts


class CommonResponse(Response):
    """
    Response object for all requests
    """

    def __init__(self, success=True, reason='', data=None, error_code=2000):

        if success:
            self.status = Response.STATE_SUCCESS
        else:
            self.status = Response.STATE_FAIL

        self.response = {}
        self.set_response(consts.REASON, reason)
        self.set_response(consts.DATA, data)
        self.set_response(consts.ERROR_CODE, error_code)


