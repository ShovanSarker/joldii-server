from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View


def dashboard(request):
    context = {'page_dashboard': "active"}
    return render(request, 'dashboard.html', context)


def login(request):
    context = {'page' : "Login"}
    return render(request, 'login.html', context)


def users(request):
    context = {'page_users': "active"}
    return render(request, 'users.html', context)


def rides(request):
    context = {'page_rides': "active"}
    return render(request, 'rides.html', context)


def ride_detail(request):
    context = {'page_detail': "active"}
    return render(request, 'ride_detail.html', context)


def ride_settings(request):
    context = {'page_settings': "active"}
    return render(request, 'ride_settings.html', context)


def promo(request):
    context = {'page_promo': "active"}
    return render(request, 'coupon.html', context)


def accounts(request):
    context = {'page_accounts': "active"}
    return render(request, 'accounts.html', context)


def user_directory(request):
    context = {'page_userdir' : "active"}
    return render(request, 'users_app.html', context)


def vehicle_list(request):
    context = {'page_vehicle' : "active"}
    return render(request, 'vehicle_list.html', context)


