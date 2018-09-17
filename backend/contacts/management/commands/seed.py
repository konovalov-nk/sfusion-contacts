from random import randint
from django.core.management.base import BaseCommand
from spec.contacts.factories.user import UserFactory
from spec.contacts.factories.user_email import UserEmailFactory
from spec.contacts.factories.user_phone import UserPhoneFactory


class Command(BaseCommand):
    help = 'Populates database with some random data to play with.'

    def handle(self, *args, **options):
        amount = int(options['amount']) if options['amount'] else 15

        for i in range(0, amount):
            user = UserFactory()
            for j in range(0, randint(1, 5)):
                UserPhoneFactory(user=user)

            for k in range(0, randint(1, 5)):
                UserEmailFactory(user=user)

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            help='User records to be added to the database',
            action='store',
            dest='amount'
        )
