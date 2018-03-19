from django.db import models

from joldii.models import BaseModel
from joldii.models import UserModel
from joldii.models import VehicleClassModel


class PromoModel(BaseModel):

    name = models.TextField(max_length=128)
    vehicle_type = models.ForeignKey(VehicleClassModel, related_name='promo_model_vehicle_class')
    maximum_number_of_discount = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    promo_active = models.BooleanField(default=True)

    class Meta:
        app_label = "joldii"
        db_table = "promo"


class UserPromoModel(BaseModel):

    user = models.ForeignKey(UserModel, related_name='user_promo_model_user')
    promo = models.ForeignKey(PromoModel, related_name='user_promo_model_promo')
    remaining_ride = models.IntegerField(default=0)

    class Meta:
        app_label = "joldii"
        db_table = "user_with_promo"
