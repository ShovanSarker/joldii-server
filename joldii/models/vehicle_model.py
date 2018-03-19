from django.db import models

from joldii.models import BaseModel
from joldii.models import DriverModel


class VehicleClassModel(BaseModel):

    name = models.TextField(max_length=128)
    maximum_passenger = models.IntegerField(default=1)
    base_fare = models.FloatField(default=0)
    per_kilometer_fare = models.FloatField(default=0)
    per_minute_fare = models.FloatField(default=0)

    class Meta:
        app_label = "joldii"
        db_table = "vehicle_class"


class VehicleModel(BaseModel):

    registration_number = models.TextField(max_length=128, unique=True)
    engine_number = models.TextField(max_length=128, null=True)
    chassis_number = models.TextField(max_length=128, null=True)
    registration_certificate_image = models.TextField(max_length=128, null=True)
    tax_token_image = models.TextField(max_length=128, null=True)
    insurance_image = models.TextField(max_length=128, null=True)
    color = models.TextField(max_length=128, null=True)
    ride_class = models.ForeignKey(VehicleClassModel, related_name='vehicle_model_ride_class')
    status = models.IntegerField(default=0, null=False)
    average_rating = models.FloatField(default=0)
    number_of_rides = models.IntegerField(default=0)

    driver = models.ManyToManyField(DriverModel, related_name='vehicle_model_driver')

    class Meta:
        app_label = "joldii"
        db_table = "vehicle"
