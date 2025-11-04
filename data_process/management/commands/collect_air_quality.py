# data_process/management/commands/collect_air_quality.py
from django.core.management.base import BaseCommand
from data_process.services import OpenWeatherAirQuality
from data_process.views import get_station_coordinates

# Função para coleta dos parâmetros correntes
class Command(BaseCommand):
    help = 'Coleta dados de qualidade do ar para todas as estações'
    
    def handle(self, *args, **options):
        weather_service = OpenWeatherAirQuality()
        stations = get_station_coordinates()
        
        self.stdout.write('Coletando dados de qualidade do ar...')
        
        for station in stations:
            result = weather_service.save_air_quality_data(station)
            if result:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Dados coletados para {station['nome']} - AQI: {result.aqi}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Erro ao coletar dados para {station['nome']}"
                    )
                )