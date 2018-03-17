from django.db import models

from joldii.models import BaseModel
from joldii.models.user_model import UserModel
from joldii.models.ride_model import RideModel


from joldii.utils import UUID


class SessionModel(BaseModel):
    session_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(UserModel, related_name='session_user_user')
    current_lat = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    current_lon = models.DecimalField(default=0, max_digits=19, decimal_places=10)
    current_ride = models.ForeignKey(RideModel, null=True, blank=True, related_name='session_model_current_ride')
    is_driver = models.BooleanField(default=False)
    driver_status = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "joldii"
        db_table = "session"

    def save(self, *args, **kwargs):
        self.session_id = UUID.uuid_generator()
        super(SessionModel, self).save(*args, **kwargs)

    @staticmethod
    def cleanup_session(uid):
        try:
            session = SessionModel.objects.get(user=uid)
            session.delete()
        except SessionModel.DoesNotExist:
            return

    @staticmethod
    def get_user_by_session(session_id):
        try:
            session = SessionModel.objects.get(pk=session_id)
            return session.user
        except SessionModel.DoesNotExist:
            return None

    @staticmethod
    def get_session(user):
        try:
            session = SessionModel.objects.get(user=user)
        except SessionModel.DoesNotExist:
            session = SessionModel(user=user)
            session.save()
        return session.session_id
