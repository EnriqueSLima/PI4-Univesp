# data_process/services.py

#import requests
#from django.conf import settings
#from .models import AirQualityData

# data_process/services.py

import requests
from django.conf import settings
from .models import AirQualityData
from datetime import datetime, timedelta
import time

def collect_historical_data_single_station(station_data, days=5):
    """
    Coleta dados históricos para UMA única estação
    station_data: dict com 'coords', 'nome', 'estacao_id'
    days: número de dias para buscar (padrão: 5)
    """
    
    # Configurações
    API_KEY = settings.OPENWEATHER_API_KEY
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    
    # Extrair dados da estação
    lat, lon = station_data['coords']
    station_name = station_data['nome']
    station_id = station_data['estacao_id']
    
    print(f"Coletando dados históricos para {station_name}...")
    
    # Calcular timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    print(f"Período: {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}")
    
    # Construir URL
    url = f"{BASE_URL}?lat={lat}&lon={lon}&start={start_timestamp}&end={end_timestamp}&appid={API_KEY}"
    
    print(f"URL da requisição: {url}")
    
    try:
        # Fazer requisição
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            saved_count = 0
            
            if 'list' in data and len(data['list']) > 0:
                print(f"Encontrados {len(data['list'])} registros na API")
                
                for item in data['list']:
                    # Converter timestamp
                    timestamp = datetime.fromtimestamp(item['dt'])
                    
                    # Verificar se já existe
                    exists = AirQualityData.objects.filter(
                        station_id=station_id,
                        timestamp=timestamp
                    ).exists()
                    
                    if not exists:
                        # Salvar no banco
                        air_data = AirQualityData(
                            station_id=station_id,
                            station_name=station_name,
                            latitude=lat,
                            longitude=lon,
                            aqi=item['main']['aqi'],
                            co=item['components']['co'],
                            no=item['components']['no'],
                            no2=item['components']['no2'],
                            o3=item['components']['o3'],
                            so2=item['components']['so2'],
                            pm2_5=item['components']['pm2_5'],
                            pm10=item['components']['pm10'],
                            nh3=item['components']['nh3'],
                            timestamp=timestamp
                        )
                        air_data.save()
                        saved_count += 1
                        print(f"✓ Salvo: {timestamp.strftime('%d/%m/%Y %H:%M')} - AQI: {item['main']['aqi']}")
                    else:
                        print(f"⏭️  Já existe: {timestamp.strftime('%d/%m/%Y %H:%M')}")
                
                print(f"✅ Finalizado {station_name}: {saved_count} novos registros salvos")
                return saved_count
            else:
                print(f"❌ Nenhum dado encontrado na API para {station_name}")
                return 0
        else:
            print(f"❌ Erro na API: {response.status_code} - {response.text}")
            return 0
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return 0

class OpenWeatherAirQuality:
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
    
    def get_air_quality(self, lat, lon):
        """Obtém dados de qualidade do ar para coordenadas específicas"""
        url = f"{self.BASE_URL}?lat={lat}&lon={lon}&appid={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def save_air_quality_data(self, station_data):
        """Salva os dados de qualidade do ar no banco"""
        lat, lon = station_data['coords']
        station_name = station_data['nome']
        station_id = station_data['estacao_id']
        
        # Obter dados da API
        api_data = self.get_air_quality(lat, lon)
        
        if api_data and 'list' in api_data and len(api_data['list']) > 0:
            air_data = api_data['list'][0]
            components = air_data['components']
            main_aqi = air_data['main']['aqi']
            
            # Salvar no banco
            air_quality = AirQualityData(
                station_id=station_id,
                station_name=station_name,
                latitude=lat,
                longitude=lon,
                aqi=main_aqi,
                co=components.get('co', 0),
                no=components.get('no', 0),
                no2=components.get('no2', 0),
                o3=components.get('o3', 0),
                so2=components.get('so2', 0),
                pm2_5=components.get('pm2_5', 0),
                pm10=components.get('pm10', 0),
                nh3=components.get('nh3', 0)
            )
            air_quality.save()
            return air_quality
        
        return None