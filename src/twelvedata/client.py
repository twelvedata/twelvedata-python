from .context import Context
from .endpoints import (
    StocksListEndpoint,
    StockExchangesListEndpoint,
    ForexPairsListEndpoint,
    ETFListEndpoint,
    IndicesListEndpoint,
    ExchangesListEndpoint,
    CryptocurrenciesListEndpoint,
    CryptocurrencyExchangesListEndpoint,
    TechnicalIndicatorsListEndpoint,
    SymbolSearchEndpoint,
    EarliestTimestampEndpoint,
    EarningsEndpoint,
    EarningsCalendarEndpoint,
)
from .http_client import DefaultHttpClient
from .time_series import TimeSeries
from .utils import patch_endpoints_meta
from .websocket import TDWebSocket


class TDClient:
    def __init__(self, apikey, http_client=None, base_url=None, **defaults):
        self.ctx = Context()
        self.ctx.apikey = apikey
        self.ctx.base_url = base_url or "https://api.twelvedata.com"
        self.ctx.http_client = http_client or DefaultHttpClient(self.ctx.base_url)
        self.ctx.defaults = defaults

        patch_endpoints_meta(self.ctx)

    def websocket(self, **defaults):
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TDWebSocket(ctx)

    def get_stocks_list(self, **defaults):
        """
        Creates request builder for Stocks List

        This API call return array of symbols available at twelvedata API.
        This list is daily updated.

        :returns: request builder instance
        :rtype: StocksListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return StocksListEndpoint(ctx, **ctx.defaults)

    def get_stock_exchanges_list(self):
        """
        Creates request builder for Stock Exchanges List

        This API call return array of stock exchanges available at twelvedata
        API. This list is daily updated.

        :returns: request builder instance
        :rtype: StockExchangesListRequestBuilder
        """
        return StockExchangesListEndpoint(ctx=self.ctx)

    def get_forex_pairs_list(self, **defaults):
        """
        Creates request builder for Forex Pairs List

        This API call return array of forex pairs available at twelvedata API.
        This list is daily updated.

        :returns: request builder instance
        :rtype: ForexPairsListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ForexPairsListEndpoint(ctx, **ctx.defaults)

    def get_cryptocurrencies_list(self, **defaults):
        """
        Creates request builder for Cryptocurrencies List

        This API call return array of cryptocurrency pairs available at
        twelvedata API. This list is daily updated.

        :returns: request builder instance
        :rtype: CryptocurrenciesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CryptocurrenciesListEndpoint(ctx, **ctx.defaults)

    def get_etf_list(self, **defaults):
        """
        Creates request builder for ETF List

        This API call return array of ETFs available at Twelve Data API. This list is daily updated.
        This list is daily updated.

        :returns: request builder instance
        :rtype: ETFListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFListEndpoint(ctx, **ctx.defaults)

    def get_indices_list(self, **defaults):
        """
        Creates request builder for Indices List

        This API call return array of indices available at Twelve Data API. This list is daily updated.
        This list is daily updated.

        :returns: request builder instance
        :rtype: IndicesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IndicesListEndpoint(ctx, **ctx.defaults)

    def get_exchanges_list(self, **defaults):
        """
        Creates request builder for Exchanges List

        This API call return array of stock, ETF or index exchanges available at Twelve Data API.
        This list is daily updated.

        :returns: request builder instance
        :rtype: ExchangesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ExchangesListEndpoint(ctx, **ctx.defaults)

    def get_cryptocurrency_exchanges_list(self, **defaults):
        """
        Creates request builder for Cryptocurrency Exchanges List

        This API call return array of cryptocurrency exchanges available at
        twelvedata API. This list is daily updated.

        :returns: request builder instance
        :rtype: CryptocurrencyExchangesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CryptocurrencyExchangesListEndpoint(ctx, **ctx.defaults)

    def get_technical_indicators_list(self):
        """
        Creates request builder for Technical Indicators List

        This API call return array of objects with available technical indicators. This endpoint might be used to build
        an abstract interface to make more convenient API calls from the application.

        :returns: request builder instance
        :rtype: TechnicalIndicatorsListRequestBuilder
        """
        return TechnicalIndicatorsListEndpoint(ctx=self.ctx)

    def symbol_search(self, **defaults):
        """
        Creates request builder for Symbol Search

        This method helps to find the best matching symbol. It can be used as the base for custom lookups.
        The response is returned in descending order, with the most relevant instrument at the beginning.

        :returns: request builder instance
        :rtype: SymbolSearchRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return SymbolSearchEndpoint(ctx, **ctx.defaults)

    def get_earliest_timestamp(self, **defaults):
        """
        Creates request builder for Earliest Timestamp

        This method returns the first available DateTime for a given instrument at the specific interval.

        :returns: request builder instance
        :rtype: EarliestTimestampRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EarliestTimestampEndpoint(ctx, **ctx.defaults)

    def time_series(self, **defaults):
        """
        Creates factory for time series requests.

        :returns: request factory instance
        :rtype: TimeSeries
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TimeSeries(ctx)

    def get_earnings(self, **defaults):
        """
        Creates request builder for Earnings

        This API call returns earnings data for a given company, including EPS estimate and EPS actual.
        Earnings are available for complete company history.

        :returns: request builder instance
        :rtype: EarningsRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EarningsEndpoint(ctx, **ctx.defaults)

    def get_earnings_calendar(self, **defaults):
        """
        Creates request builder for Earnings Calendar

        This API method returns earning data as a calendar for a given date range. By default today's earning is returned.
        To call custom period, use start_date and end_date parameters.

        :returns: request builder instance
        :rtype: EarningsCalendarRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EarningsCalendarEndpoint(ctx, **ctx.defaults)
