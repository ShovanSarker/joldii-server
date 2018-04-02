from django.db import models

from joldii.models import BaseModel
from joldii.models import UserModel
from joldii.models import DriverModel
from joldii.models.ride_model import RideModel


class UserRatingModel(BaseModel):

    user = models.ForeignKey(UserModel, related_name='user_rating_model_user')
    driver = models.ForeignKey(DriverModel, related_name='user_rating_model_driver')
    rating = models.IntegerField(default=0)
    ride = models.ForeignKey(RideModel, related_name='user_rating_model_ride')
    comment = models.TextField()

    class Meta:
        app_label = "joldii"
        db_table = "user_rating"


class DriverRatingModel(BaseModel):

    user = models.ForeignKey(UserModel, related_name='driver_rating_model_user')
    driver = models.ForeignKey(DriverModel, related_name='driver_rating_model_driver')
    rating = models.IntegerField(default=0)
    ride = models.ForeignKey(RideModel, related_name='driver_rating_model_ride')
    comment = models.TextField()

    class Meta:
        app_label = "joldii"
        db_table = "driver_rating"
