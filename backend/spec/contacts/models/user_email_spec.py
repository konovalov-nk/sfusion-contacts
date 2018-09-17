from django.db import IntegrityError
from expects import expect, raise_error
from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from spec.contacts.factories.user_email import UserEmailFactory
from spec.common.utils import clean_database, validate_field

with description('User Email'):
    with before.each:
        clean_database()

    with context('when creating') as self:
        with before.each:
            self.user_email = UserEmailFactory()

        with it('raises ValidationError if email is empty'):
            self.user_email.email = ''
            validate_field(self.user_email, 'email')

        with it('raises ValidationError if email is not valid'):
            self.user_email.email = 'invalidemail'
            validate_field(self.user_email, 'email')

        with it('raises IntegrityError if email is not unique'):
            expect(lambda: UserEmailFactory(email=self.user_email.email)).to(raise_error(IntegrityError))
