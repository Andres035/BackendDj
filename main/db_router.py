from django.db import connections
from django.db.utils import OperationalError

class ReplicaRouter:
    def db_for_read(self, model, **hints):
        # Siempre leer desde 'default'
        return 'default'

    def db_for_write(self, model, **hints):
        # Escribir en 'default'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Migrar solo en la base de datos 'default'
        return db == 'default'
