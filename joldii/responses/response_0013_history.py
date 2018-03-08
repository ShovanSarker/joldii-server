from base_response import Response
from ..constants import consts


class ViewHistoryResponse(Response):
    """
    Response object for ride requests
    """

    def __init__(self, history=None):
        self.set_response(consts.PARAM_ACTION, consts.ACTION_VIEW_HISTORY)
        self.parse_response(history)

    def parse_response(self, history):
        if history is not None:
            if len(history) > 0:
                self.set_status(Response.STATE_SUCCESS)
                self.set_response(consts.PARAM_HISTORY, history)
            else:
                self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_NO_HISTORY)
        else:
            self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_UNKNOWN)

        print self.respond()
