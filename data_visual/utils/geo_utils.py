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
    url = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3550308?formato=application/vnd.geo+json&qualidade=maxima"
    
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
        return False

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
        #print(f"❌ Erro ao carregar {filename}: {e}")
        return None

def get_distritos_sp():
    """Carrega GeoJSON dos distritos com conversão de coordenadas"""
    return load_local_geojson('geoportal_distrito_municipal_v2.geojson')

def get_subprefeituras_sp():
    """Carrega GeoJSON das subprefeituras com conversão de coordenadas"""
    return load_local_geojson('geoportal_subprefeitura_v2.geojson')

def get_areaverde_sp():
    """Carrega GeoJSON das praças e largos com conversão de coordenadas"""
    return load_local_geojson('praca_largo.geojson')

