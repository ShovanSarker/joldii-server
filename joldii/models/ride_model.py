from django.db import models

from joldii.models import BaseModel
from joldii.models.user_model import UserModel
from joldii.models import DriverModel


class RideModel(BaseModel):

    user = models.ForeignKey(UserModel, related_name='ride_model_user')
    driver = models.ForeignKey(DriverModel, related_name='ride_model_driver')
    pickup_lat = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    pickup_lon = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    drop_lat = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    drop_lon = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    path = models.CharField(max_length=1024, null=True, blank=True)
    distance = models.FloatField(default=0)
    duration = models.BigIntegerField(default=0)
    base_fare = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    total_bill = models.FloatField(default=0)
    order_status = models.IntegerField(default=0)

    class Meta:
        app_label = "joldii"
        db_table = "ride"
