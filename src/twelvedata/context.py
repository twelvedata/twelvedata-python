# coding: utf-8


class Context:
    """
    Context which used by all request builders

    :ivar http_client: Default HTTP client
    :ivar apikey: API key for access to the Twelvedata API
    :ivar base_url: Base URL for Twelvedata API
    :ivar defaults: Default parameters that will be used by request builders.
    """

    http_client = None
    apikey = None
    base_url = None
    defaults = None

    @classmethod
    def from_context(cls, ctx):
        """
        Creates copy of specified Context
        """
        instance = cls()
        instance.http_client = ctx.http_client
        instance.apikey = ctx.apikey
        instance.base_url = ctx.base_url
        instance.defaults = dict(ctx.defaults or {})
        return instance
