from django.db import models

from joldii.models import BaseModel
from joldii.models.user_model import UserModel
from joldii.models import DriverModel
from joldii.models.vehicle_model import VehicleClassModel
from joldii.models.vehicle_model import VehicleModel

from joldii.utils import UUID


class RideModel(BaseModel):
    ride_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(UserModel, related_name='ride_model_user')
    driver = models.ForeignKey(DriverModel, related_name='ride_model_driver', null=True, blank=True)
    vehicle_class = models.ForeignKey(VehicleClassModel, related_name='vehicle_class_model', null=True, blank=True)
    vehicle = models.ForeignKey(VehicleModel, related_name='vehicle_model', null=True, blank=True)
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
    time_start = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)

    class Meta:
        app_label = "joldii"
        db_table = "ride"

    def save(self, *args, **kwargs):
        if not RideModel.objects.filter(pk=self.ride_id).exists():
            self.ride_id = UUID.uuid_generator()
        super(RideModel, self).save(*args, **kwargs)
