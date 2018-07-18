from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, raise_error, have_key
from spec.contacts.factories.user import UserFactory
from django.core.validators import ValidationError


def validate_field(user, field_name):
    """
    Raises Validation error for provided field name.

    :param UserFactory user:
    :param String field_name:
    :return:
    """
    expect(lambda: user.clean_fields()).to(raise_error(ValidationError, have_key(field_name)))


with description('User'):
    with context('when creating') as self:
        with before.each:
            self.user = UserFactory()

        with it('raises ValidationError if first_name is empty'):
            self.user.first_name = ''
            validate_field(self.user, 'first_name')

        with it('raises ValidationError if first_name is over 100 characters'):
            self.user.first_name = 'x' * 101
            validate_field(self.user, 'first_name')

        with it('raises ValidationError if last_name is empty'):
            self.user.last_name = ''
            validate_field(self.user, 'last_name')

        with it('raises ValidationError if last_name is over 100 characters'):
            self.user.last_name = 'x' * 101
            validate_field(self.user, 'last_name')
