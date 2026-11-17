from django.apps import AppConfig
from django.db.backends.signals import connection_created


def unicode_lower(value):
    return value.lower() if isinstance(value, str) else value


def register_sqlite_functions(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        connection.connection.create_function('LOWER', 1, unicode_lower, deterministic=True)


class AdsConfig(AppConfig):
    name = 'ads'
    verbose_name = 'Объявления'

    def ready(self):
        connection_created.connect(register_sqlite_functions)
