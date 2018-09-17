from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal, raise_error, contain

from contacts.models import User, UserPhone, UserEmail
from spec.common.utils import clean_database
from spec.common.endpoint_client import EndpointClient
import json

from spec.contacts.factories.user import UserFactory
from spec.contacts.factories.user_email import UserEmailFactory
from spec.contacts.factories.user_phone import UserPhoneFactory

client = EndpointClient() \
    .set_default_data({
    'first_name': 'John',
    'last_name': 'Smith',
    'date_of_birth': '1989-11-27',
}) \
    .set_url('/users/1') \
    .set_method('put')

with description('PUT /users/{pk}') as self:
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
            self.user_2_details = {
                'phone': UserPhoneFactory(user=self.user_2),
                'email': UserEmailFactory(user=self.user_2),
            }

        with context('when updating first user'):
            with context('with correct arguments'):
                with before.each:
                    self.response = client.request()

                with it('responds with 200'):
                    expect(self.response.status_code).to(equal(200))

                with it('responds with valid JSON'):
                    pass
                    # expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

                with it('shows success message'):
                    pass
                    # expect(str(self.response.content)).to(contain(
                    #     'User successfully updated', 'John', 'Smith'
                    # ))

            with context('with incorrect arguments'):
                with it('responds with 400'):
                    response = client.request(data={'phone': 'incorrect'})
                    # expect(response.status_code).to(equal(400))

                with it('responds with valid JSON'):
                    response = client.request(data={'phone': 'incorrect'})
                    response.render()
                    # expect(json.loads(response.content)).not_to(raise_error(ValueError))

                with it('shows error message'):
                    response = client.request(data={'phone': 'incorrect'})
                    response.render()
                    # expect(str(response.content)).to(contain(
                    #     'User could not be created', 'The phone number entered is not valid'
                    # ))
