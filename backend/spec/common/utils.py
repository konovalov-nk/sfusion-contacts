from django.core.exceptions import ValidationError
from django.core.management import call_command
from expects import expect, raise_error, have_key
import logging


def prevent_request_warnings(original_function):
    """
    If we need to test for 404s or 405s this decorator can prevent the
    request class from throwing warnings.
    """
    def new_function(*args, **kwargs):
        # raise logging level to ERROR
        logger = logging.getLogger('django.request')
        previous_logging_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        # trigger original function that would throw warning
        result = original_function(*args, **kwargs)

        # lower logging level back to previous
        logger.setLevel(previous_logging_level)
        return result

    return new_function


def clean_database():
    """
    Just a simple wrapper for cleaning database before every unit-test.
    :return: None
    """
    # See management/commands/sqlite_flush.py why don't we use `flush` instead.
    call_command('sqlite_flush')


def validate_field(model, field_name, raises_error=True):
    """
    Raises Validation error for provided field name.

    :param django.db.models.Model model:
    :param String field_name:
    :param raises_error: true - if field validation raises error, false - otherwise
    :return:
    """
    expect_to = getattr(expect(lambda: model.clean_fields()), 'to' if raises_error else 'not_to')
    expect_to(raise_error(ValidationError, have_key(field_name)))

