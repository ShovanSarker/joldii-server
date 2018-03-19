from base_response import Response
from joldii.models import SessionModel
from ..constants import consts


class RegisterResponse(Response):
    """
    Response object for register requests
    """

    def __init__(self, user=None, verified=False):
        self.status = Response.STATE_FAIL
        self.response = {}
        self.parse_user(user, verified)

    def parse_user(self, user, verified=False):
        sid = None
        self.set_response(consts.PARAM_USER_VERIFIED, verified)
        if user is not None:
            sid = SessionModel.get_session(user)
            username = user.username
            email = user.email
            pic = user.user_picture
            self.set_response(consts.PARAM_USER_NAME, username)
            self.set_response(consts.PARAM_USER_MAIL, email)
            self.set_response(consts.PARAM_USER_PIC, pic)
        if sid is not None:
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_SESSION_ID, sid)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
