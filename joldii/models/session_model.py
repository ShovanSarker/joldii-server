import random
import string

from django.db import models

from base_model import BaseModel
from user_model import UserModel


class SessionModel(BaseModel):
    session_id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(UserModel)

    def save(self, *args, **kwargs):
        size = 15
        chars = string.ascii_uppercase + string.digits
        random_token = ''.join(random.choice(chars) for _ in range(size))
        self.session_id = random_token
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

    class Meta:
        app_label = "chander_gari"
        db_table = "session"
