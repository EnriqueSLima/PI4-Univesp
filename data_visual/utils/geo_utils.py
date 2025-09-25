#   Este arquivo contém funções para tratamento de arquivos .geojson

import requests
import json
import os
from django.conf import settings
from pyproj import Transformer

class CoordinateConverter:
    def __init__(self):
        # Conversão UTM para Lat/Long (SP está no fuso 23S - EPSG:31983)
        self.transformer = Transformer.from_crs(
            "EPSG:31983",  # SIRGAS 2000 / UTM zone 23S (usado pelo GeoSampa)
            "EPSG:4326",   # WGS84 (Lat/Long)
            always_xy=True
        )
    
    def convert_geojson(self, geojson_data):
        """Converte todo o GeoJSON de UTM para Lat/Long"""
        if not geojson_data or 'features' not in geojson_data:
            return geojson_data
        
        converted_features = []
        for feature in geojson_data['features']:
            converted_feature = self.convert_feature(feature)
            if converted_feature:
                converted_features.append(converted_feature)
        
        return {
            'type': 'FeatureCollection',
            'features': converted_features
        }
    
    def convert_feature(self, feature):
        """Converte uma feature individual"""
        if 'geometry' not in feature or 'coordinates' not in feature['geometry']:
            return feature
        
        geometry = feature['geometry']
        converted_coords = self.convert_coordinates(geometry['coordinates'], geometry['type'])
        
        return {
            'type': 'Feature',
            'properties': feature.get('properties', {}),
            'geometry': {
                'type': geometry['type'],
                'coordinates': converted_coords
            }
        }
    
    def convert_coordinates(self, coordinates, geom_type):
        """Converte coordenadas baseado no tipo de geometria"""
        if geom_type == 'Point':
            return self.convert_point(coordinates)
        elif geom_type == 'LineString':
            return self.convert_linestring(coordinates)
        elif geom_type == 'Polygon':
            return self.convert_polygon(coordinates)
        elif geom_type == 'MultiPolygon':
            return self.convert_multipolygon(coordinates)
        else:
            return coordinates
    
    def convert_point(self, coords):
        """Converte um ponto UTM → Lat/Long"""
        try:
            lon, lat = self.transformer.transform(coords[0], coords[1])
            return [lon, lat]
        except Exception as e:
            print(f"Erro na conversão do ponto: {e}")
            return coords
    
    def convert_linestring(self, coords_list):
        """Converte uma LineString"""
        return [self.convert_point(coord) for coord in coords_list]
    
    def convert_polygon(self, polygons):
        """Converte um Polygon (lista de anéis)"""
        return [self.convert_linestring(ring) for ring in polygons]
    
    def convert_multipolygon(self, multipolygons):
        """Converte um MultiPolygon"""
        return [self.convert_polygon(polygon) for polygon in multipolygons]

# Instância global do conversor
coord_converter = CoordinateConverter()

def get_sp_geojson():
    """Obtém GeoJSON dos limites de São Paulo do IBGE"""
    url = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3550308?formato=application/vnd.geo+json&qualidade=minima"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        geojson_data = response.json()
        
        # Adicionar campo 'nome' se não existir
        for feature in geojson_data['features']:
            if 'properties' not in feature:
                feature['properties'] = {}
            if 'nome' not in feature['properties']:
                feature['properties']['nome'] = 'São Paulo'
                
        return geojson_data
        
    except requests.RequestException:
        # Fallback para GeoJSON local simplificado
        return create_simple_sp_geojson()

def create_simple_sp_geojson():
    """Cria um GeoJSON simples para São Paulo"""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nome": "São Paulo",
                    "codarea": "3550308"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-46.825, -23.700], 
                        [-46.365, -23.700], 
                        [-46.365, -23.400], 
                        [-46.825, -23.400], 
                        [-46.825, -23.700]
                    ]]
                }
            }
        ]
    }

def get_available_fields(geojson):
    """Retorna os campos disponíveis no GeoJSON"""
    if not geojson or 'features' not in geojson or not geojson['features']:
        return []
    
    first_feature = geojson['features'][0]
    if 'properties' in first_feature:
        return list(first_feature['properties'].keys())
    return []

def load_local_geojson(filename):
    """Carrega arquivo GeoJSON da pasta static e converte coordenadas"""
    try:
        # Caminho para a pasta static
        static_path = os.path.join(settings.BASE_DIR, 'data_visual', 'static', 'data_visual', 'geojson')
        file_path = os.path.join(static_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
            
        # Converter coordenadas UTM para Lat/Long
        print(f"📁 Carregando {filename}...")
        converted_data = coord_converter.convert_geojson(geojson_data)
        print(f"✅ {filename} convertido com sucesso")
        
        return converted_data
        
    except Exception as e:
        print(f"❌ Erro ao carregar {filename}: {e}")
        return None

def get_distritos_sp():
    """Carrega GeoJSON dos distritos com conversão de coordenadas"""
    return load_local_geojson('geoportal_distrito_municipal_v2.geojson')

def get_subprefeituras_sp():
    """Carrega GeoJSON das subprefeituras com conversão de coordenadas"""
    return load_local_geojson('geoportal_subprefeitura_v2.geojson')

def inspect_geojson(geojson_data, name="GeoJSON"):
    """Inspeciona a estrutura do GeoJSON para debug"""
    if not geojson_data:
        print(f"{name}: Arquivo não encontrado ou vazio")
        return
    
    print(f"\n=== {name} ===")
    print(f"Tipo: {geojson_data.get('type', 'Desconhecido')}")
    print(f"Número de features: {len(geojson_data.get('features', []))}")
    
    if geojson_data.get('features'):
        first_feature = geojson_data['features'][0]
        print(f"Campos disponíveis: {list(first_feature.get('properties', {}).keys())}")
        
        # Verificar coordenadas de exemplo (após conversão)
        geometry = first_feature.get('geometry', {})
        if geometry and geometry.get('coordinates'):
            coords = geometry['coordinates']
            if geometry['type'] == 'Polygon' and coords:
                first_coord = coords[0][0] if coords[0] else []
                print(f"Primeira coordenada: {first_coord}")
                # Verificar se as coordenadas estão no formato correto
                if first_coord and len(first_coord) == 2:
                    lon, lat = first_coord
                    if -180 <= lon <= 180 and -90 <= lat <= 90:
                        print("✅ Coordenadas no formato Lat/Long correto")
                    else:
                        print("❌ Coordenadas fora do range Lat/Long (provavelmente UTM)")

def validate_geojson_plotting(geojson_data, name="GeoJSON"):
    """Valida se o GeoJSON pode ser plotado"""
    if not geojson_data:
        print(f"❌ {name}: Dados vazios")
        return False
    
    if geojson_data.get('type') != 'FeatureCollection':
        print(f"❌ {name}: Tipo incorreto. Esperado: FeatureCollection, Obtido: {geojson_data.get('type')}")
        return False
    
    features = geojson_data.get('features', [])
    if not features:
        print(f"❌ {name}: Nenhuma feature encontrada")
        return False
    
    print(f"✅ {name}: {len(features)} features válidas")
    
    # Verificar se as coordenadas estão no formato correto
    first_feature = features[0]
    geometry = first_feature.get('geometry', {})
    if geometry and geometry.get('coordinates'):
        coords = geometry['coordinates']
        if geometry['type'] == 'Polygon' and coords and coords[0]:
            first_coord = coords[0][0]
            if first_coord and len(first_coord) == 2:
                lon, lat = first_coord
                if -180 <= lon <= 180 and -90 <= lat <= 90:
                    print("✅ Coordenadas no formato Lat/Long correto")
                    return True
                else:
                    print("❌ Coordenadas fora do range Lat/Long")
                    return False
    
    return True

def get_ciclovias_sp():
    """Carrega GeoJSON das ciclovias"""
    return load_local_geojson('geoportal_via_bicicleta.geojson')

def inspect_ciclovias_data():
    """Função especial para debug das ciclovias"""
    ciclovias_data = get_ciclovias_sp()
    inspect_geojson(ciclovias_data, "Ciclovias")
    
    if ciclovias_data and ciclovias_data.get('features'):
        first_feature = ciclovias_data['features'][0]
        print("📋 Propriedades da primeira ciclovia:")
        for key, value in first_feature.get('properties', {}).items():
            print(f"   {key}: {value}")
    
    return ciclovias_data