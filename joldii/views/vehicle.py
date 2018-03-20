from __future__ import unicode_literals

from django.http import HttpResponse
from django.views import View

from joldii.constants import consts

from joldii.models import SessionModel
from joldii.models import VehicleClassModel

from joldii.responses.response_update_location import UpdateLocationResponse


class AddVehicle(View):

    @staticmethod
    def post(request):
        vehicle_class = VehicleClassModel(
            name=request.POST['name'],
            maximum_passenger=request.POST['max'],
            base_fare=request.POST['base'],
            per_kilometer_fare=request.POST['kilo'],
            per_minute_fare=request.POST['min']
        )
        vehicle_class.save()
        return HttpResponse('{"success":"added"}', content_type="application/json")
