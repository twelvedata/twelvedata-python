# coding: utf-8

import requests
from json import JSONDecodeError

from .exceptions import (
    BadRequestError,
    InternalServerError,
    InvalidApiKeyError,
    TwelveDataError,
)

__all__ = ("DefaultHttpClient",)


class DefaultHttpClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, relative_url, *args, **kwargs):

        # For the sake of monitoring, we add a "source" parameter
        params = kwargs.get("params", {})
        params["source"] = "python"
        kwargs["params"] = params

        resp = requests.get("{}{}".format(self.base_url, relative_url), timeout=30, *args, **kwargs)
        if ('Is_batch' in resp.headers and resp.headers['Is_batch'] == 'true') or \
                ('Content-Type' in resp.headers and resp.headers['Content-Type'] == 'text/csv'):
            return resp

        if not resp.ok:
            self._raise_error(resp.status_code, resp.text)

        json_resp = resp.json()
        if 'status' not in json_resp:
            return resp

        status = json_resp['status']
        if status == 'error':
            error_code = json_resp['code']
        else:
            return resp

        try:
            message = json_resp["message"]
        except ValueError:
            message = resp.text

        self._raise_error(error_code, message)

    @staticmethod
    def _raise_error(error_code, message):
        if error_code == 401:
            raise InvalidApiKeyError(message)

        if error_code == 400:
            raise BadRequestError(message)

        if error_code >= 500:
            raise InternalServerError(message)

        raise TwelveDataError(message)
