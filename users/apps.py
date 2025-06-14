#apps.py  C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\users\apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
