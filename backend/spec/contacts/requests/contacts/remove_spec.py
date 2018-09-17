import json

from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal, raise_error, contain

from contacts.models import User
from spec.common.utils import clean_database, prevent_request_warnings
from spec.common.endpoint_client import EndpointClient
from spec.contacts.factories.user import UserFactory

client = EndpointClient()\
    .set_default_data({
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '1989-11-27',
        'email': 'john.smith@example.com',
        'phone': '+12025550160'
    })\
    .set_url('/users/1')\
    .set_method('delete')

with description('DELETE /users/{pk}') as self:
    with before.each:
        clean_database()

    with context('given two users exist in database'):
        with before.each:
            self.user_1 = UserFactory()
            self.user_2 = UserFactory()

        with context('when deleting first one'):
            with before.each:
                self.response = client.request(url='/users/%d' % self.user_1.id)

            with it('responds with 200'):
                expect(self.response.status_code).to(equal(200))

            with it('deletes one `user` record from database'):
                expect(User.objects.count()).to(equal(1))

            with it('deletes only `user` specified by id'):
                expect(lambda: User.objects.get(pk=self.user_1.id)).to(raise_error(User.DoesNotExist))
                expect(lambda: User.objects.get(pk=self.user_2.id)).not_to(raise_error(User.DoesNotExist))

            with it('responds with valid JSON'):
                expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

            with it('shows success message'):
                expect(self.response.content.decode()).to(contain(
                    'User successfully deleted'
                ))

        with context('when deleting not an existing user'):
            with before.each:
                self.response = prevent_request_warnings(lambda: client.request(url='/users/3'))()

            with it('responds with 400'):
                expect(self.response.status_code).to(equal(404))

            with it("doesn't delete anything from `users` table"):
                expect(User.objects.count()).to(equal(2))

            with it('responds with valid JSON'):
                expect(json.loads(self.response.content)).not_to(raise_error(ValueError))

            with it('shows error message'):
                expect(self.response.content.decode()).to(contain(
                    'User does not exist'
                ))

