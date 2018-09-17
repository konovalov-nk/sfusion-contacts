from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from contacts.models import User


class Command(BaseCommand):
    """
        Django doesn't reset auto-increment values in sqlite db using `flush` command by default,
         and it is 3x slower than doing things manually (there are few other tables we don't care about),
         and this class solves these issues.
    """

    help = 'Flushes sqlite tables'

    def handle(self, *args, **options):
        User.objects.all().delete()

        self._reset_sqlite_autoincrement()

    def _reset_sqlite_autoincrement(self):
        """
        Resets auto-increment
        :return: None
        """
        reset_sql = self._get_sqlite_reset_sql()

        with connection.cursor() as cursor:
            cursor.executescript(reset_sql)

    @staticmethod
    def _get_sqlite_reset_sql():
        """
        Generates SQL needed to reset auto-increment fields on sqlite tables.
        :return: String
        """
        app_models = apps.get_app_config('contacts').get_models()
        sql = ''

        for model in app_models:
            sql += """
                DELETE FROM sqlite_sequence WHERE name='%s';
            """ % model._meta.db_table

        return sql
