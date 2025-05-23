from django.apps import AppConfig


class DendoUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dendo_users'

    def ready(self):
        from . import signals