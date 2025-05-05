from django.contrib import admin
from django.urls import include, path
from .views import admin_dashboard
# from commulink import firtsApp

urlpatterns = [
    path("dashboard/", admin_dashboard, name='admin_dashboard'),
]
