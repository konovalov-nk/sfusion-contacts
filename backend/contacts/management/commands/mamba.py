from django.core.management.base import BaseCommand
from mamba import application_factory
from django.core.management import call_command
from django.conf import settings


class Settings(object):
    def __init__(self):
        self.slow = .075
        self.enable_coverage = False
        self.coverage_file = '.coverage'
        self.format = 'documentation'
        self.no_color = False
        self.tags = None
        self.specs = settings.BASE_DIR


class Command(BaseCommand):
    help = 'Runs Mamba tests'

    def handle(self, *args, **options):
        self.stdout.write(settings.DATABASES['default']['ENGINE'])
        call_command('migrate', verbosity=0)

        arguments = Settings()
        factory = application_factory.ApplicationFactory(arguments)
        runner = factory.runner()
        runner.run()
