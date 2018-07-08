import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


def configure(settings):
    # Do nothing
    return

