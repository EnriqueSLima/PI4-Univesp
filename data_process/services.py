# data_process/services.py
import requests
from django.conf import settings
from .models import AirQualityData
from datetime import datetime, timedelta
import time

# Função para uso da chave da API
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

def collect_historical_data_all_stations(days=7, delay_between_requests=1.0):
    # Configurações da chave
    API_KEY = settings.OPENWEATHER_API_KEY
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    
    # Lista de estações
    all_stations = [
        {'coords': [-23.50455587377614, -46.62856773359203], 'nome': 'Santana', 'estacao_id': '1'},
        {'coords': [-23.65452312102595, -46.70995648887296], 'nome': 'Santo Amaro', 'estacao_id': '2'},
        {'coords': [-23.545735329390677, -46.62765280792035], 'nome': 'Pq. Dom Pedro II', 'estacao_id': '3'},
        {'coords': [-23.615943617970945, -46.663295450971994], 'nome': 'Congonhas', 'estacao_id': '4'},
        {'coords': [-23.585792325197616, -46.658413146546586], 'nome': 'Ibirapuera', 'estacao_id': '5'},
        {'coords': [-23.515542173706905, -46.72656563120576], 'nome': 'Lapa', 'estacao_id': '6'},
        {'coords': [-23.549287355222415, -46.60148160421932], 'nome': 'Mooca', 'estacao_id': '7'},
        {'coords': [-23.55391441958687, -46.67298963305492], 'nome': 'Cerqueira César', 'estacao_id': '8'},
        {'coords': [-23.56270064684056, -46.61263985588234], 'nome': 'Cambuci', 'estacao_id': '9'},
        {'coords': [-23.547325518021744, -46.64207690421932], 'nome': 'Centro', 'estacao_id': '10'},
        {'coords': [-23.566121466158865, -46.73809550680783], 'nome': 'Cid.Universitária-USP-Ipen', 'estacao_id': '11'},
        {'coords': [-23.47753959549242, -46.692138309772915], 'nome': 'N.Senhora do Ó', 'estacao_id': '12'},
        {'coords': [-23.58234192392213, -46.47046700421834], 'nome': 'Itaquera', 'estacao_id': '13'},
        {'coords': [-23.77645628706186, -46.69677564469008], 'nome': 'Grajaú-Parelheiros', 'estacao_id': '14'},
        {'coords': [-23.560924449393774, -46.70153337538319], 'nome': 'Pinheiros', 'estacao_id': '15'},
        {'coords': [-23.49890019033872, -46.4450417772355], 'nome': 'S Miguel Paulista', 'estacao_id': '16'},
        {'coords': [-23.680711167687296, -46.67579978588038], 'nome': 'Interlagos', 'estacao_id': '17'},
        {'coords': [-23.501541879266153, -46.42067224654922], 'nome': 'Itaim Paulista', 'estacao_id': '18'},
        {'coords': [-23.666353022636017, -46.7810391597671], 'nome': 'Capão Redondo', 'estacao_id': '19'},
        {'coords': [-23.518761440588285, -46.744062190727675], 'nome': 'Marg.Tietê-Pte Remédios', 'estacao_id': '20'},
        {'coords': [-23.457931652360394, -46.76675231176519], 'nome': 'Pico do Jaraguá', 'estacao_id': '21'},
        {'coords': [-23.41485503641999, -46.75647394840244], 'nome': 'Perus', 'estacao_id': '22'},
    ]
    
    print(f"🚀 INICIANDO COLETA HISTÓRICA CORRIGIDA PARA {len(all_stations)} ESTAÇÕES")
    print(f"📅 Período: últimos {days} dias")
    print("=" * 60)
    
    # Calcular timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    print(f"📊 Período da API: {start_date.strftime('%d/%m/%Y %H:%M')} até {end_date.strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    total_saved = 0
    results = []
    
    for i, station in enumerate(all_stations, 1):
        lat, lon = station['coords']
        station_name = station['nome']
        station_id = station['estacao_id']
        
        print(f"\n[{i}/{len(all_stations)}] 📍 Processando {station_name}...")
        
        # Construir URL
        url = f"{BASE_URL}?lat={lat}&lon={lon}&start={start_timestamp}&end={end_timestamp}&appid={API_KEY}"
        
        try:
            # Fazer requisição com delay
            if i > 1:
                time.sleep(delay_between_requests)
            
            response = requests.get(url)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                saved_count = 0
                
                if 'list' in data and len(data['list']) > 0:
                    print(f"📈 Encontrados {len(data['list'])} registros históricos")
                    
                    for item in data['list']:
                        #Uusar o timestamp real da medição
                        timestamp = datetime.fromtimestamp(item['dt'])
                        
                        print(f"   📅 Medição de: {timestamp.strftime('%d/%m/%Y %H:%M')}")
                        
                        # Verificar se já existe (usando unique_together)
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
                                timestamp=timestamp  # TIMESTAMP REAL DA MEDIÇÃO
                            )
                            air_data.save()
                            saved_count += 1
                        else:
                            print(f"   ⚠️  Registro duplicado: {timestamp}")
                    
                    total_saved += saved_count
                    results.append({
                        'station': station_name,
                        'status': 'success',
                        'records_found': len(data['list']),
                        'records_saved': saved_count,
                        'first_timestamp': data['list'][0]['dt'] if data['list'] else None,
                        'last_timestamp': data['list'][-1]['dt'] if data['list'] else None
                    })
                    
                    print(f"✅ {station_name}: {saved_count} novos registros salvos")
                    
                else:
                    print(f"⚠️  {station_name}: Nenhum dado encontrado no período")
                    results.append({
                        'station': station_name,
                        'status': 'no_data',
                        'records_found': 0,
                        'records_saved': 0
                    })
                    
            else:
                print(f"❌ {station_name}: Erro {response.status_code}")
                results.append({
                    'station': station_name,
                    'status': 'error',
                    'error_code': response.status_code,
                    'records_saved': 0
                })
                
        except Exception as e:
            print(f"💥 {station_name}: Erro na requisição - {e}")
            results.append({
                'station': station_name,
                'status': 'exception',
                'error': str(e),
                'records_saved': 0
            })
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DA COLETA HISTÓRICA CORRIGIDA")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] in ['error', 'exception'])
    no_data_count = sum(1 for r in results if r['status'] == 'no_data')
    
    print(f"🏁 COLETA CONCLUÍDA!")
    print(f"📊 Estações processadas: {len(all_stations)}")
    print(f"✅ Sucesso: {success_count} estações")
    print(f"⚠️  Sem dados: {no_data_count} estações")
    print(f"❌ Erros: {error_count} estações")
    print(f"💾 Total de registros salvos: {total_saved}")
    
    # Mostrar range de datas coletadas
    successful_results = [r for r in results if r['status'] == 'success' and r['first_timestamp']]
    if successful_results:
        min_timestamp = min(r['first_timestamp'] for r in successful_results)
        max_timestamp = max(r['last_timestamp'] for r in successful_results)
        min_date = datetime.fromtimestamp(min_timestamp).strftime('%d/%m/%Y %H:%M')
        max_date = datetime.fromtimestamp(max_timestamp).strftime('%d/%m/%Y %H:%M')
        print(f"📅 Período das medições: {min_date} até {max_date}")
    
    return {
        'total_stations': len(all_stations),
        'total_records_saved': total_saved,
        'success_count': success_count,
        'error_count': error_count,
        'no_data_count': no_data_count,
        'details': results
    }

# Função que verifica a quantidade de registros por estação
def check_historical_data():
    """Verifica quantos dados históricos temos por estação"""
    
    stations = [
        {'nome': 'Santana', 'estacao_id': '1'},
        {'nome': 'Santo Amaro', 'estacao_id': '2'},
        {'nome': 'Pq. Dom Pedro II','estacao_id': '3'},
        {'nome': 'Congonhas', 'estacao_id': '4'},
        {'nome': 'Ibirapuera', 'estacao_id': '5'},
        {'nome': 'Lapa', 'estacao_id': '6'},
        {'nome': 'Mooca', 'estacao_id': '7'},
        {'nome': 'Cerqueira César', 'estacao_id': '8'},
        {'nome': 'Cambuci', 'estacao_id': '9'},
        {'nome': 'Centro', 'estacao_id': '10'},
        {'nome': 'Cid.Universitária-USP-Ipen', 'estacao_id': '11'},
        {'nome': 'N.Senhora do Ó', 'estacao_id': '12'},
        {'nome': 'Itaquera', 'estacao_id': '13'},
        {'nome': 'Grajaú-Parelheiros', 'estacao_id': '14'},
        {'nome': 'Pinheiros', 'estacao_id': '15'},
        {'nome': 'S Miguel Paulista', 'estacao_id': '16'},
        {'nome': 'Interlagos', 'estacao_id': '17'},
        {'nome': 'Itaim Paulista', 'estacao_id': '18'},
        {'nome': 'Capão Redondo', 'estacao_id': '19'},
        {'nome': 'Marg.Tietê-Pte Remédios','estacao_id': '20'},
        {'nome': 'Pico do Jaraguá', 'estacao_id': '21'},
        {'nome': 'Perus', 'estacao_id': '22'},
    ]
    
    print("📊 VERIFICAÇÃO DE DADOS HISTÓRICOS")
    print("=" * 50)
    
    for station in stations:
        count = AirQualityData.objects.filter(station_id=station['estacao_id']).count()
        latest = AirQualityData.objects.filter(station_id=station['estacao_id']).order_by('-timestamp').first()
        
        latest_str = latest.timestamp.strftime('%d/%m/%Y %H:%M') if latest else "Nenhum"
        
        print(f"📍 {station['nome']}: {count} registros | Mais recente: {latest_str}")

def collect_last_hour_data_all_stations(delay_between_requests=1.0):
    # Configurações da chave
    API_KEY = settings.OPENWEATHER_API_KEY
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    
    # Lista de estações (mesma da sua função)
    all_stations = [
        {'coords': [-23.50455587377614, -46.62856773359203], 'nome': 'Santana', 'estacao_id': '1'},
        # ... suas outras estações
    ]
    
    print(f"🚀 INICIANDO COLETA DA ÚLTIMA HORA PARA {len(all_stations)} ESTAÇÕES")
    print("=" * 60)
    
    # Calcular timestamps para última hora
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=1)  # Apenas 1 hora atrás
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    print(f"📊 Período da API: {start_date.strftime('%d/%m/%Y %H:%M')} até {end_date.strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    total_saved = 0
    results = []
    
    for i, station in enumerate(all_stations, 1):
        lat, lon = station['coords']
        station_name = station['nome']
        station_id = station['estacao_id']
        
        print(f"\n[{i}/{len(all_stations)}] 📍 Processando {station_name}...")
        
        # Construir URL
        url = f"{BASE_URL}?lat={lat}&lon={lon}&start={start_timestamp}&end={end_timestamp}&appid={API_KEY}"
        
        try:
            # Fazer requisição com delay
            if i > 1:
                time.sleep(delay_between_requests)
            
            response = requests.get(url)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                saved_count = 0
                
                if 'list' in data and len(data['list']) > 0:
                    print(f"📈 Encontrados {len(data['list'])} registros na última hora")
                    
                    for item in data['list']:
                        # Usar o timestamp real da medição
                        timestamp = datetime.fromtimestamp(item['dt'])
                        
                        print(f"   🕐 Medição de: {timestamp.strftime('%d/%m/%Y %H:%M')}")
                        
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
                        else:
                            print(f"   ⚠️  Registro duplicado: {timestamp}")
                    
                    total_saved += saved_count
                    results.append({
                        'station': station_name,
                        'status': 'success',
                        'records_found': len(data['list']),
                        'records_saved': saved_count
                    })
                    
                    print(f"✅ {station_name}: {saved_count} novos registros salvos")
                    
                else:
                    print(f"⚠️  {station_name}: Nenhum dado na última hora")
                    results.append({
                        'station': station_name,
                        'status': 'no_data',
                        'records_found': 0,
                        'records_saved': 0
                    })
                    
            else:
                print(f"❌ {station_name}: Erro {response.status_code}")
                results.append({
                    'station': station_name,
                    'status': 'error',
                    'error_code': response.status_code,
                    'records_saved': 0
                })
                
        except Exception as e:
            print(f"💥 {station_name}: Erro na requisição - {e}")
            results.append({
                'station': station_name,
                'status': 'exception',
                'error': str(e),
                'records_saved': 0
            })
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL - ÚLTIMA HORA")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] in ['error', 'exception'])
    no_data_count = sum(1 for r in results if r['status'] == 'no_data')
    
    print(f"🏁 COLETA CONCLUÍDA!")
    print(f"📊 Estações processadas: {len(all_stations)}")
    print(f"✅ Com dados: {success_count} estações")
    print(f"⚠️  Sem dados: {no_data_count} estações")
    print(f"❌ Erros: {error_count} estações")
    print(f"💾 Total de registros salvos: {total_saved}")
    
    return {
        'total_stations': len(all_stations),
        'total_records_saved': total_saved,
        'success_count': success_count,
        'error_count': error_count,
        'no_data_count': no_data_count,
        'details': results
    }