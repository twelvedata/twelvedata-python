import warnings

from .context import Context
from .endpoints import (
    # Advanced
    APIUsageEndpoint,
    CustomEndpoint,
    # Analysis
    AnalystRatingsLightEndpoint,
    AnalystRatingsUSEquitiesEndpoint,
    EPSRevisionsEndpoint,
    EPSTrendEndpoint,
    EarningsEstimateEndpoint,
    GrowthEstimatesEndpoint,
    PriceTargetEndpoint,
    RecommendationsEndpoint,
    RevenueEstimateEndpoint,
    # Currencies
    CurrencyConversionEndpoint,
    ExchangeRateEndpoint,
    # ETFs
    ETFsDetailedListEndpoint,
    ETFsFamilyEndpoint,
    ETFsTypeEndpoint,
    ETFsWorldCompositionEndpoint,
    ETFsWorldEndpoint,
    ETFsWorldPerformanceEndpoint,
    ETFsWorldRiskEndpoint,
    ETFsWorldSummaryEndpoint,
    # Fundamentals
    BalanceSheetConsolidatedEndpoint,
    BalanceSheetEndpoint,
    CashFlowConsolidatedEndpoint,
    CashFlowEndpoint,
    DividendsCalendarEndpoint,
    DividendsEndpoint,
    EarningsCalendarEndpoint,
    EarningsEndpoint,
    IPOCalendarEndpoint,
    IncomeStatementConsolidatedEndpoint,
    IncomeStatementEndpoint,
    KeyExecutivesEndpoint,
    LastChangeEndpoint,
    LogoEndpoint,
    MarketCapEndpoint,
    PressReleasesEndpoint,
    ProfileEndpoint,
    SplitsCalendarEndpoint,
    SplitsEndpoint,
    StatisticsEndpoint,
    # Market Data
    EODEndpoint,
    MarketMoversEndpoint,
    PriceEndpoint,
    QuoteEndpoint,
    TimeSeriesCrossEndpoint,
    # Options (deprecated)
    OptionsChainEndpoint,
    OptionsExpirationEndpoint,
    # Mutual Funds
    MutualFundsFamilyEndpoint,
    MutualFundsListEndpoint,
    MutualFundsTypeEndpoint,
    MutualFundsWorldCompositionEndpoint,
    MutualFundsWorldEndpoint,
    MutualFundsWorldPerformanceEndpoint,
    MutualFundsWorldPurchaseInfoEndpoint,
    MutualFundsWorldRatingsEndpoint,
    MutualFundsWorldRiskEndpoint,
    MutualFundsWorldSummaryEndpoint,
    MutualFundsWorldSustainabilityEndpoint,
    # Reference Data
    BondsListEndpoint,
    CommoditiesListEndpoint,
    CountriesEndpoint,
    CrossListingsEndpoint,
    CryptocurrenciesListEndpoint,
    CryptocurrencyExchangesListEndpoint,
    ETFListEndpoint,
    EarliestTimestampEndpoint,
    ExchangeScheduleEndpoint,
    ExchangesListEndpoint,
    ForexPairsListEndpoint,
    FundsListEndpoint,
    IndicesListEndpoint,
    InstrumentTypeEndpoint,
    IntervalsEndpoint,
    MarketStateEndpoint,
    StockExchangesListEndpoint,
    StocksListEndpoint,
    SymbolSearchEndpoint,
    TechnicalIndicatorsListEndpoint,
    # Regulatory
    DirectHoldersEndpoint,
    EdgarFilingsArchiveEndpoint,
    FundHoldersEndpoint,
    InsiderTransactionsEndpoint,
    InstitutionalHoldersEndpoint,
    SanctionsEndpoint,
    TaxInfoEndpoint,
)
from .http_client import DefaultHttpClient
from .time_series import TimeSeries
from .utils import patch_endpoints_meta
from .websocket import TDWebSocket


class TDClient:
    def __init__(self, apikey, http_client=None, base_url=None, self_heal_time_s=None, **defaults):
        self.ctx = Context()
        self.ctx.apikey = apikey
        self.ctx.self_heal_time_s = self_heal_time_s
        self.ctx.base_url = base_url or "https://api.twelvedata.com"
        self.ctx.http_client = http_client or DefaultHttpClient(self.ctx.base_url)
        self.ctx.defaults = defaults

        patch_endpoints_meta(self.ctx)

    # Advanced

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

    def websocket(self, **defaults):
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TDWebSocket(ctx)

    # Analysis

    def get_analyst_ratings_light(self, **defaults):
        """
        Creates request builder for Analyst Ratings (Light).

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return AnalystRatingsLightEndpoint(ctx, **ctx.defaults)

    def get_analyst_ratings_us_equities(self, **defaults):
        """
        Creates request builder for Analyst Ratings (US Equities).

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return AnalystRatingsUSEquitiesEndpoint(ctx, **ctx.defaults)

    def get_earnings_estimate(self, **defaults):
        """
        Creates request builder for Earnings Estimate.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EarningsEstimateEndpoint(ctx, **ctx.defaults)

    def get_eps_revisions(self, **defaults):
        """
        Creates request builder for EPS Revisions.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EPSRevisionsEndpoint(ctx, **ctx.defaults)

    def get_eps_trend(self, **defaults):
        """
        Creates request builder for EPS Trend.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EPSTrendEndpoint(ctx, **ctx.defaults)

    def get_growth_estimates(self, **defaults):
        """
        Creates request builder for Growth Estimates.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return GrowthEstimatesEndpoint(ctx, **ctx.defaults)

    def get_price_target(self, **defaults):
        """
        Creates request builder for Price Target.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return PriceTargetEndpoint(ctx, **ctx.defaults)

    def get_recommendations(self, **defaults):
        """
        Creates request builder for Recommendations.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return RecommendationsEndpoint(ctx, **ctx.defaults)

    def get_revenue_estimate(self, **defaults):
        """
        Creates request builder for Revenue Estimate.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return RevenueEstimateEndpoint(ctx, **ctx.defaults)

    # Currencies

    def currency_conversion(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: CurrencyConversion
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CurrencyConversionEndpoint(ctx, **ctx.defaults)

    def exchange_rate(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: ExchangeRate
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ExchangeRateEndpoint(ctx, **ctx.defaults)

    # ETFs

    def get_etfs_family(self, **defaults):
        """
        Creates request builder for ETFs Family.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsFamilyEndpoint(ctx, **ctx.defaults)

    def get_etfs_list(self, **defaults):
        """
        Creates request builder for ETFs Detailed List.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsDetailedListEndpoint(ctx, **ctx.defaults)

    def get_etfs_type(self, **defaults):
        """
        Creates request builder for ETFs Type.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsTypeEndpoint(ctx, **ctx.defaults)

    def get_etfs_world(self, **defaults):
        """
        Creates request builder for ETFs World.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsWorldEndpoint(ctx, **ctx.defaults)

    def get_etfs_world_composition(self, **defaults):
        """
        Creates request builder for ETFs World Composition.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsWorldCompositionEndpoint(ctx, **ctx.defaults)

    def get_etfs_world_performance(self, **defaults):
        """
        Creates request builder for ETFs World Performance.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsWorldPerformanceEndpoint(ctx, **ctx.defaults)

    def get_etfs_world_risk(self, **defaults):
        """
        Creates request builder for ETFs World Risk.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsWorldRiskEndpoint(ctx, **ctx.defaults)

    def get_etfs_world_summary(self, **defaults):
        """
        Creates request builder for ETFs World Summary.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFsWorldSummaryEndpoint(ctx, **ctx.defaults)

    # Fundamentals

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

    def get_balance_sheet_consolidated(self, **defaults):
        """
        Creates request builder for Balance Sheet (Consolidated).

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return BalanceSheetConsolidatedEndpoint(ctx, **ctx.defaults)

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

    def get_cash_flow_consolidated(self, **defaults):
        """
        Creates request builder for Cash Flow (Consolidated).

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CashFlowConsolidatedEndpoint(ctx, **ctx.defaults)

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

    def get_dividends_calendar(self, **defaults):
        """
        Creates request builder for Dividends Calendar

        Returns the dividend data as a calendar for a given date range. To call custom period, use start_date and end_date parameters.

        :returns: request builder instance
        :rtype: DividendsCalendarRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return DividendsCalendarEndpoint(ctx, **ctx.defaults)

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

    def get_income_statement_consolidated(self, **defaults):
        """
        Creates request builder for Income Statement (Consolidated).

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IncomeStatementConsolidatedEndpoint(ctx, **ctx.defaults)

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

    def get_last_change(self, **defaults):
        """
        Creates request builder for Last Change.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return LastChangeEndpoint(ctx, **ctx.defaults)

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

    def get_market_cap(self, **defaults):
        """
        Creates request builder for Market Cap.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MarketCapEndpoint(ctx, **ctx.defaults)

    def get_press_releases(self, **defaults):
        """
        Creates request builder for Press Releases.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return PressReleasesEndpoint(ctx, **ctx.defaults)

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

    def get_splits_calendar(self, **defaults):
        """
        Creates request builder for Splits Calendar

        Returns split data as a calendar for a given date range. To call custom period, use start_date and end_date parameters.

        :returns: request builder instance
        :rtype: SplitsCalendarRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return SplitsCalendarEndpoint(ctx, **ctx.defaults)

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

    # Market Data

    def eod(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: EOD
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EODEndpoint(ctx, **ctx.defaults)

    def get_market_movers(self, **defaults):
        """
        Creates request builder for Market Movers.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MarketMoversEndpoint(ctx, **ctx.defaults)

    def price(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: Price
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return PriceEndpoint(ctx, **ctx.defaults)

    def quote(self, **defaults):
        """
        Creates factory for exchange rate requests.

        :returns: request factory instance
        :rtype: Quote
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return QuoteEndpoint(ctx, **ctx.defaults)

    def time_series(self, **defaults):
        """
        Creates factory for time series requests.

        :returns: request factory instance
        :rtype: TimeSeries
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TimeSeries(ctx)

    def time_series_cross(self, **defaults):
        """
        Creates request builder for Time Series Cross.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TimeSeriesCrossEndpoint(ctx, **ctx.defaults)

    # Mutual Funds

    def get_mutual_funds_family(self, **defaults):
        """
        Creates request builder for Mutual Funds Family.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsFamilyEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_list(self, **defaults):
        """
        Creates request builder for Mutual Funds List.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsListEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_type(self, **defaults):
        """
        Creates request builder for Mutual Funds Type.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsTypeEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world(self, **defaults):
        """
        Creates request builder for Mutual Funds World.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_composition(self, **defaults):
        """
        Creates request builder for Mutual Funds World Composition.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldCompositionEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_performance(self, **defaults):
        """
        Creates request builder for Mutual Funds World Performance.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldPerformanceEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_purchase_info(self, **defaults):
        """
        Creates request builder for Mutual Funds World Purchase Info.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldPurchaseInfoEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_ratings(self, **defaults):
        """
        Creates request builder for Mutual Funds World Ratings.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldRatingsEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_risk(self, **defaults):
        """
        Creates request builder for Mutual Funds World Risk.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldRiskEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_summary(self, **defaults):
        """
        Creates request builder for Mutual Funds World Summary.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldSummaryEndpoint(ctx, **ctx.defaults)

    def get_mutual_funds_world_sustainability(self, **defaults):
        """
        Creates request builder for Mutual Funds World Sustainability.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MutualFundsWorldSustainabilityEndpoint(ctx, **ctx.defaults)

    # Reference Data

    def get_bonds_list(self, **defaults):
        """
        Creates request builder for Bonds List

        This API call return array of bonds available at Twelve Data API. This list is daily updated.

        :returns: request builder instance
        :rtype: BondsListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return BondsListEndpoint(ctx, **ctx.defaults)

    def get_commodities_list(self, **defaults):
        """
        Creates request builder for Commodities List

        This API call return array of commodities available at Twelve Data API. This list is daily updated.

        :returns: request builder instance
        :rtype: CommoditiesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CommoditiesListEndpoint(ctx, **ctx.defaults)

    def get_countries(self, **defaults):
        """
        Creates request builder for Countries.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CountriesEndpoint(ctx, **ctx.defaults)

    def get_cross_listings(self, **defaults):
        """
        Creates request builder for Cross Listings.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return CrossListingsEndpoint(ctx, **ctx.defaults)

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

    def get_etf_list(self, **defaults):
        """
        Creates request builder for ETF List

        This API call return array of ETFs available at Twelve Data API. This list is daily updated.

        :returns: request builder instance
        :rtype: ETFListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ETFListEndpoint(ctx, **ctx.defaults)

    def get_exchange_schedule(self, **defaults):
        """
        Creates request builder for Exchange Schedule.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return ExchangeScheduleEndpoint(ctx, **ctx.defaults)

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

    def get_funds_list(self, **defaults):
        """
        Creates request builder for Funds List

        This API call return array of funds available at Twelve Data API. This list is daily updated.

        :returns: request builder instance
        :rtype: FundsListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return FundsListEndpoint(ctx, **ctx.defaults)

    def get_indices_list(self, **defaults):
        """
        Creates request builder for Indices List

        This API call return array of indices available at Twelve Data API. This list is daily updated.

        :returns: request builder instance
        :rtype: IndicesListRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IndicesListEndpoint(ctx, **ctx.defaults)

    def get_instrument_type(self, **defaults):
        """
        Creates request builder for Instrument Types.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return InstrumentTypeEndpoint(ctx, **ctx.defaults)

    def get_intervals(self, **defaults):
        """
        Creates request builder for Intervals.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return IntervalsEndpoint(ctx, **ctx.defaults)

    def get_market_state(self, **defaults):
        """
        Creates request builder for Market State

        Check the state of all available exchanges, time to open, and time to close. Returns all available stock exchanges by default.

        :returns: request builder instance
        :rtype: MarketStateRequestBuilder
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return MarketStateEndpoint(ctx, **ctx.defaults)

    def get_stock_exchanges_list(self):
        """
        Creates request builder for Stock Exchanges List

        This API call return array of stock exchanges available at twelvedata
        API. This list is daily updated.

        :returns: request builder instance
        :rtype: StockExchangesListRequestBuilder
        """
        return StockExchangesListEndpoint(ctx=self.ctx)

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

    # Regulatory

    def get_direct_holders(self, **defaults):
        """
        Creates request builder for Direct Holders.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return DirectHoldersEndpoint(ctx, **ctx.defaults)

    def get_edgar_filings_archive(self, **defaults):
        """
        Creates request builder for EDGAR Filings Archive.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return EdgarFilingsArchiveEndpoint(ctx, **ctx.defaults)

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

    def get_sanctions(self, **defaults):
        """
        Creates request builder for Sanctions.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return SanctionsEndpoint(ctx, **ctx.defaults)

    def get_tax_info(self, **defaults):
        """
        Creates request builder for Tax Info.

        :returns: request builder instance
        """
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return TaxInfoEndpoint(ctx, **ctx.defaults)

    # Options (deprecated)

    def get_options_expiration(self, **defaults):
        """
        Creates request builder for Options Expiration.

        .. deprecated::
            The Options Expiration endpoint is deprecated and will be
            removed in a future release.

        :returns: request builder instance
        :rtype: OptionsExpirationRequestBuilder
        """
        warnings.warn(
            "get_options_expiration() is deprecated and will be removed in a "
            "future release.",
            FutureWarning,
            stacklevel=2,
        )
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return OptionsExpirationEndpoint(ctx, **ctx.defaults)

    def get_options_chain(self, **defaults):
        """
        Creates request builder for Options Chain.

        .. deprecated::
            The Options Chain endpoint is deprecated and will be removed
            in a future release.

        :returns: request builder instance
        :rtype: OptionsChainRequestBuilder
        """
        warnings.warn(
            "get_options_chain() is deprecated and will be removed in a "
            "future release.",
            FutureWarning,
            stacklevel=2,
        )
        ctx = Context.from_context(self.ctx)
        ctx.defaults.update(defaults)
        return OptionsChainEndpoint(ctx, **ctx.defaults)
