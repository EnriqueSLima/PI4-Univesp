# data_process/management/commands/clear_air_quality_data.py
from django.core.management.base import BaseCommand
from data_process.models import AirQualityData

# Função para limpar os dados do banco
class Command(BaseCommand):
    help = 'Remove todos os dados de qualidade do ar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a exclusão sem confirmação',
        )

    def handle(self, *args, **options):
        total = AirQualityData.objects.count()
        
        if not options['force']:
            confirm = input(
                f"⚠️  TEM CERTEZA que quer excluir TODOS os {total} registros? "
                f"Isso não pode ser desfeito! (digite 'SIM' para confirmar): "
            )
            if confirm != 'SIM':
                self.stdout.write('❌ Operação cancelada')
                return

        # Exclui todos os registros
        deleted = AirQualityData.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Todos os {total} registros foram excluídos!')
        )