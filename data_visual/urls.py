from django.urls import path
from . import views

urlpatterns = [
    path('', views.sp_map_dashboard, name='dashboard'),
    #path('debug/', views.geojson_debug, name='debug'), # Debug de distritos e subprefeituras
    #path('ciclovias-debug/', views.ciclovias_debug, name='ciclovias_debug'),  # Debug de ciclovias
]