from .context import Context
from .endpoints import (
    StocksListEndpoint,
    StockExchangesListEndpoint,
    ForexPairsListEndpoint,
    CryptocurrenciesListEndpoint,
    CryptocurrencyExchangesListEndpoint,
)
from .http_client import DefaultHttpClient
from .time_series import TimeSeries
from .utils import patch_endpoints_meta


class TDClient:
    def __init__(self, apikey, http_client=None, base_url=None, **defaults):
        self.ctx = Context()
        self.ctx.apikey = apikey
        self.ctx.base_url = base_url or "https://api.twelvedata.com"
        self.ctx.http_client = http_client or DefaultHttpClient(self.ctx.base_url)
        self.ctx.defaults = defaults

        patch_endpoints_meta(self.ctx)

    def get_stocks_list(self):
        """
        Creates request builder for Stocks List

        This API call return array of symbols available at twelvedata API.
        This list is daily updated.

        :returns: request builder instance
        :rtype: StocksListRequestBuilder
        """
        return StocksListEndpoint(ctx=self.ctx)

    def get_stock_exchanges_list(self):
        """
        Creates request builder for Stock Exchanges List

        This API call return array of stock exchanges available at twelvedata
        API. This list is daily updated.

        :returns: request builder instance
        :rtype: StockExchangesListRequestBuilder
        """
        return StockExchangesListEndpoint(ctx=self.ctx)

    def get_forex_pairs_list(self):
        """
        Creates request builder for Forex Pairs List

        This API call return array of forex pairs available at twelvedata API.
        This list is daily updated.

        :returns: request builder instance
        :rtype: ForexPairsListRequestBuilder
        """
        return ForexPairsListEndpoint(ctx=self.ctx)

    def get_cryptocurrencies_list(self):
        """
        Creates request builder for Cryptocurrencies List

        This API call return array of cryptocurrency pairs available at
        twelvedata API. This list is daily updated.

        :returns: request builder instance
        :rtype: CryptocurrenciesListRequestBuilder
        """
        return CryptocurrenciesListEndpoint(ctx=self.ctx)

    def get_cryptocurrency_exchanges_list(self):
        """
        Creates request builder for Cryptocurrency Exchanges List

        This API call return array of cryptocurrency exchanges available at
        twelvedata API. This list is daily updated.

        :returns: request builder instance
        :rtype: CryptocurrencyExchangesListRequestBuilder
        """
        return CryptocurrencyExchangesListEndpoint(ctx=self.ctx)

    def time_series(self, **defaults):
        """
        Creates factory for time series requests.

        :returns: request factory instance
        :rtype: TimeSeries
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TimeSeries(ctx)
