# data_process/management/commands/collect_historical_all.py
from django.core.management.base import BaseCommand
from data_process.services import collect_historical_data_all_stations

# Função para coletar os dados de todas as estações
class Command(BaseCommand):
    help = 'Coleta dados históricos para TODAS as estações'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=5,
            help='Número de dias para coletar (padrão: 5)',
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='Delay entre requisições em segundos (padrão: 1.0)',
        )
    
    def handle(self, *args, **options):
        days = options['days']
        delay = options['delay']
        
        self.stdout.write(
            self.style.WARNING(
                f'🚀 Iniciando coleta histórica para todas as estações...'
            )
        )
        
        resultado = collect_historical_data_all_stations(days=days, delay_between_requests=delay)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'🏁 Coleta concluída! '
                f'Total: {resultado["total_records_saved"]} registros salvos em '
                f'{resultado["success_count"]} estações'
            )
        )