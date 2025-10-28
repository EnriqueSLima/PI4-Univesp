from django.urls import path
from . import views

urlpatterns = [
    path('', views.sp_map_dashboard, name='dashboard'),
]