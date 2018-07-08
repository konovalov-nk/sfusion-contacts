from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, raise_error, have_key
from contacts.models import User
from django.core.validators import ValidationError

with description('User'):
    with context('when creating') as self:
        with before.each:
            self.user = User.objects.create(first_name="John", last_name="Doe")

        with it('raises ValidationError if first_name is empty'):
            self.user.first_name = ''
            expect(lambda: self.user.clean_fields()).to(raise_error(ValidationError, have_key('first_name')))

        with it('raises ValidationError if first_name is over 100 characters'):
            self.user.first_name = 'x' * 101
            expect(lambda: self.user.clean_fields()).to(raise_error(ValidationError, have_key('first_name')))

        with it('raises ValidationError if last_name is empty'):
            self.user.last_name = ''
            expect(lambda: self.user.clean_fields()).to(raise_error(ValidationError, have_key('last_name')))

        with it('raises ValidationError if last_name is over 100 characters'):
            self.user.last_name = 'x' * 101
            expect(lambda: self.user.clean_fields()).to(raise_error(ValidationError, have_key('last_name')))

