from mamba import description, context, it, before, \
    fdescription, fcontext, fit
from expects import expect, equal

with description('views') as self:
    with it('is example spec'):
        expect(1).to(equal(1))
