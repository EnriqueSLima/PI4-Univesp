from django.core.management.base import BaseCommand
from data_process.auto_collector import auto_collect_if_needed

class Command(BaseCommand):
    help = 'Verifica e executa a coleta se necessário'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Verificando se precisa coletar dados...')
        result = auto_collect_if_needed()
        
        if result:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Coleta executada: {result["total_records_saved"]} registros')
            )
        else:
            self.stdout.write('⏸️  Coleta não necessária no momento')