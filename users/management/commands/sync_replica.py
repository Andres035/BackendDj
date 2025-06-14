from django.core.management.base import BaseCommand
from users.utils import consulta_desde_replica

class Command(BaseCommand):
    help = 'Consulta datos desde la réplica'

    def handle(self, *args, **kwargs):
        resultados = consulta_desde_replica('replicarailway')
        for fila in resultados:
            print(fila)
