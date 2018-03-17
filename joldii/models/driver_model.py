from django.db import models

from base_model import BaseModel
from user_model import UserModel


class DriverModel(BaseModel):

    user = models.ForeignKey(UserModel, related_name='driver_model_user')
    national_id = models.TextField(max_length=128, null=True)
    driving_license = models.TextField(max_length=128, null=True)
    driving_license_image = models.TextField(max_length=128, null=True)
    status = models.IntegerField(default=0, null=False)
    average_rating = models.FloatField(default=0)
    number_of_rides = models.IntegerField(default=0)

    class Meta:
        app_label = "joldii"
        db_table = "driver"
