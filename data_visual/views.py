# data_visual/views.py
import folium

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from data_process.models import AirQualityData
from .utils.geo_utils import get_sp_geojson, get_distritos_sp, get_subprefeituras_sp, get_areaverde_sp


#   View para mapa focado em São Paulo
def sp_map_dashboard(request):
    """Dashboard com mapa restrito aos limites de SP"""
    # Obter o GeoJSON de SP
    sp_geojson = get_sp_geojson()
    
    # Calcular os limites (bounds) de São Paulo - SP
    if sp_geojson and sp_geojson.get('features'):
        coordinates = sp_geojson['features'][0]['geometry']['coordinates'][0]
        lats = [coord[1] for coord in coordinates]
        lons = [coord[0] for coord in coordinates]
        
        sw_bound = [min(lats), min(lons)]
        ne_bound = [max(lats), max(lons)]
        bounds = [sw_bound, ne_bound]
    else:
        bounds = [[-23.700, -46.825], [-23.400, -46.365]]
    
    # Criar mapa
    sp_map = folium.Map(
        location=[-23.700, -46.600],
        zoom_start=10,
        tiles='OpenStreetMap',
        control_scale=True,
        min_zoom=10,
        max_zoom=16
    )
    
    # Adicionar máscara e obter bounds externos
    outer_bounds = add_mask_layer(sp_map, sp_geojson)
    
    # Usar os bounds externos para restringir o movimento
    if outer_bounds:
        restriction_bounds = outer_bounds
    else:
        # Fallback: expandir um pouco os bounds originais
        restriction_bounds = [
            [bounds[0][0] - 0.02, bounds[0][1] - 0.02],
            [bounds[1][0] + 0.02, bounds[1][1] + 0.02]
        ]
    
    # **SCRIPT DE RESTRIÇÃO USANDO OS BOUNDS DA MÁSCARA**
    restrict_script = f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var map = {sp_map.get_name()};
            var restrictionBounds = [
                [{restriction_bounds[0][0]}, {restriction_bounds[0][1]}],
                [{restriction_bounds[1][0]}, {restriction_bounds[1][1]}]
            ];
            
            // Definir limites máximos do mapa
            map.setMaxBounds(restrictionBounds);
            
            // Fit inicial nos bounds de SP (não nos de restrição)
            var spBounds = [
                [{bounds[0][0]}, {bounds[0][1]}],
                [{bounds[1][0]}, {bounds[1][1]}]
            ];
            map.fitBounds(spBounds);
            
            // Prevenir que o usuário saia da área permitida
            map.on('drag', function() {{
                map.panInsideBounds(restrictionBounds);
            }});
        }});
    </script>
    """
    sp_map.get_root().html.add_child(folium.Element(restrict_script))
    
    # Adiciona camada de distritos
    add_distritos_layer(sp_map)
    # Adiciona camada de subprefeituras
    add_subprefeituras_layer(sp_map)
<<<<<<< HEAD
    # Adiciona controles de camadas
    folium.LayerControl().add_to(sp_map)
    # Adiciona marcadores estações de medição
    add_station_marker(sp_map)
=======
>>>>>>> f1c61f4 (Adiciona layer com praças e largos e legenda)
    # Adiciona estações de medição
    add_station_data(sp_map)
    # Adiciona camada com praças e largos
    add_areaverde_layer(sp_map)
    
    # Adiciona controles de camadas
    folium.LayerControl().add_to(sp_map)

    map_html = sp_map._repr_html_()

    context = {
        'map_html': map_html,
        'title': '',
    }
    
    return render(request, 'visualization/dashboard.html', context)

# Adiciona retêngulo branco em volta do município
def add_mask_layer(map_object, sp_geojson):
    """Adiciona máscara retangular para área ao redor de SP"""
    if not sp_geojson or not sp_geojson.get('features'):
        return
    
    # Calcular bounds de SP com uma margem
    coordinates = sp_geojson['features'][0]['geometry']['coordinates'][0]
    lats = [coord[1] for coord in coordinates]
    lons = [coord[0] for coord in coordinates]
    
    # Bounds de SP
    sp_sw = [min(lats), min(lons)]
    sp_ne = [max(lats), max(lons)]
    
    # Criar bounds externos com margem (ajuste conforme necessário)
    margin = 0.15  # Margem em graus
    outer_sw = [sp_sw[0] - margin, sp_sw[1] - 1.6*margin]
    outer_ne = [sp_ne[0] + margin, sp_ne[1] + 1.6*margin]
    
    # Criar polígono retangular com buraco de SP
    mask_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "mask"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        # Polígono externo
                        [
                            [outer_sw[1], outer_sw[0]],  # SW
                            [outer_ne[1], outer_sw[0]],  # SE
                            [outer_ne[1], outer_ne[0]],  # NE
                            [outer_sw[1], outer_ne[0]],  # NW
                            [outer_sw[1], outer_sw[0]]   # SW
                        ],
                        # "Buraco" no formato de SP
                        sp_geojson['features'][0]['geometry']['coordinates'][0]
                    ]
                }
            }
        ]
    }
    
    folium.GeoJson(
        mask_geojson,
        name='Área de Foco',
        style_function=lambda x: {
            'fillColor': 'whitesmoke',
            'color': 'darkgray',
            'weight': 2,
            'fillOpacity': 1,
            'dashArray': '5, 5'
        },
        show=True
    ).add_to(map_object)
    
    # Retornar os bounds externos para usar na restrição do mapa
    return [outer_sw, outer_ne]

#   Adiciona layer com contorno das sub-prefeituras.
def add_subprefeituras_layer(map_object):
    """Adiciona camada de subprefeituras"""
    subprefeituras_data = get_subprefeituras_sp()
    
    # Obter campos disponíveis
    properties = get_feature_properties(subprefeituras_data)
    tooltip_fields = ['nm_subprefeitura', 'sg_subprefeitura']
    available_tooltip_fields = [f for f in tooltip_fields if f in properties]
    
    folium.GeoJson(
        subprefeituras_data,
        name='Subprefeituras',
        style_function=lambda feature: {
            'fillColor': 'None',
            'color': 'black',
            'weight': 2.2,
            'fillOpacity': 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=available_tooltip_fields,
            aliases=['Subprefeitura:', 'Sigla:'] if len(available_tooltip_fields) == 2 else ['Subprefeitura:'],
            style=("background-color: white; color: #333; font-size: 11px; padding: 4px;")
        ) if available_tooltip_fields else None,
        popup=folium.GeoJsonPopup(
            fields=['nm_subprefeitura', 'sg_subprefeitura', 'qt_area_quilometro'],
            aliases=['Subprefeitura:', 'Sigla:', 'Área (km²):'],
            localize=False,
            max_width=250
        ),
        show=False  # Ocultar por padrão (para não sobrecarregar)
    ).add_to(map_object)

#   Adiciona layer com contorno dos distritos.
def add_distritos_layer(map_object):
    """Adiciona camada de distritos (ajustada para não sobrepor ciclovias)"""
    distritos_data = get_distritos_sp()
    
    properties = get_feature_properties(distritos_data)
    tooltip_fields = ['nm_distrito_municipal', 'sg_distrito_municipal']
    available_tooltip_fields = [f for f in tooltip_fields if f in properties]
    
    folium.GeoJson(
        distritos_data,
        name='Distritos',
        style_function=lambda feature: {
            'fillColor': 'None',#get_color_for_distrito(feature),
            'color': 'black',
            'weight': 1.2,
            'fillOpacity': 0.3,
            'opacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=available_tooltip_fields,
            aliases=['Distrito:', 'Sigla:'] if len(available_tooltip_fields) == 2 else ['Distrito:'],
            style=("background-color: white; color: #333; font-size: 11px; padding: 4px;")
        ) if available_tooltip_fields else None,
        popup=folium.GeoJsonPopup(
            fields=['nm_distrito_municipal', 'sg_distrito_municipal', 'qt_area_quilometro'],
            aliases=['Distrito:', 'Sigla:', 'Área (km²):'],
            localize=True,
            max_width=250
        ),
        show=True  # Visível por padrão
    ).add_to(map_object)

#   Adiciona layer com praças e largos.
def add_areaverde_layer(map_object):
    """Adiciona camada de praças e largos - versão mínima"""
    try:
        areaverde_data = get_areaverde_sp()
        
        if not areaverde_data or not areaverde_data.get('features'):
            print("⚠️ Nenhum dado de áreas verdes encontrado")
            return
        
        print(f"✅ Carregadas {len(areaverde_data['features'])} praças/largos")
        
        # Versão mínima sem tooltips complexos
        folium.GeoJson(
            areaverde_data,
            name='Praças e Largos',
            style_function=lambda x: {
                'fillColor': 'green',
                'color': 'darkgreen',
                'weight': 1,
                'fillOpacity': 0.5,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['nome'] if 'nome' in get_feature_properties(areaverde_data) else [],
                aliases=['Praça:']
            ),
            show=True
        ).add_to(map_object)
        
        print("✅ Layer de praças e largos adicionado!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

#   Função para capturar propriedades dos distritos e sub-prefeituras.
def get_feature_properties(geojson_data):
    """Retorna as propriedades da primeira feature para referência"""
    if not geojson_data or not geojson_data.get('features'):
        return {}
    
    first_feature = geojson_data['features'][0]
    return first_feature.get('properties', {})

# Função para adicionar marcadores simples
def add_station_marker(map_object):
    """Adiciona alguns marcadores com estações de medição"""
    pontos_referencia = [
        ([-23.50455587377614, -46.62856773359203], 'Santana',  'green', 'leaf', 'Estação de medição.', '1'),
        ([-23.65452312102595, -46.70995648887296], 'Santo Amaro', 'green', 'leaf', 'Estação de medição.', '2'),
        ([-23.545735329390677, -46.62765280792035], 'Pq. Dom Pedro II',  'green', 'leaf', 'Estação de medição.', '3'),
        ([-23.615943617970945, -46.663295450971994], 'Congonhas',  'green', 'leaf', 'Estação de medição.', '4'),
        ([-23.585792325197616, -46.658413146546586], 'Ibirapuera',  'green', 'leaf', 'Estação de medição.', '5'),
        ([-23.515542173706905, -46.72656563120576], 'Lapa',  'green', 'leaf', 'Estação de medição.', '6'),
        ([-23.549287355222415, -46.60148160421932], 'Mooca',  'green', 'leaf', 'Estação de medição.', '7'),
        ([-23.55391441958687, -46.67298963305492], 'Cerqueira César',  'green', 'leaf', 'Estação de medição.', '8'),
        ([-23.56270064684056, -46.61263985588234], 'Cambuci',  'green', 'leaf', 'Estação de medição.', '9'),
        ([-23.547325518021744, -46.64207690421932], 'Centro',  'green', 'leaf', 'Estação de medição.', '10'),
        ([-23.566121466158865, -46.73809550680783], 'Cid.Universitária-USP-Ipen',  'green', 'leaf', 'Estação de medição.', '11'),
        ([-23.47753959549242, -46.692138309772915], 'N.Senhora do Ó',  'green', 'leaf', 'Estação de medição.', '12'),
        ([-23.58234192392213, -46.47046700421834], 'Itaquera',  'green', 'leaf', 'Estação de medição.', '13'),
        ([-23.77645628706186, -46.69677564469008], 'Grajaú-Parelheiros',  'green', 'leaf', 'Estação de medição.', '14'),
        ([-23.560924449393774, -46.70153337538319], 'Pinheiros',  'green', 'leaf', 'Estação de medição.', '15'),
        ([-23.49890019033872, -46.4450417772355], 'S Miguel Paulista',  'green', 'leaf', 'Estação de medição.', '16'),
        ([-23.680711167687296, -46.67579978588038], 'Interlagos',  'green', 'leaf', 'Estação de medição.', '17'),
        ([-23.501541879266153, -46.42067224654922], 'Itaim Paulista',  'green', 'leaf', 'Estação de medição.', '18'),
        ([-23.666353022636017, -46.7810391597671], 'Capão Redondo',  'green', 'leaf', 'Estação de medição.', '19'),
        ([-23.518761440588285, -46.744062190727675], 'Marg.Tietê-Pte Remédios',  'green', 'leaf', 'Estação de medição.', '20'),
        ([-23.457931652360394, -46.76675231176519], 'Pico do Jaraguá',  'green', 'leaf', 'Estação de medição.', '21'),
        ([-23.41485503641999, -46.75647394840244], 'Perus',  'green', 'leaf', 'Estação de medição.', '22'),
    ]
    
    for coords, nome, cor, icone, descricao, estacao_id in pontos_referencia:
        # Criar popup com link que pode ser capturado pelo evento de clique do marcador
        popup_html = f'''
        <div>
            <b>{nome}</b><br>
            {descricao}<br>
            <button>Ver Dados</button>
        </div>
        '''
        
        marker = folium.Marker(
            coords,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Clique para ver dados de {nome}",
            icon=folium.Icon(color=cor, icon=icone)
        )
        
        # Adicionar propriedade customizada ao marcador
        marker.estacao_id = estacao_id
        marker.estacao_nome = nome
        
        marker.add_to(map_object)

def add_station_data(map_object):
    """Adiciona marcadores com dados reais da API"""
    # Buscar os dados mais recentes de todas as estações
    stations_data = []
    for station_id in range(1, 23):  # Assumindo IDs de 1 a 22
        try:
            data = AirQualityData.objects.filter(
                station_id=str(station_id)
            ).latest('timestamp')
            stations_data.append(data)
        except AirQualityData.DoesNotExist:
            # Se não tiver dados, usar dados padrão
            continue
    
    # Coordenadas das estações
    coordenadas_estacoes = {
        '1': [-23.50455587377614, -46.62856773359203],
        '2': [-23.65452312102595, -46.70995648887296],
        '3': [-23.545735329390677, -46.62765280792035],
        '4': [-23.615943617970945, -46.663295450971994],
        '5': [-23.585792325197616, -46.658413146546586],
        '6': [-23.515542173706905, -46.72656563120576],
        '7': [-23.549287355222415, -46.60148160421932],
        '8': [-23.55391441958687, -46.67298963305492],
        '9': [-23.56270064684056, -46.61263985588234],
        '10': [-23.547325518021744, -46.64207690421932],
        '11': [-23.566121466158865, -46.73809550680783],
        '12': [-23.47753959549242, -46.692138309772915],
        '13': [-23.58234192392213, -46.47046700421834],
        '14': [-23.77645628706186, -46.69677564469008],
        '15': [-23.560924449393774, -46.70153337538319],
        '16': [-23.49890019033872, -46.4450417772355],
        '17': [-23.680711167687296, -46.67579978588038],
        '18': [-23.501541879266153, -46.42067224654922],
        '19': [-23.666353022636017, -46.7810391597671],
        '20': [-23.518761440588285, -46.744062190727675],
        '21': [-23.457931652360394, -46.76675231176519],
        '22': [-23.41485503641999, -46.75647394840244],
        # ... adicione todas as outras
    }
    
    for data in stations_data:
        coords = coordenadas_estacoes.get(data.station_id)
        if not coords:
            continue
            
        aqi_color = data.get_aqi_color()
        aqi_description = data.get_aqi_description()
        
        # Criar popup com dados reais
        popup_html = f'''
        <div style="min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: #333;">{data.station_name}</h4>
            <div style="background-color: {aqi_color}; color: white; padding: 5px; border-radius: 3px; text-align: center; margin-bottom: 10px;">
                <strong>AQI: {data.aqi} - {aqi_description}</strong>
            </div>
            <table style="width: 100%; font-size: 12px;">
                <tr><td>PM2.5:</td><td><strong>{data.pm2_5:.1f} µg/m³</strong></td></tr>
                <tr><td>PM10:</td><td><strong>{data.pm10:.1f} µg/m³</strong></td></tr>
                <tr><td>NO₂:</td><td><strong>{data.no2:.1f} µg/m³</strong></td></tr>
                <tr><td>O₃:</td><td><strong>{data.o3:.1f} µg/m³</strong></td></tr>
                <tr><td>CO:</td><td><strong>{data.co:.1f} µg/m³</strong></td></tr>
            </table>
            <button onclick="loadStationChart('{data.station_id}')" 
                    style="width: 100%; margin-top: 10px; padding: 5px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;">
                Ver Gráficos
            </button>
        </div>
        '''
        
        # Escolher ícone baseado na qualidade do ar
        icon_type = 'info-sign' if data.aqi <= 2 else 'exclamation-sign'
        
        marker = folium.Marker(
            coords,
            #popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{data.station_name} - AQI: {data.aqi} ({aqi_description})",
            icon=folium.Icon(color=aqi_color, icon=icon_type)
        )
        
        # Adicionar propriedades customizadas
        marker.estacao_id = data.station_id
        marker.estacao_nome = data.station_name
        
        marker.add_to(map_object)

def get_dados_dia(request, station_id):
    """API para dados do dia atual"""
    try:
        hoje = datetime.now().date()
        
        dados_hoje = AirQualityData.objects.filter(
            station_id=station_id,
            timestamp__date=hoje
        ).order_by('timestamp')
        
        dados_json = []
        for dado in dados_hoje:
            dados_json.append({
                'timestamp': dado.timestamp.isoformat(),
                'pm2_5': dado.pm2_5,
                'pm10': dado.pm10,
                'no2': dado.no2,
                'o3': dado.o3,
                'so2': dado.so2,
                'co': dado.co,
            })
        
        return JsonResponse({
            'success': True,
            'dados': dados_json
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_estacao_data(request, station_id):
    """API para dados de uma estação específica - últimos 7 dias"""
    try:
        # Últimos 7 dias
        data_inicio = datetime.now() - timedelta(days=7)
        
        dados = AirQualityData.objects.filter(
            station_id=station_id,
            timestamp__gte=data_inicio
        ).order_by('timestamp')
        
        # Se não houver dados dos últimos 7 dias, busca os últimos 30 registros
        if not dados.exists():
            dados = AirQualityData.objects.filter(
                station_id=station_id
            ).order_by('-timestamp')[:30]
        
        dados_json = []
        for dado in dados:
            dados_json.append({
                'timestamp': dado.timestamp.isoformat(),
                'aqi': dado.aqi,
                'pm2_5': dado.pm2_5,
                'pm10': dado.pm10,
                'no2': dado.no2,
                'o3': dado.o3,
                'so2': dado.so2,
                'co': dado.co,
            })
        
        return JsonResponse({
            'success': True,
            'station_name': dados[0].station_name if dados else 'Estação',
            'dados': dados_json
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})