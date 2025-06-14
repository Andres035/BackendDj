from django.db import connections
from django.db.utils import OperationalError

class ReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'default'  # Siempre leer de default

    def db_for_write(self, model, **hints):
        return 'default'  # Siempre escribir en default

    def allow_relation(self, obj1, obj2, **hints):
        return True  # Permite relaciones entre bases

    def allow_migrate(self, db, app_label, model=None, **hints):
        if db == 'railway':
            return True
        if db == 'default':
            return True
        return False
