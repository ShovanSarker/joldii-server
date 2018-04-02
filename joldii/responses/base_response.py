import json

from ..constants import consts


class Response(object):
    STATE_SUCCESS = "success"
    STATE_FAIL = "fail"

    def __init__(self):
        self.status = Response.STATE_FAIL
        self.response = {}

    def set_status(self, status):
        self.status = status

    def set_response(self, key, value):
        self.response[key] = value

    def respond(self):
        final_response = self.response
        final_response[consts.STATUS] = self.status
        print json.dumps(final_response)
        return json.dumps(final_response)


    #
    #     def set_status(self, status):
    #     self.status = status
    #
    # def set_reason(self, key, value):
    #     self.response[key] = value
    #
    # def set_data(self, key, value):
    #     self.response[key] = value
    #
    # def set_error_code(self, key, value):
    #     self.response[key] = value
    #
    # def respond(self):
    #     final_response = self.response
    #     print(final_response)
    #     final_response[consts.PARAM_SUCCESS] = self.status
    #     # print json.dumps(final_response)
    #     return json.dumps(final_response)
