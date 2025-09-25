#   Este arquivo será utilizado para funções relacionadas a qualidade do ar

import folium

def get_color_by_quality(quality_index):
    """Retorna cor baseada na qualidade do ar"""
    if quality_index <= 40:
        return 'green'
    elif quality_index <= 80:
        return 'yellow'
    elif quality_index <= 120:
        return 'orange'
    else:
        return 'red'