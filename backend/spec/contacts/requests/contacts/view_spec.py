from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal, raise_error, contain

from contacts.models import User, UserPhone, UserEmail
from spec.common.utils import clean_database, prevent_request_warnings
from spec.common.endpoint_client import EndpointClient
import json

from spec.contacts.factories.user import UserFactory
from spec.contacts.factories.user_email import UserEmailFactory
from spec.contacts.factories.user_phone import UserPhoneFactory

client = EndpointClient() \
    .set_url('/users/1/details') \
    .set_method('get')


with description('GET /users/{pk}/details') as self:
    with before.each:
        clean_database()

    with context('given two users exist in database'):
        with before.each:
            self.user_1 = UserFactory()
            self.user_1_details = {
                'phone': UserPhoneFactory(user=self.user_1),
                'email': UserEmailFactory(user=self.user_1),
            }

            self.user_2 = UserFactory()

        with context('when retrieving existing user'):
            with before.each:
                client.set_url('/users/1/details')
                self.response = client.request()

            with it('responds with 200'):
                expect(self.response.status_code).to(equal(200))

            with it('responds with valid JSON'):
                expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

            with it('shows user details'):
                expect(self.response.content.decode()).to(contain(
                    self.user_1.first_name, self.user_1.last_name, self.user_1.date_of_birth,
                    self.user_1_details['phone'].phone.as_e164,
                    self.user_1_details['email'].email,
                ))

        with context('when retrieving non-existing user'):
            with before.each:
                self.response = prevent_request_warnings(lambda: client.request(url='/users/5/details'))()
                self.response.render()

            with it('responds with 404'):
                expect(self.response.status_code).to(equal(404))

            with it('responds with valid JSON'):
                expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

            with it('shows error message'):
                expect(self.response.content.decode()).to(contain(
                    'User does not exist'
                ))


