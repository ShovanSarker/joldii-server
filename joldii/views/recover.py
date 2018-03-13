from __future__ import unicode_literals

from django.views import View

from joldii.actions import user_session


class Recover(View):
    @staticmethod
    def post(request):
        return user_session.register(request)
