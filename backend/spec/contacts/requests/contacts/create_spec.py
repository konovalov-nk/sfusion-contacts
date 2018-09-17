from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal, raise_error, contain

from contacts.models import User, UserPhone, UserEmail
from spec.common.utils import clean_database
from spec.common.endpoint_client import EndpointClient
import json

client = EndpointClient()\
    .set_default_data({
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '1989-11-27',
        'email': 'john.smith@example.com',
        'phone': '+12025550160'
    })\
    .set_url('/users')\
    .set_method('post')

with description('POST /users') as self:
    with before.each:
        clean_database()

    with context('when creating a new contact'):
        with context('with correct arguments'):
            with before.each:
                self.response = client.request()

            with it('responds with 201'):
                expect(self.response.status_code).to(equal(201))

            with it('dw with valid JSON'):
                expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

            with it('shows success message'):
                expect(self.response.content.decode()).to(contain(
                    'User successfully created', 'John', 'Smith'
                ))

            with it('shows phone number and email'):
                expect(self.response.content.decode()).to(contain(
                    '+12025550160', 'john.smith@example.com'
                ))

            with it('creates `user` record in database'):
                expect(User.objects.count()).to(equal(1))

            with it('creates `user_phone` record in database'):
                expect(UserPhone.objects.count()).to(equal(1))

            with it('creates `user_email` record in database'):
                expect(UserEmail.objects.count()).to(equal(1))

        with context('with incorrect arguments'):
            with it('responds with 400'):
                response = client.request(data={'phone': 'incorrect'})
                expect(response.status_code).to(equal(400))

            with it('responds with valid JSON'):
                response = client.request(data={'phone': 'incorrect'})
                response.render()
                expect(json.loads(response.content)).not_to(raise_error(ValueError))

            with it('shows error message'):
                response = client.request(data={'phone': 'incorrect'})
                response.render()
                expect(response.content.decode()).to(contain(
                    'User could not be created', 'The phone number entered is not valid'
                ))

            with it("doesn't create `user` record in database"):
                client.request(data={'first_name': ''})
                expect(User.objects.count()).to(equal(0))

            with it("doesn't create `user_phone` record in database"):
                client.request(data={'phone': 'incorrect'})
                expect(UserPhone.objects.count()).to(equal(0))

            with it("doesn't create `user_email` record in database"):
                client.request(data={'email': 'incorrect'})
                expect(UserEmail.objects.count()).to(equal(0))
