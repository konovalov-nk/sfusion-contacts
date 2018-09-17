import factory

from contacts import models
from spec.contacts.factories.user import UserFactory


class UserEmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserEmail

    user = factory.SubFactory(UserFactory)
    email = factory.Faker('email')
