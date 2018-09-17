from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from spec.contacts.factories.user import UserFactory
from spec.common.utils import clean_database, validate_field

with description('User'):
    with before.each:
        clean_database()

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
