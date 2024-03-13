from django.apps import AppConfig


class NidsmodelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NidsModels'

    def ready(self):
        import NidsModels.Signal
