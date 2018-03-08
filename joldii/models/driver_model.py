from decimal import getcontext

from django.db import models

from base_model import BaseModel
from user_model import UserModel


class DriverModel(BaseModel):
    getcontext().prec = 14

    user = models.ForeignKey(UserModel)
    vehicle_num = models.TextField(max_length=128, null=True)
    vehicle_name = models.TextField(max_length=128, null=True)
    license_num = models.TextField(max_length=128, null=True)

    national_id = models.TextField(max_length=128, null=True)

    curr_lat = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    curr_lon = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    status = models.IntegerField(default=0, null=False)

    driver_rating = models.DecimalField(default=2.5, max_digits=3, decimal_places=2)

    class Meta:
        app_label = "joldii"
        db_table = "driver"

    @staticmethod
    def find_nearby_drivers(lat, lon, dist):
        min_lat = lat - dist
        max_lat = lat + dist
        min_lon = lon - dist
        max_lon = lon + dist
        drivers = DriverModel.objects.filter(curr_lat__range=(min_lat, max_lat),
                                             curr_lon__range=(min_lon, max_lon),
                                             status=3
                                             )
        return drivers
