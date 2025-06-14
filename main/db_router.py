class ReplicaRouter:
    """
    Un router para controlar operaciones de base de datos:
    - Lecturas van a la base 'replicarailway'
    - Escrituras van a la base 'default'
    """

    def db_for_read(self, model, **hints):
        return 'replicarailway'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Permitir relaciones entre objetos en ambas bases
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permitir migraciones solo en la base default (o en ambas si quieres)
        if db == 'default':
            return True
        elif db == 'replicarailway':
            # Evita que migraciones modifiquen replica, si es solo para lectura
            return False
        return None
