import json

from ..constants import consts


class Response(object):
    STATE_SUCCESS = "true"
    STATE_FAIL = "false"

    def __init__(self):
        self.status = Response.STATE_FAIL
        self.response = {}

    def set_status(self, status):
        self.status = status

    def set_response(self, key, value):
        self.response[key] = value

    def respond(self):
        final_response = self.response
        final_response[consts.PARAM_SUCCESS] = self.status
        print json.dumps(final_response)
        return json.dumps(final_response)
