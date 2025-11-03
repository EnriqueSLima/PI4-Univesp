# data_process/views.py

from django.http import JsonResponse
from django.views import View
from .services import OpenWeatherAirQuality
from .models import AirQualityData

from django.shortcuts import render


def get_station_coordinates():
    """Retorna as coordenadas das estações"""
    return [
        { 'coords': [-23.50455587377614, -46.62856773359203], 'nome' : 'Santana', 'estacao_id': '1'},
        { 'coords': [-23.65452312102595, -46.70995648887296], 'nome' : 'Santo Amaro', 'estacao_id': '2'},
        { 'coords': [-23.545735329390677, -46.62765280792035], 'nome' : 'Pq. Dom Pedro II', 'estacao_id': '3'},
        { 'coords': [-23.615943617970945, -46.663295450971994], 'nome' : 'Congonhas', 'estacao_id': '4'},
        { 'coords': [-23.585792325197616, -46.658413146546586], 'nome' : 'Ibirapuera', 'estacao_id': '5'},
        { 'coords': [-23.515542173706905, -46.72656563120576], 'nome' : 'Lapa', 'estacao_id': '6'},
        { 'coords': [-23.549287355222415, -46.60148160421932], 'nome' : 'Mooca', 'estacao_id': '7'},
        { 'coords': [-23.55391441958687, -46.67298963305492], 'nome' : 'Cerqueira César', 'estacao_id': '8'},
        { 'coords': [-23.56270064684056, -46.61263985588234], 'nome' : 'Cambuci', 'estacao_id': '9'},
        { 'coords': [-23.547325518021744, -46.64207690421932], 'nome' : 'Centro', 'estacao_id': '10'},
        { 'coords': [-23.566121466158865, -46.73809550680783], 'nome' : 'Cid.Universitária-USP-Ipen', 'estacao_id': '11'},
        { 'coords': [-23.47753959549242, -46.692138309772915], 'nome' : 'N.Senhora do Ó', 'estacao_id': '12'},
        { 'coords': [-23.58234192392213, -46.47046700421834], 'nome' : 'Itaquera', 'estacao_id': '13'},
        { 'coords': [-23.77645628706186, -46.69677564469008], 'nome' : 'Grajaú-Parelheiros', 'estacao_id': '14'},
        { 'coords': [-23.560924449393774, -46.70153337538319], 'nome' : 'Pinheiros', 'estacao_id': '15'},
        { 'coords': [-23.49890019033872, -46.4450417772355], 'nome' : 'S Miguel Paulista', 'estacao_id': '16'},
        { 'coords': [-23.680711167687296, -46.67579978588038], 'nome' : 'Interlagos', 'estacao_id': '17'},
        { 'coords': [-23.501541879266153, -46.42067224654922], 'nome' : 'Itaim Paulista', 'estacao_id': '18'},
        { 'coords': [-23.666353022636017, -46.7810391597671], 'nome' : 'Capão Redondo', 'estacao_id': '19'},
        { 'coords': [-23.518761440588285, -46.744062190727675], 'nome' : 'Marg.Tietê-Pte Remédios', 'estacao_id': '20'},
        { 'coords': [-23.457931652360394, -46.76675231176519], 'nome' : 'Pico do Jaraguá', 'estacao_id': '21'},
        { 'coords': [-23.41485503641999, -46.75647394840244], 'nome' : 'Perus', 'estacao_id': '22'},
        # ... adicione todas as outras estações
    ]

class CollectAirQualityData(View):
    def get(self, request):
        """Coleta dados de todas as estações"""
        weather_service = OpenWeatherAirQuality()
        stations = get_station_coordinates()
        results = []
        
        for station in stations:
            air_quality = weather_service.save_air_quality_data(station)
            if air_quality:
                results.append({
                    'station': station['nome'],
                    'aqi': air_quality.aqi,
                    'status': 'success'
                })
            else:
                results.append({
                    'station': station['nome'],
                    'status': 'error'
                })
        
        return JsonResponse({'results': results})

class GetStationData(View):
    def get(self, request, station_id):
        """Retorna dados específicos de uma estação"""
        try:
            # Pega o dado mais recente da estação
            data = AirQualityData.objects.filter(
                station_id=station_id
            ).latest('timestamp')
            
            return JsonResponse({
                'station_id': data.station_id,
                'station_name': data.station_name,
                'aqi': data.aqi,
                'aqi_description': data.get_aqi_description(),
                'aqi_color': data.get_aqi_color(),
                'pollutants': {
                    'co': data.co,
                    'no2': data.no2,
                    'o3': data.o3,
                    'so2': data.so2,
                    'pm2_5': data.pm2_5,
                    'pm10': data.pm10
                },
                'timestamp': data.timestamp.isoformat()
            })
        except AirQualityData.DoesNotExist:
            return JsonResponse({'error': 'Dados não encontrados'}, status=404)
