from django.conf.urls import url

from dashboard.views import dashboard
from dashboard.views import login
from dashboard.views import users
from dashboard.views import rides
from dashboard.views import ride_detail
from dashboard.views import ride_settings
from dashboard.views import promo
from dashboard.views import accounts
from dashboard.views import user_directory
from dashboard.views import vehicle_list


urlpatterns = [

    url(r'^$', view=dashboard, name="dashboard"),
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
