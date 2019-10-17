# coding: utf-8

__all__ = (
    "TwelveDataError",
    "BadRequestError",
    "InternalServerError",
    "InvalidApiKeyError",
)


class TwelveDataError(RuntimeError):
    pass


class BadRequestError(TwelveDataError):
    pass


class InternalServerError(TwelveDataError):
    pass


class InvalidApiKeyError(TwelveDataError):
    pass
