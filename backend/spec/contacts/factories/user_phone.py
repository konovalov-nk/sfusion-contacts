import factory

from contacts import models
from spec.contacts.factories.user import UserFactory
from faker_e164.providers import E164Provider
factory.faker.Faker.add_provider(E164Provider)


class UserPhoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserPhone

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('e164')
