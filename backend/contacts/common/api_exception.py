from rest_framework.views import exception_handler
from contacts.common.api_response import api_error


def api_exception(exc, context):
    response = exception_handler(exc, context)

    return api_error(message=response.data['detail'], http_code=response.status_code)
