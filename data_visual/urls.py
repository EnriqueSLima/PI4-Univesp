from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.sp_map_dashboard, name='dashboard'),
    path('api/estacao/<str:station_id>/', views.get_estacao_data, name='estacao_data'),
    path('api/dados-dia/<str:station_id>/', views.get_dados_dia, name='dados_dia'),
]