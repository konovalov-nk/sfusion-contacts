from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework.utils.urls import replace_query_param


def api_response(data=None, message='Request was successful', http_code=status.HTTP_200_OK, **kwargs):
    if data is None:
        data = {}

    return Response({
        'status': 'ok',
        'message': message,
        'data': data,
    }, status=http_code, **kwargs)


def api_error(errors=None, message='There was an error in your request', http_code=status.HTTP_400_BAD_REQUEST, **kwargs):
    if errors is None:
        errors = {}

    return Response({
        'status': 'error',
        'message': message,
        'errors': errors,
    }, status=http_code, **kwargs)


def api_paginated_response(request, queryset, serializer):
    paginator = ApiPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = serializer(result_page, context={'request': request}, many=True)

    return paginator.get_paginated_response(serializer.data)


class ApiPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = 'last'

        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1

        return replace_query_param(url, self.page_query_param, page_number)

    def get_self_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.number

        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return api_response({
            'meta': {
                'total-pages': self.page.paginator.count
            },
            'data': data,
            'links': {
                'self': self.get_self_link(),
                'first': self.get_first_link(),
                'prev': self.get_previous_link(),
                'next': self.get_next_link(),
                'last': self.get_last_link(),
            },
        })
