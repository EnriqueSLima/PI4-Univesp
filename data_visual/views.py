from django.shortcuts import render
import folium
from .utils.geo_utils import get_sp_geojson, get_distritos_sp, get_subprefeituras_sp, get_ciclovias_sp, validate_geojson_plotting

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

    # Adicionar camada de subprefeituras
    add_subprefeituras_layer(sp_map)

    # Adicionar camada de distritos
    add_distritos_layer(sp_map)

    # Adicionar camada de ciclovias (por cima dos distritos)
    add_ciclovias_layer(sp_map)

    # Adicionar controles de camadas
    folium.LayerControl().add_to(sp_map)

    # Adicionar dados de exemplo (opcional)
    #add_sample_data(sp_map)
    
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
    
    if not validate_geojson_plotting(subprefeituras_data, "Subprefeituras"):
        print("❌ Camada de subprefeituras não carregada")
        return
    
    # Obter campos disponíveis
    properties = get_feature_properties(subprefeituras_data)
    tooltip_fields = ['nm_subprefeitura', 'sg_subprefeitura']
    available_tooltip_fields = [f for f in tooltip_fields if f in properties]
    
    folium.GeoJson(
        subprefeituras_data,
        name='Subprefeituras',
        style_function=lambda feature: {
            'fillColor': 'None',
            'color': 'gray',
            'weight': 4,
            'fillOpacity': 0,
            'dashArray': '5, 5'
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
        show=False  # Ocultar por padrão (para não sobrecarregar)
    ).add_to(map_object)

#   Adiciona layer com contorno dos distritos.
def add_distritos_layer(map_object):
    """Adiciona camada de distritos (ajustada para não sobrepor ciclovias)"""
    distritos_data = get_distritos_sp()
    
    if not validate_geojson_plotting(distritos_data, "Distritos"):
        print("❌ Camada de distritos não carregada")
        return
    
    properties = get_feature_properties(distritos_data)
    tooltip_fields = ['nm_distrito_municipal', 'sg_distrito_municipal']
    available_tooltip_fields = [f for f in tooltip_fields if f in properties]
    
    folium.GeoJson(
        distritos_data,
        name='Distritos',
        style_function=lambda feature: {
            'fillColor': get_color_for_distrito(feature),
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.4,
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

#   Adiciona layer com ciclovias.
def add_ciclovias_layer(map_object):
    """Adiciona camada de ciclovias"""
    ciclovias_data = get_ciclovias_sp()
    
    if not validate_geojson_plotting(ciclovias_data, "Ciclovias"):
        print("❌ Camada de ciclovias não carregada")
        # Adicionar marcador de aviso
        folium.Marker(
            [-23.5600, -46.6400],
            popup='<b>Ciclovias não carregadas</b><br>Verifique o arquivo GeoJSON',
            icon=folium.Icon(color='orange', icon='exclamation-triangle')
        ).add_to(map_object)
        return
    
    # Obter campos disponíveis dinamicamente
    properties = get_feature_properties(ciclovias_data)
    available_fields = list(properties.keys())
    
    # Escolher campos apropriados para tooltip
    tooltip_fields = []
    field_priority = ['nome', 'name', 'logradouro', 'tipo', 'tipo_via', 'descricao']
    
    for field in field_priority:
        if field in available_fields:
            tooltip_fields = [field]
            break
    
    if not tooltip_fields and available_fields:
        tooltip_fields = [available_fields[0]]  # Usar primeiro campo disponível
    
    # Estilo para ciclovias
    folium.GeoJson(
        ciclovias_data,
        name='Ciclovias',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 2,
            'opacity': 0.8,
            'lineCap': 'round',
            'lineJoin': 'round'
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=['Ciclovia:'] * len(tooltip_fields),
            style=("background-color: white; color: #333; font-size: 11px; padding: 4px;")
        ) if tooltip_fields else None,
        popup=folium.GeoJsonPopup(
            fields=available_fields[:6],  # Mostrar até 6 campos
            aliases=[f.replace('_', ' ').title() for f in available_fields[:6]],
            localize=True,
            max_width=300
        ),
        show=True   # Visível por padrão
    ).add_to(map_object)
    print("✅ Camada de ciclovias adicionada ao mapa")

#   Função para adicionar marcadores simples
def add_sample_data(map_object):
    """Adiciona alguns pontos de referência para orientação"""
    pontos_referencia = [
        ([-23.5505, -46.6333], 'Praça da Sé', 'red', 'star', 'Centro histórico de SP'),
        ([-23.5632, -46.6544], 'Av. Paulista', 'blue', 'building', 'Principal centro financeiro'),
        ([-23.5870, -46.6570], 'Parque Ibirapuera', 'green', 'tree', 'Principal parque urbano'),
        ([-23.5200, -46.6200], 'Zona Leste', 'orange', 'home', 'Região residencial'),
    ]
    
    for coords, nome, cor, icone, descricao in pontos_referencia:
        folium.Marker(
            coords,
            popup=f'<b>{nome}</b><br>{descricao}',
            tooltip=nome,
            icon=folium.Icon(color=cor, icon=icone)
        ).add_to(map_object)

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

#! Mantenha a view de debug para verificação

#   View de Debug para distritos e subprefeituras
def geojson_debug(request):
    """Página para debug dos arquivos GeoJSON"""
    from .utils.geo_utils import get_distritos_sp, get_subprefeituras_sp, inspect_geojson
    import json
    
    distritos = get_distritos_sp()
    subprefeituras = get_subprefeituras_sp()
    
    inspect_geojson(distritos, "Distritos")
    inspect_geojson(subprefeituras, "Subprefeituras")
    
    context = {
        'distritos_fields': list(distritos['features'][0]['properties'].keys()) if distritos and distritos.get('features') else [],
        'subprefeituras_fields': list(subprefeituras['features'][0]['properties'].keys()) if subprefeituras and subprefeituras.get('features') else [],
        'distritos_count': len(distritos.get('features', [])) if distritos else 0,
        'subprefeituras_count': len(subprefeituras.get('features', [])) if subprefeituras else 0,
    }
    
    return render(request, 'visualization/debug.html', context)

#   View de Debug para ciclovias
def ciclovias_debug(request):
    """Página específica para debug das ciclovias"""
    from .utils.geo_utils import inspect_ciclovias_data
    import json
    
    ciclovias_data = inspect_ciclovias_data()
    
    context = {
        'ciclovias_fields': list(ciclovias_data['features'][0]['properties'].keys()) if ciclovias_data and ciclovias_data.get('features') else [],
        'ciclovias_count': len(ciclovias_data.get('features', [])) if ciclovias_data else 0,
        'ciclovias_sample': json.dumps(ciclovias_data['features'][0]['properties'], indent=2, ensure_ascii=False) if ciclovias_data and ciclovias_data.get('features') else "Nenhum dado",
    }
    
    return render(request, 'visualization/ciclovias_debug.html', context)