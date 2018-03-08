from base_response import Response
from ..constants import consts


class LoginResponse(Response):
    """
    Response object for login requests
    """

    def __init__(self, user=None):
        self.status = Response.STATE_FAIL
        self.response = {}
        self.parse_user(user)

    def parse_user(self, user):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_LOGIN)
        if user is not None:
            username = user.username
            email = user.email
            pic = user.user_picture
            sid = user.get_session()
            self.set_status(Response.STATE_SUCCESS)
            self.set_response(consts.PARAM_SESSION_ID, sid)
            self.set_response(consts.PARAM_USER_NAME, username)
            self.set_response(consts.PARAM_USER_MAIL, email)
            self.set_response(consts.PARAM_USER_PIC, pic)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)
