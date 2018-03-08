from django.conf.urls import url

from joldii.views import APIRouter

urlpatterns = [
    url(r'^v1/$', view=APIRouter.as_view(), name="api_router"),
]
