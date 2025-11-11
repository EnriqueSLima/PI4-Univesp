import time
import threading
from django.utils import timezone
from django.db import close_old_connections
from .models import AirQualityData  # ajuste o import do seu model

def should_collect_data():
    """
    Verifica se precisa coletar dados baseado no último registro
    Retorna True se o último registro tem mais de 50 minutos
    """
    try:
        # Buscar o registro mais recente de qualquer estação
        last_record = AirQualityData.objects.order_by('-timestamp').first()
        
        if not last_record:
            print("📭 Nenhum registro no banco - Coletando dados...")
            return True
        
        # Calcular diferença em minutos
        now = timezone.now()
        time_diff = (now - last_record.timestamp).total_seconds() / 60
        
        print(f"⏰ Último registro: {last_record.timestamp}")
        print(f"🕐 Diferença: {time_diff:.1f} minutos")
        
        # Se o último registro tem mais de 50 minutos, coletar novos dados
        if time_diff > 50:
            print(f"✅ Precisa coletar - Último registro tem {time_diff:.1f} minutos")
            return True
        else:
            print(f"⏸️  Aguardando - Último registro tem apenas {time_diff:.1f} minutos")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar último registro: {e}")
        return True  # Em caso de erro, coleta para garantir

def auto_collect_if_needed():
    """
    Verifica e executa a coleta se necessário
    """
    from data_process.services import collect_last_hour_data_all_stations
    
    if should_collect_data():
        print("🚀 Iniciando coleta automática...")
        try:
            close_old_connections()  # Fechar conexões antigas
            result = collect_last_hour_data_all_stations()
            print(f"✅ Coleta automática concluída: {result.get('total_records_saved', 0)} registros")
            return result
        except Exception as e:
            print(f"❌ Erro na coleta automática: {e}")
            return None
    else:
        print("⏸️  Coleta não necessária no momento")
        return None

def start_auto_collector():
    """
    Inicia o coletor automático em background
    Verifica a cada 10 minutos se precisa coletar dados
    """
    print("🔍 Iniciando verificador automático de coleta...")
    print("📋 Verificando a cada 10 minutos se precisa coletar dados")
    
    while True:
        try:
            print(f"\n🕐 Verificação automática - {timezone.now().strftime('%d/%m/%Y %H:%M')}")
            auto_collect_if_needed()
            print("💤 Aguardando 10 minutos para próxima verificação...")
            time.sleep(600)  # 10 minutos = 600 segundos
            
        except Exception as e:
            print(f"💥 Erro no verificador automático: {e}")
            time.sleep(300)  # Espera 5 minutos em caso de erro e continua

def init_auto_collector():
    """
    Inicializa o coletor automático em thread separada
    """
    # Esperar o Django carregar completamente
    time.sleep(30)
    
    collector_thread = threading.Thread(
        target=start_auto_collector,
        daemon=True,
        name="AutoCollector"
    )
    collector_thread.start()
    
    print("🎯 Coletor automático iniciado!")