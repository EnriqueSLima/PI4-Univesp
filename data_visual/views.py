from django.shortcuts import render
import folium
from .utils.geo_utils import get_sp_geojson, get_distritos_sp, get_subprefeituras_sp

#   View para mapa focado em São Paulo
def sp_map_dashboard(request):
    """Dashboard com mapa restrito aos limites de SP"""
    
    # Obter o GeoJSON de SP para calcular os bounds
    sp_geojson = get_sp_geojson()
    
    # Calcular os limites (bounds) de SP
    if sp_geojson and sp_geojson.get('features'):
        coordinates = sp_geojson['features'][0]['geometry']['coordinates'][0]
        lats = [coord[1] for coord in coordinates]
        lons = [coord[0] for coord in coordinates]
        
        sw_bound = [min(lats), min(lons)]  # Sudoeste
        ne_bound = [max(lats), max(lons)]  # Nordeste
        bounds = [sw_bound, ne_bound]
    else:
        # Bounds aproximados de SP como fallback
        bounds = [[-23.700, -46.825], [-23.400, -46.365]]
    
    # Criar mapa focado em SP
    sp_map = folium.Map(
        location=[-23.6905, -46.6333],
        zoom_start=10,
        tiles='OpenStreetMap',
        control_scale=True,
        max_bounds=bounds,  # Restringe o movimento do mapa
        min_zoom=10,        # Zoom mínimo
        max_zoom=16         # Zoom máximo
    )

    # Adicionar máscara para área fora de SP
    add_mask_layer(sp_map, sp_geojson)

    # Adicionar camada de distritos
    add_distritos_layer(sp_map)

    # Adicionar camada de subprefeituras
    add_subprefeituras_layer(sp_map)

    # Adicionar controles de camadas
    folium.LayerControl().add_to(sp_map)

    # Adicionar dados de exemplo (opcional)
    add_station_data(sp_map)

    # Calcular estatísticas reais
    estatisticas = calcular_estatisticas()
    map_html = sp_map._repr_html_()

    context = {
        'map_html': map_html,
        'title': 'Dashboard SP - Análise de Dados',
        'estatisticas': estatisticas  # Passar dados para o template
    }
    # Forçar o zoom nos limites de SP
    sp_map.fit_bounds(bounds)
    
    return render(request, 'visualization/dashboard.html', context)

#   Adiciona layer com mascara ao redor do município.
def add_mask_layer(map_object, sp_geojson):
    """Adiciona máscara para área fora dos limites de SP"""
    if not sp_geojson or not sp_geojson.get('features'):
        return
    
    # Criar um polígono muito grande que cobre o mundo inteiro
    # com um "buraco" no formato de SP
    world_with_hole = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "mask"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        # Polígono externo (mundo inteiro)
                        [[-180, 90], [180, 90], [180, -90], [-180, -90], [-180, 90]],
                        # "Buraco" no formato de SP (coordenadas invertidas)
                        sp_geojson['features'][0]['geometry']['coordinates'][0]
                    ]
                }
            }
        ]
    }
    folium.GeoJson(
        world_with_hole,
        name='Área de Foco',
        style_function=lambda x: {
            'fillColor': 'whitesmoke',
            'color': 'white',
            'weight': 0,
            'fillOpacity': 1
        },
        show=True  # Visível por padrão
    ).add_to(map_object)

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
            localize=True,
            max_width=250
        ),
        show=True  # Ocultar por padrão (para não sobrecarregar)
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
            'fillColor': get_color_for_distrito(feature),
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

#   Adiciona layer com cores de preenchimento dos distritos.
def get_color_for_distrito(feature):
    """Gera cores consistentes para cada distrito"""
    properties = feature.get('properties', {})
    distrito_name = properties.get('nm_distrito_municipal', '') or 'unknown'
    
    import hashlib
    hash_obj = hashlib.md5(distrito_name.encode())
    hash_int = int(hash_obj.hexdigest()[:8], 16)
    
    # Cores mais suaves para melhor visualização
    colors = [
        '#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7',
        '#C7CEEA', '#F8B195', '#F67280', '#C06C84', '#6C5B7B',
        '#355C7D', '#99B898', '#FECEAB', '#FF847C', '#E84A5F'
    ]
    
    return colors[hash_int % len(colors)]

#   Função para capturar propriedades dos distritos e sub-prefeituras.
def get_feature_properties(geojson_data):
    """Retorna as propriedades da primeira feature para referência"""
    if not geojson_data or not geojson_data.get('features'):
        return {}
    
    first_feature = geojson_data['features'][0]
    return first_feature.get('properties', {})

#   Função para adicionar marcadores simples
def add_station_data(map_object):
    """Adiciona alguns marcadores com estações de medição"""
    pontos_referencia = [
        ([-23.50455587377614, -46.62856773359203], 'Santana', 'blue', 'star', 'Estação de medição.'),
        ([-23.65452312102595, -46.70995648887296], 'Santo Amaro', 'blue', 'star', 'Estação de medição.'),
        ([-23.545735329390677, -46.62765280792035], 'Pq. Dom Pedro II', 'blue', 'star', 'Estação de medição.'),
        ([-23.615943617970945, -46.663295450971994], 'Congonhas', 'blue', 'star', 'Estação de medição.'),
        ([-23.585792325197616, -46.658413146546586], 'Ibirapuera', 'blue', 'star', 'Estação de medição.'),
        ([-23.515542173706905, -46.72656563120576], 'Lapa', 'blue', 'star', 'Estação de medição.'),
        ([-23.549287355222415, -46.60148160421932], 'Mooca', 'blue', 'star', 'Estação de medição.'),
        ([-23.55391441958687, -46.67298963305492], 'Cerqueira César', 'blue', 'star', 'Estação de medição.'),
        ([-23.56270064684056, -46.61263985588234], 'Cambuci', 'blue', 'star', 'Estação de medição.'),
        ([-23.547325518021744, -46.64207690421932], 'Centro', 'blue', 'star', 'Estação de medição.'),
        ([-23.566121466158865, -46.73809550680783], 'Cid.Universitária-USP-Ipen', 'blue', 'star', 'Estação de medição.'),
        ([-23.47753959549242, -46.692138309772915], 'N.Senhora do Ó', 'blue', 'star', 'Estação de medição.'),
        ([-23.58234192392213, -46.47046700421834], 'Itaquera', 'blue', 'star', 'Estação de medição.'),
        ([-23.77645628706186, -46.69677564469008], 'Grajaú-Parelheiros', 'blue', 'star', 'Estação de medição.'),
        ([-23.560924449393774, -46.70153337538319], 'Pinheiros', 'blue', 'star', 'Estação de medição.'),
        ([-23.49890019033872, -46.4450417772355], 'S Miguel Paulista', 'blue', 'star', 'Estação de medição.'),
        ([-23.680711167687296, -46.67579978588038], 'Interlagos', 'blue', 'star', 'Estação de medição.'),
        ([-23.501541879266153, -46.42067224654922], 'Itaim Paulista', 'blue', 'star', 'Estação de medição.'),
        ([-23.666353022636017, -46.7810391597671], 'Capão Redondo', 'blue', 'star', 'Estação de medição.'),
        ([-23.518761440588285, -46.744062190727675], 'Marg.Tietê-Pte Remédios', 'blue', 'star', 'Estação de medição.'),
        ([-23.457931652360394, -46.76675231176519], 'Pico do Jaraguá', 'blue', 'star', 'Estação de medição.'),
        ([-23.41485503641999, -46.75647394840244], 'Perus', 'blue', 'star', 'Estação de medição.'),
    ]
    
    for coords, nome, cor, icone, descricao in pontos_referencia:
        folium.Marker(
            coords,
            popup=f'<b>{nome}</b><br>{descricao}',
            tooltip=nome,
            icon=folium.Icon(color=cor, icon=icone)
        ).add_to(map_object)

#! Cálculos estatísticos
def calcular_estatisticas():
    """Calcula estatísticas reais dos dados"""
    try:
        distritos_data = get_distritos_sp()
        ciclovias_data = get_ciclovias_sp()
        
        # Estatísticas básicas
        estatisticas = {
            'total_ciclovias': len(ciclovias_data.get('features', [])) if ciclovias_data else 0,
            'total_distritos': len(distritos_data.get('features', [])) if distritos_data else 0,
            'total_subprefeituras': 32,  # Fixo para SP
        }
        
        # Aqui você pode adicionar cálculos mais complexos
        # como distribuição por região, tipos de ciclovia, etc.
        
        return estatisticas
        
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")
        return {
            'total_ciclovias': 0,
            'total_distritos': 0,
            'total_subprefeituras': 0
        }
