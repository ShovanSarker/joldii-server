from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register

urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),
]
