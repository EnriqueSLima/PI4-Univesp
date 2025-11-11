from django.apps import AppConfig
import threading

#class DataProcessConfig(AppConfig):
#    default_auto_field = 'django.db.models.BigAutoField'
#    name = 'data_process'
#
#
#class SeuAppConfig(AppConfig):
#    default_auto_field = 'django.db.models.BigAutoField'
#    name = 'seu_app'
class DataProcessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_process'
    
    def ready(self):
        """
        Inicia o coletor automático quando o app carrega
        """
        from django.conf import settings
        
        #if not settings.TESTING:
        from .auto_collector import init_auto_collector
        
        # Inicia após 45 segundos
        timer = threading.Timer(45.0, init_auto_collector)
        timer.daemon = True
        timer.start()