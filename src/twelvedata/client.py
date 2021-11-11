from .context import Context
from .endpoints import (
    CustomEndpoint,
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
    ExchangeRateEndpoint,
    CurrencyConversionEndpoint,
    QuoteEndpoint,
    PriceEndpoint,
    EODEndpoint,
    LogoEndpoint,
    ProfileEndpoint,
    DividendsEndpoint,
    SplitsEndpoint,
    EarningsEndpoint,
    EarningsCalendarEndpoint,
    IPOCalendarEndpoint,
    StatisticsEndpoint,
    InsiderTransactionsEndpoint,
    IncomeStatementEndpoint,
    BalanceSheetEndpoint,
    CashFlowEndpoint,
    OptionsExpirationEndpoint,
    OptionsChainEndpoint,
    KeyExecutivesEndpoint,
    InstitutionalHoldersEndpoint,
    FundHoldersEndpoint,
    APIUsageEndpoint,
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

    def custom_endpoint(self, **defaults):
        """
        Creates request builder for custom endpoint

        This method can request any GET endpoint available at Twelve Data
        with a custom set of parameters

        :returns: request builder instance
        :rtype: CustomEndpointRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CustomEndpoint(ctx, **ctx.defaults)

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

    def exchange_rate(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: ExchangeRate
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ExchangeRateEndpoint(ctx, **ctx.defaults)

    def currency_conversion(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: CurrencyConversion
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CurrencyConversionEndpoint(ctx, **ctx.defaults)

    def quote(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: Quote
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return QuoteEndpoint(ctx, **ctx.defaults)

    def price(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: Price
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return PriceEndpoint(ctx, **ctx.defaults)

    def eod(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: EOD
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EODEndpoint(ctx, **ctx.defaults)

    def get_logo(self, **defaults):
        """
        Creates request builder for Logo

        Returns logo of the company.

        :returns: request builder instance
        :rtype: LogoRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return LogoEndpoint(ctx, **ctx.defaults)

    def get_profile(self, **defaults):
        """
        Creates request builder for Profile

        Returns general information about the company.

        :returns: request builder instance
        :rtype: ProfileRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ProfileEndpoint(ctx, **ctx.defaults)

    def get_dividends(self, **defaults):
        """
        Creates request builder for Dividends

        Returns the amount of dividends paid out for the last 10+ years.

        :returns: request builder instance
        :rtype: DividendsRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return DividendsEndpoint(ctx, **ctx.defaults)

    def get_splits(self, **defaults):
        """
        Creates request builder for Splits

        Returns the date and the split factor of shares of the company for the last 10+ years.

        :returns: request builder instance
        :rtype: SplitsRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return SplitsEndpoint(ctx, **ctx.defaults)

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

    def get_ipo_calendar(self, **defaults):
        """
        Creates request builder for IPO Calendar

        This endpoint returns past, today, or upcoming IPOs.

        :returns: request builder instance
        :rtype: IPOCalendarRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IPOCalendarEndpoint(ctx, **ctx.defaults)

    def get_statistics(self, **defaults):
        """
        Creates request builder for Statistics

        Returns current overview of company’s main statistics including valuation metrics and financials.

        :returns: request builder instance
        :rtype: StatisticsRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return StatisticsEndpoint(ctx, **ctx.defaults)

    def get_insider_transactions(self, **defaults):
        """
        Creates request builder for Insider Transactions

        Returns trading information performed by insiders.

        :returns: request builder instance
        :rtype: InsiderTransactionsRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return InsiderTransactionsEndpoint(ctx, **ctx.defaults)

    def get_income_statement(self, **defaults):
        """
        Creates request builder for Income Statement

        Returns complete income statement of a company and shows the company’s revenues and expenses
        during a period (annual or quarter).

        :returns: request builder instance
        :rtype: IncomeStatementRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IncomeStatementEndpoint(ctx, **ctx.defaults)

    def get_balance_sheet(self, **defaults):
        """
        Creates request builder for Balance Sheet

        Returns complete balance sheet of a company showing the summary of assets, liabilities, and
        shareholders’ equity.

        :returns: request builder instance
        :rtype: BalanceSheetRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return BalanceSheetEndpoint(ctx, **ctx.defaults)

    def get_cash_flow(self, **defaults):
        """
        Creates request builder for Cash Flow

        Returns complete cash flow of a company showing net the amount of cash and cash equivalents
        being transferred into and out of a business.

        :returns: request builder instance
        :rtype: CashFlowRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CashFlowEndpoint(ctx, **ctx.defaults)

    def get_options_expiration(self, **defaults):
        """
        Creates request builder for Options Expiration

        Return the expiration dates of an option contract.

        :returns: request builder instance
        :rtype: OptionsExpirationRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return OptionsExpirationEndpoint(ctx, **ctx.defaults)

    def get_options_chain(self, **defaults):
        """
        Creates request builder for Options Chain

        Returns a listing of all available options contracts for given security. It shows all listed puts,
        calls, their expiration, strike prices, and pricing information for a single underlying asset
        within a given maturity period.

        :returns: request builder instance
        :rtype: OptionsChainRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return OptionsChainEndpoint(ctx, **ctx.defaults)

    def get_key_executives(self, **defaults):
        """
        Creates request builder for Key Executives

        Returns individuals at the highest level of management of an organization.

        :returns: request builder instance
        :rtype: KeyExecutivesRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return KeyExecutivesEndpoint(ctx, **ctx.defaults)

    def get_institutional_holders(self, **defaults):
        """
        Creates request builder for Institutional Holders

        Returns the amount of the company’s available stock owned by institutions (pension funds,
        insurance companies, investment firms, private foundations, endowments, or other large
        entities that manage funds on behalf of others).

        :returns: request builder instance
        :rtype: InstitutionalHoldersRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return InstitutionalHoldersEndpoint(ctx, **ctx.defaults)

    def get_fund_holders(self, **defaults):
        """
        Creates request builder for Fund Holders

        Returns the amount of the company’s available stock owned by mutual fund holders.

        :returns: request builder instance
        :rtype: FundHoldersRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return FundHoldersEndpoint(ctx, **ctx.defaults)

    def api_usage(self, **defaults):
        """
        Creates request builder for API usage

        This endpoint will provide information on the current usage of Twelve Data API.

        :returns: request builder instance
        :rtype: APIUsage
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return APIUsageEndpoint(ctx, **ctx.defaults)
