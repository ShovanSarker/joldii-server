import random
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import models

from base_model import BaseModel


class UserModel(BaseModel):
    username = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=32, null=True, unique=True)
    password = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=256, null=True)
    user_type = models.IntegerField(default=0, null=False)
    is_active = models.BooleanField(default=False)
    user_picture = models.CharField(max_length=128, null=True)
    average_rating = models.FloatField(default=0)
    number_of_rides = models.IntegerField(default=0)

    class Meta:
        app_label = "joldii"
        db_table = "user"

    def save(self, *args, **kwargs):
        super(UserModel, self).save(*args, **kwargs)


    @staticmethod
    def create_random_password(size=5, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def encrypt_password(password):
        return make_password(password, settings.SECRET_KEY)

    @staticmethod
    def get_user_by_phone_password(phone, password=None):
        try:
            if password is not None:
                password = make_password(password, settings.SECRET_KEY)
                user = UserModel.objects.get(phone=phone, password=password)
                return user
            else:
                user = UserModel.objects.get(phone=phone)
                return user
        except UserModel.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_phone_password_type(phone, password=None, user_type=None):
        try:
            if password is not None and user_type is not None:
                password = make_password(password, settings.SECRET_KEY)
                user = UserModel.objects.get(phone=phone, password=password, user_type=user_type)
                return user
            elif password is not None:
                password = make_password(password, settings.SECRET_KEY)
                user = UserModel.objects.get(phone=phone, password=password)
                return user
            elif user_type is not None:
                user = UserModel.objects.get(phone=phone, user_type=user_type)
                return user
            else:
                user = UserModel.objects.get(phone=phone)
                return user
        except UserModel.DoesNotExist:
            return None

