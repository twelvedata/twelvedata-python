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

        resp = requests.get("{}{}".format(self.base_url, relative_url), *args, **kwargs)

        if resp.ok:
            return resp

        try:
            message = resp.json()["message"]
        except ValueError:
            message = resp.text

        if resp.status_code == 401:
            raise InvalidApiKeyError(message)

        if resp.status_code == 400:
            raise BadRequestError(message)

        if resp.status_code >= 500:
            raise InternalServerError(message)

        raise TwelveDataError(message)
