from django.db import connections

def consulta_desde_replica():
    try:
        with connections['replica'].cursor() as cursor:
            cursor.execute("SELECT * FROM users_user")
            return cursor.fetchall()
    except Exception as e:
        print("Error consultando réplica:", e)
        return []

resultados = consulta_desde_replica()
print(resultados)
