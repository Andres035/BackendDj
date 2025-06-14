#C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\users\utils.py
from django.db import connections

def consulta_desde_replica(alias='replica'):
    with connections[alias].cursor() as cursor:
        cursor.execute("SELECT * FROM Usuarios")  # Cambia según tu tabla
        return cursor.fetchall()
