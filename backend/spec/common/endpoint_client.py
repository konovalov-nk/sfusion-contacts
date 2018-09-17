from rest_framework.test import APIClient


class EndpointClient:
    """
    Wrapper around APIClient for a little bit easier way to setup default data.
    """
    default_data = {}
    url = '/users'
    http_method = 'post'

    def set_default_data(self, data):
        self.default_data = data

        return self

    def set_method(self, method):
        self.http_method = method

        return self

    def set_url(self, endpoint):
        self.url = endpoint

        return self

    def request(self, url=None, data: dict=None):
        if url is None:
            url = self.url
        if data is None:
            data = self.default_data
        else:
            if not isinstance(data, dict):
                raise TypeError('data is expected to be of dict type')

            for key, value in data.items():
                self.default_data[key] = value
            data = self.default_data

        return getattr(APIClient(enforce_csrf_checks=True), self.http_method)(url, data)