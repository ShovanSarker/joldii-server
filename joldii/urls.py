from django.conf.urls import url

from joldii.views import Login
from joldii.views import Register
from joldii.views import dashboard
from joldii.views import login
from joldii.views import users
from joldii.views import rides
from joldii.views import ride_detail
from joldii.views import ride_settings
from joldii.views import promo
from joldii.views import accounts
from joldii.views import user_directory
from joldii.views import vehicle_list


urlpatterns = [
    url(r'^register', view=Register.as_view(), name="register"),
    url(r'^login', view=Login.as_view(), name="login"),
    url(r'^dashboard', view=dashboard, name="dashboard"),
    url(r'^log', view=login, name="login"),
    url(r'^users', view=users, name="users"),
    url(r'^rides', view=rides, name="rides"),
    url(r'^ride_detail', view=ride_detail, name="ride_detail"),
    url(r'^ride_settings', view=ride_settings, name="ride_settings"),
    url(r'^promo', view=promo, name="promo"),
    url(r'^accounts', view=accounts, name="accounts"),
    url(r'^user_directory', view=user_directory, name="user_directory"),
    url(r'^vehicle_list', view=vehicle_list, name="vehicle_list"),
]
