from base_response import Response
from ..constants import consts


class IncorrectParametersResponse(Response):
    """
    Response object for fail requests
    """

    def incorrect_parameters(self):
        self.set_response(consts.PARAM_ERROR_CODE, consts.ERROR_INCORRECT_PARAMETERS)
