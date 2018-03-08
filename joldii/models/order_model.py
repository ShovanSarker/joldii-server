from decimal import getcontext

from django.db import models

from base_model import BaseModel
from driver_model import DriverModel
from user_model import UserModel


class OrderModel(BaseModel):
    getcontext().prec = 14

    ord_user = models.ForeignKey(UserModel)
    start_lat = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    start_lon = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    end_lat = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    end_lon = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    predicted_distance = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    actual_distance = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    final_end_lat = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)
    final_end_lon = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)

    driver = models.ForeignKey(DriverModel)
    bill = models.DecimalField(default=0.0, max_digits=14, decimal_places=7, null=False)

    status = models.IntegerField(default=0, null=False)

    class Meta:
        app_label = "chander_gari"
        db_table = "order"

    @staticmethod
    def find_driver(lat, lon):
        radius = 5 * 0.01449
        drivers = DriverModel.find_nearby_drivers(float(lat), float(lon), radius)
        if len(drivers) > 0:
            return drivers[0]
        else:
            return None
