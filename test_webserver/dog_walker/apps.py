from django.apps import AppConfig


class DogWalkerConfig(AppConfig):
    name = 'dog_walker'

    def ready(self):
        import dog_walker.signals