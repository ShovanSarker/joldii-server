from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register
from joldii.views import Recover

urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),
    url(r'^recover', view=Recover.as_view(), name="recover"),
]
