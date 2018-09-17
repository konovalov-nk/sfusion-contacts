from django.db import IntegrityError
from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal, raise_error
from spec.contacts.factories.user_phone import UserPhoneFactory
from spec.common.utils import clean_database, validate_field

with description('User Phone'):
    with before.each:
        clean_database()

    with context('when creating') as self:
        with before.each:
            self.user_phone = UserPhoneFactory()

        with it('raises ValidationError if phone is empty'):
            self.user_phone.phone = ''
            validate_field(self.user_phone, 'phone')

        with it('raises ValidationError if phone format is not E164'):
            self.user_phone.phone = '8-964-2912-21-22'
            validate_field(self.user_phone, 'phone')

        with it('raises IntegrityError if phone is not unique'):
            expect(lambda: UserPhoneFactory(phone=self.user_phone.phone)).to(raise_error(IntegrityError))

        with it('passes if phone format is E164'):
            self.user_phone.phone = '+79621112222'
            validate_field(self.user_phone, 'phone', False)

        with it('filters out some alpha and special characters'):
            self.user_phone.phone = 's+7-9(6211s]1[]2222S'
            self.user_phone.clean_fields()
            expect(self.user_phone.phone).to(equal('+79621112222'))
