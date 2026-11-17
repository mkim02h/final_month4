from django.apps import AppConfig
from django.db.backends.signals import connection_created


class AdsConfig(AppConfig):
    name = 'ads'
    verbose_name = 'Объявления'

