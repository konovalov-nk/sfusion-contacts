from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal
from django.test.client import RequestFactory

with description('requests') as self:
    with it('is example spec'):
        expect(1).to(equal(1))
