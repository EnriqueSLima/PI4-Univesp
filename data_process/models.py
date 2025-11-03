# data_process/models.py

from django.db import models

class AirQualityData(models.Model):
    station_id = models.CharField(max_length=10)
    station_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Dados da poluição
    aqi = models.IntegerField()  # Índice de qualidade do ar
    co = models.FloatField()     # Monóxido de Carbono
    no = models.FloatField()     # Óxido Nítrico
    no2 = models.FloatField()    # Dióxido de Nitrogênio
    o3 = models.FloatField()     # Ozônio
    so2 = models.FloatField()    # Dióxido de Enxofre
    pm2_5 = models.FloatField()  # Material Particulado 2.5
    pm10 = models.FloatField()   # Material Particulado 10
    nh3 = models.FloatField()    # Amônia
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.station_name} - AQI: {self.aqi}"
    
    def get_aqi_description(self):
        """Retorna a descrição do índice de qualidade do ar"""
        aqi_levels = {
            1: "Boa",
            2: "Razoável", 
            3: "Moderada",
            4: "Ruim",
            5: "Muito Ruim"
        }
        return aqi_levels.get(self.aqi, "Desconhecido")
    
    def get_aqi_color(self):
        """Retorna a cor baseada no AQI"""
        aqi_colors = {
            1: "green",
            2: "lightgreen",
            3: "orange", 
            4: "red",
            5: "darkred"
        }
        return aqi_colors.get(self.aqi, "gray")
