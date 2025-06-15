# main/utils/db_utils.py

from django.db import connections

def use_replica():
    """
    Cambia la conexión predeterminada a la base de datos réplica.
    """
    connections['default'].alias = 'replica'
