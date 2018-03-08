from base_response import Response
from ..constants import consts


class RegisterResponse(Response):
    """
    Response object for register requests
    """

    def __init__(self, user=None):
        self.status = Response.STATE_FAIL
        self.response = {}
        self.set_response(consts.PARAM_ACTION, consts.ACTION_REGISTER)
        self.parse_user(user)

    def parse_user(self, user):
        sid = None
        if user is not None:
            sid = user.get_session()
        if sid is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_SESSION_ID, sid)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
