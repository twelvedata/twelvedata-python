import itertools
from .mixins import AsMixin


__all__ = (
    # Advanced
    "APIUsageEndpoint",
    "TechIndicatorsMetaEndpoint",
    # Analysis
    "AnalystRatingsLightEndpoint",
    "AnalystRatingsUSEquitiesEndpoint",
    "EPSRevisionsEndpoint",
    "EPSTrendEndpoint",
    "EarningsEstimateEndpoint",
    "GrowthEstimatesEndpoint",
    "PriceTargetEndpoint",
    "RecommendationsEndpoint",
    "RevenueEstimateEndpoint",
    # Currencies
    "CurrencyConversionEndpoint",
    "ExchangeRateEndpoint",
    # ETFs
    "ETFsDetailedListEndpoint",
    "ETFsFamilyEndpoint",
    "ETFsTypeEndpoint",
    "ETFsWorldCompositionEndpoint",
    "ETFsWorldEndpoint",
    "ETFsWorldPerformanceEndpoint",
    "ETFsWorldRiskEndpoint",
    "ETFsWorldSummaryEndpoint",
    # Fundamentals
    "BalanceSheetConsolidatedEndpoint",
    "CashFlowConsolidatedEndpoint",
    "DividendsCalendarEndpoint",
    "EarningsCalendarEndpoint",
    "EarningsEndpoint",
    "IncomeStatementConsolidatedEndpoint",
    "LastChangeEndpoint",
    "MarketCapEndpoint",
    "PressReleasesEndpoint",
    "SplitsCalendarEndpoint",
    # Market Data
    "EODEndpoint",
    "MarketMoversEndpoint",
    "PriceEndpoint",
    "QuoteEndpoint",
    "TimeSeriesCrossEndpoint",
    "TimeSeriesEndpoint",
    # Mutual Funds
    "MutualFundsFamilyEndpoint",
    "MutualFundsListEndpoint",
    "MutualFundsTypeEndpoint",
    "MutualFundsWorldCompositionEndpoint",
    "MutualFundsWorldEndpoint",
    "MutualFundsWorldPerformanceEndpoint",
    "MutualFundsWorldPurchaseInfoEndpoint",
    "MutualFundsWorldRatingsEndpoint",
    "MutualFundsWorldRiskEndpoint",
    "MutualFundsWorldSummaryEndpoint",
    "MutualFundsWorldSustainabilityEndpoint",
    # Reference Data
    "BondsListEndpoint",
    "CommoditiesListEndpoint",
    "CountriesEndpoint",
    "CrossListingsEndpoint",
    "CryptocurrenciesListEndpoint",
    "CryptocurrencyExchangesListEndpoint",
    "ETFListEndpoint",
    "EarliestTimestampEndpoint",
    "ExchangeScheduleEndpoint",
    "ExchangesListEndpoint",
    "ForexPairsListEndpoint",
    "FundsListEndpoint",
    "IndicesListEndpoint",
    "InstrumentTypeEndpoint",
    "IntervalsEndpoint",
    "MarketStateEndpoint",
    "StockExchangesListEndpoint",
    "StocksListEndpoint",
    "SymbolSearchEndpoint",
    # Options (deprecated)
    "OptionsChainEndpoint",
    "OptionsExpirationEndpoint",
    # Regulatory
    "DirectHoldersEndpoint",
    "EdgarFilingsArchiveEndpoint",
    "SanctionsEndpoint",
    "TaxInfoEndpoint",
    # Technical Indicators
    "ADDEndpoint",
    "ADEndpoint",
    "ADOSCEndpoint",
    "ADXEndpoint",
    "ADXREndpoint",
    "APOEndpoint",
    "AROONEndpoint",
    "AROONOSCEndpoint",
    "ATREndpoint",
    "AVGEndpoint",
    "AVGPRICEEndpoint",
    "BBANDSEndpoint",
    "BETAEndpoint",
    "BOPEndpoint",
    "CCIEndpoint",
    "CEILEndpoint",
    "CMOEndpoint",
    "COPPOCKEndpoint",
    "CORRELEndpoint",
    "CRSIEndpoint",
    "DEMAEndpoint",
    "DIVEndpoint",
    "DPOEndpoint",
    "DXEndpoint",
    "EMAEndpoint",
    "EXPEndpoint",
    "FLOOREndpoint",
    "HEIKINASHICANDLESEndpoint",
    "HLC3Endpoint",
    "HT_DCPERIODEndpoint",
    "HT_DCPHASEEndpoint",
    "HT_PHASOREndpoint",
    "HT_SINEEndpoint",
    "HT_TRENDLINEEndpoint",
    "HT_TRENDMODEEndpoint",
    "ICHIMOKUEndpoint",
    "KAMAEndpoint",
    "KELTNEREndpoint",
    "KSTEndpoint",
    "LINEARREGANGLEEndpoint",
    "LINEARREGEndpoint",
    "LINEARREGINTERCEPTEndpoint",
    "LINEARREGSLOPEEndpoint",
    "LNEndpoint",
    "LOG10Endpoint",
    "MACDEXTEndpoint",
    "MACDEndpoint",
    "MACDSlopeEndpoint",
    "MAEndpoint",
    "MAMAEndpoint",
    "MAXEndpoint",
    "MAXINDEXEndpoint",
    "McGinleyDynamicEndpoint",
    "MEDPRICEEndpoint",
    "MFIEndpoint",
    "MIDPOINTEndpoint",
    "MIDPRICEEndpoint",
    "MINEndpoint",
    "MININDEXEndpoint",
    "MINMAXEndpoint",
    "MINMAXINDEXEndpoint",
    "MINUS_DIEndpoint",
    "MINUS_DMEndpoint",
    "MOMEndpoint",
    "MULTEndpoint",
    "NATREndpoint",
    "OBVEndpoint",
    "PLUS_DIEndpoint",
    "PLUS_DMEndpoint",
    "PPOEndpoint",
    "PercentBEndpoint",
    "PivotPointsHLEndpoint",
    "ROCEndpoint",
    "ROCPEndpoint",
    "ROCR100Endpoint",
    "ROCREndpoint",
    "RSIEndpoint",
    "RVOLEndpoint",
    "SAREXTEndpoint",
    "SAREndpoint",
    "SMAEndpoint",
    "SQRTEndpoint",
    "STDDEVEndpoint",
    "STOCHEndpoint",
    "STOCHFEndpoint",
    "STOCHRSIEndpoint",
    "SUBEndpoint",
    "SUMEndpoint",
    "SUPERTREND_HEIKINASHICANDLESEndpoint",
    "SuperTrendEndpoint",
    "T3MAEndpoint",
    "TEMAEndpoint",
    "TRANGEEndpoint",
    "TRIMAEndpoint",
    "TSFEndpoint",
    "TYPPRICEEndpoint",
    "ULTOSCEndpoint",
    "VAREndpoint",
    "VWAPEndpoint",
    "WCLPRICEEndpoint",
    "WILLREndpoint",
    "WMAEndpoint",
)


def purify_symbol(symbol):
    return "".join(symbol.split()).strip(',')


def get_symbol(symbol) -> (str, bool):
    if isinstance(symbol, str):
        purified_symbol = purify_symbol(symbol)
        if ',' in symbol and len(purified_symbol.split(',')) > 1:
            return purified_symbol, True
        return purified_symbol, False
    elif isinstance(symbol, list) or isinstance(symbol, tuple):
        if len(symbol) == 1:
            return symbol[0], False
        elif len(symbol) > 1:
            return ','.join(symbol), True
    else:
        raise TypeError('The type of argument "symbol" can be only: str, list, tuple')


def build_url(base, endpoint, params):
    query_params = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
    return '{}{}?{}'.format(base, endpoint, query_params)


class Endpoint(object):
    # This flag indicates that the current endpoint is a price chart
    is_price = False

    # This flag indicates that the current endpoint is a technical indicator
    is_indicator = False

    # This flag indicates that the chart should be drawn on the price chart
    is_overlay = False

    # This flag indicates that the current request is a batch request
    is_batch = False

    # Colors for chart
    colormap = {}

    # The fill between lines
    fill_area = {}

    def render_matplotlib(self, **kwargs):
        import matplotlib.dates as mdates
        from .renders import RENDERS_MAPPING, RenderContext

        df = kwargs.pop('df', None)
        if df is None:
            df = self.as_pandas()
        df = df.iloc[::-1]
        df.reset_index(level=0, inplace=True)
        df.set_index("datetime", inplace=True)

        ctx = RenderContext()
        ctx.colormap = self.colormap
        ctx.fill_area = self.fill_area
        ctx.interval_minutes = kwargs.pop("interval_minutes", 1)
        ctx.postfix = kwargs.pop("postfix", "")

        for render in RENDERS_MAPPING[self.__class__]:
            render.render_matplotlib(ctx, df, **kwargs)

    def render_plotly(self, **kwargs):
        from .renders import RENDERS_MAPPING, RenderContext

        ctx = RenderContext()
        ctx.colormap = self.colormap
        ctx.fill_area = self.fill_area
        ctx.fig = kwargs.pop("fig", None)
        ctx.interval_minutes = kwargs.pop("interval_minutes", 1)
        ctx.postfix = kwargs.pop("postfix", "")

        df = kwargs.pop('df', None)
        if df is None:
            df = self.as_pandas()
        return tuple(
            itertools.chain(
                *(
                    render.render_plotly(ctx, df, **kwargs)
                    for render in RENDERS_MAPPING[self.__class__]
                )
            )
        )


class CustomEndpoint(AsMixin, Endpoint):
    _name = "custom_endpoint"

    def __init__(
            self,
            ctx,
            name,
            **kwargs
    ):
        self.ctx = ctx
        self.name = name
        self.params = kwargs

    def execute(self, format="JSON", debug=False):
        self.params["format"] = format
        self.params["apikey"] = self.ctx.apikey
        endpoint = "/" + self.name

        if debug:
            return build_url(self.ctx.base_url, endpoint, self.params)
        return self.ctx.http_client.get(endpoint, params=self.params)


class TimeSeriesEndpoint(AsMixin, Endpoint):
    _name = "time_series"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        date=None,
        mic_code=None,
        previous_close=None,
        adjust=None,
        figi=None,
        isin=None,
        cusip=None,
    ):
        self.is_price = True
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.date = date
        self.mic_code = mic_code
        self.previous_close = previous_close
        self.adjust = adjust

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.date is not None:
            params["date"] = self.date
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        if self.adjust is not None:
            params["adjust"] = self.adjust

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/time_series"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ExchangeRateEndpoint(AsMixin, Endpoint):
    _name = "exchange_rate"

    def __init__(self,
                 ctx,
                 symbol,
                 date=None,
                 dp=None,
                 timezone=None
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.date = date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.date is not None:
            params["date"] = self.date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/exchange_rate"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CurrencyConversionEndpoint(AsMixin, Endpoint):
    _name = "currency_conversion"

    def __init__(self,
                 ctx,
                 symbol,
                 amount=None,
                 date=None,
                 dp=None,
                 timezone=None
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.amount = amount
        self.date = date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.amount is not None:
            params["amount"] = self.amount
        if self.date is not None:
            params["date"] = self.date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/currency_conversion"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class QuoteEndpoint(AsMixin, Endpoint):
    _name = "quote"

    def __init__(self,
                 ctx,
                 symbol,
                 interval="1day",
                 exchange=None,
                 country=None,
                 volume_time_period=None,
                 type=None,
                 dp=5,
                 timezone="Exchange",
                 prepost="false",
                 mic_code=None,
                 eod=None,
                 rolling_period=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.volume_time_period = volume_time_period
        self.type = type
        self.dp = dp
        self.timezone = timezone
        self.prepost = prepost
        self.mic_code = mic_code
        self.eod = eod
        self.rolling_period = rolling_period

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
            # Batch mode is not supported for this endpoint
            self.is_batch = False
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.volume_time_period is not None:
            params["volume_time_period"] = self.volume_time_period
        if self.type is not None:
            params["type"] = self.type
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.eod is not None:
            params["eod"] = self.eod
        if self.rolling_period is not None:
            params["rolling_period"] = self.rolling_period

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/quote"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PriceEndpoint(AsMixin, Endpoint):
    _name = "price"

    def __init__(self,
                 ctx,
                 symbol,
                 exchange=None,
                 country=None,
                 type=None,
                 dp=5,
                 prepost="false",
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.type = type
        self.dp = dp
        self.prepost = prepost
        self.mic_code = mic_code

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.dp is not None:
            params["dp"] = self.dp
        if self.prepost is not None:
            params["prepost"] = self.prepost

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/price"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EODEndpoint(AsMixin, Endpoint):
    _name = "eod"

    def __init__(self,
                 ctx,
                 symbol,
                 exchange=None,
                 country=None,
                 type=None,
                 dp=5,
                 prepost="false",
                 mic_code=None,
                 date=None,
                 figi=None,
                 isin=None,
                 cusip=None,
                 ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.type = type
        self.dp = dp
        self.prepost = prepost
        self.mic_code = mic_code
        self.date = date

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.dp is not None:
            params["dp"] = self.dp
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.date is not None:
            params["date"] = self.date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/eod"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TechIndicatorsMetaEndpoint(AsMixin, Endpoint):
    _name = "technical_indicators"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):
        params = {}
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/technical_indicators"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class StocksListEndpoint(AsMixin, Endpoint):
    _name = "stocks"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
                 mic_code=None,
                 show_plan=None,
                 include_delisted=None,
                 figi=None,
                 isin=None,
                 cusip=None,
                 cik=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.cik = cik
        self.exchange = exchange
        self.country = country
        self.type = type
        self.mic_code = mic_code
        self.show_plan = show_plan
        self.include_delisted = include_delisted

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.cik is not None:
            params["cik"] = self.cik
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan
        if self.include_delisted is not None:
            params["include_delisted"] = self.include_delisted

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stocks"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class StockExchangesListEndpoint(AsMixin, Endpoint):
    _name = "stock_exchanges"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):

        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stock_exchanges"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ForexPairsListEndpoint(AsMixin, Endpoint):
    _name = "forex_pairs"

    def __init__(self,
                 ctx,
                 symbol=None,
                 currency_base=None,
                 currency_quote=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.currency_base = currency_base
        self.currency_quote = currency_quote

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.currency_base is not None:
            params["currency_base"] = self.currency_base
        if self.currency_quote is not None:
            params["currency_quote"] = self.currency_quote

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/forex_pairs"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CryptocurrenciesListEndpoint(AsMixin, Endpoint):
    _name = "cryptocurrencies"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 currency_base=None,
                 currency_quote=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.currency_base = currency_base
        self.currency_quote = currency_quote

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.currency_base is not None:
            params["currency_base"] = self.currency_base
        if self.currency_quote is not None:
            params["currency_quote"] = self.currency_quote

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cryptocurrencies"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFListEndpoint(AsMixin, Endpoint):
    _name = "etfs"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 show_plan=None,
                 include_delisted=None,
                 figi=None,
                 isin=None,
                 cusip=None,
                 cik=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.show_plan = show_plan
        self.include_delisted = include_delisted
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.cik = cik

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan
        if self.include_delisted is not None:
            params["include_delisted"] = self.include_delisted
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.cik is not None:
            params["cik"] = self.cik

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class IndicesListEndpoint(AsMixin, Endpoint):
    _name = "indices"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 show_plan=None,
                 include_delisted=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.show_plan = show_plan
        self.include_delisted = include_delisted

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan
        if self.include_delisted is not None:
            params["include_delisted"] = self.include_delisted

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/indices"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class FundsListEndpoint(AsMixin, Endpoint):
    _name = "funds"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
                 show_plan=None,
                 include_delisted=None,
                 page=None,
                 outputsize=None,
                 figi=None,
                 isin=None,
                 cusip=None,
                 cik=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.cik = cik
        self.exchange = exchange
        self.country = country
        self.type = type
        self.show_plan = show_plan
        self.include_delisted = include_delisted
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.cik is not None:
            params["cik"] = self.cik
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan
        if self.include_delisted is not None:
            params["include_delisted"] = self.include_delisted
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/funds"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BondsListEndpoint(AsMixin, Endpoint):
    _name = "bonds"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
                 show_plan=None,
                 include_delisted=None,
                 page=None,
                 outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.show_plan = show_plan
        self.include_delisted = include_delisted
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan
        if self.include_delisted is not None:
            params["include_delisted"] = self.include_delisted
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/bonds"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)

class CommoditiesListEndpoint(AsMixin, Endpoint):
    _name = "commodities"

    def __init__(self,
                 ctx,
                 symbol=None,
                 category=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.category = category

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.category is not None:
            params["category"] = self.category

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/commodities"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ExchangesListEndpoint(AsMixin, Endpoint):
    _name = "exchanges"

    def __init__(self,
                 ctx,
                 name=None,
                 code=None,
                 country=None,
                 type=None,
                 show_plan=None,
    ):
        self.ctx = ctx
        self.name = name
        self.code = code
        self.country = country
        self.type = type
        self.show_plan = show_plan

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.name is not None:
            params["name"] = self.name
        if self.code is not None:
            params["code"] = self.code
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/exchanges"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CryptocurrencyExchangesListEndpoint(AsMixin, Endpoint):
    _name = "cryptocurrency_exchanges"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):

        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cryptocurrency_exchanges"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TechnicalIndicatorsListEndpoint(AsMixin, Endpoint):
    _name = "technical_indicators"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):

        params = {}

        params["apikey"] = self.ctx.apikey
        endpoint = "/technical_indicators"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SymbolSearchEndpoint(AsMixin, Endpoint):
    _name = "symbol_search"

    def __init__(self,
                 ctx,
                 symbol=None,
                 outputsize=None,
                 show_plan=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.outputsize = outputsize
        self.show_plan = show_plan

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.show_plan is not None:
            params["show_plan"] = self.show_plan

        params["format"] = "JSON"
        params["apikey"] = self.ctx.apikey
        endpoint = "/symbol_search"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EarliestTimestampEndpoint(AsMixin, Endpoint):
    _name = "earliest_timestamp"

    def __init__(self,
                 ctx,
                 symbol=None,
                 interval=None,
                 exchange=None,
                 mic_code=None,
                 timezone=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.mic_code = mic_code
        self.timezone = timezone

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.timezone is not None:
            params["timezone"] = self.timezone

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/earliest_timestamp"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MarketStateEndpoint(AsMixin, Endpoint):
    _name = "market_state"

    def __init__(self,
                 ctx,
                 exchange=None,
                 code=None,
                 country=None,
    ):
        self.ctx = ctx
        self.exchange = exchange
        self.code = code
        self.country = country

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.code is not None:
            params["code"] = self.code
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/market_state"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LogoEndpoint(AsMixin, Endpoint):
    _name = "logo"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "logo"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/logo"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ProfileEndpoint(AsMixin, Endpoint):
    _name = "profile"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "profile"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/profile"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DividendsEndpoint(AsMixin, Endpoint):
    _name = "dividends"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 range=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 adjust=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.range = range
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.adjust = adjust
        self.method = "dividends"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.range is not None:
            params["range"] = self.range
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.adjust is not None:
            params["adjust"] = self.adjust

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/dividends"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DividendsCalendarEndpoint(AsMixin, Endpoint):
    _name = "dividends_calendar"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 outputsize=None,
                 page=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.outputsize = outputsize
        self.page = page
        self.method = "dividends_calendar"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.page is not None:
            params["page"] = self.page

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/dividends_calendar"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SplitsEndpoint(AsMixin, Endpoint):
    _name = "splits"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 range=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.range = range
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.method = "splits"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.range is not None:
            params["range"] = self.range
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/splits"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SplitsCalendarEndpoint(AsMixin, Endpoint):
    _name = "splits_calendar"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 outputsize=None,
                 page=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.outputsize = outputsize
        self.page = page
        self.method = "splits_calendar"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.page is not None:
            params["page"] = self.page

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/splits_calendar"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EarningsEndpoint(AsMixin, Endpoint):
    _name = "earnings"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 period=None,
                 outputsize=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 dp=None,
                 type=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.dp = dp
        self.type = type
        self.method = "earnings"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.dp is not None:
            params["dp"] = self.dp
        if self.type is not None:
            params["type"] = self.type

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/earnings"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EarningsCalendarEndpoint(AsMixin, Endpoint):
    _name = "earnings_calendar"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 period=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.dp = dp
        self.method = "earnings_calendar"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/earnings_calendar"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class IPOCalendarEndpoint(AsMixin, Endpoint):
    _name = "ipo_calendar"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.method = "ipo_calendar"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ipo_calendar"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class StatisticsEndpoint(AsMixin, Endpoint):
    _name = "statistics"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "statistics"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/statistics"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class InsiderTransactionsEndpoint(AsMixin, Endpoint):
    _name = "insider_transactions"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "insider_transactions"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/insider_transactions"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class IncomeStatementEndpoint(AsMixin, Endpoint):
    _name = "income_statement"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 period=None,
                 outputsize=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.method = "income_statement"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/income_statement"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BalanceSheetEndpoint(AsMixin, Endpoint):
    _name = "balance_sheet"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 period=None,
                 outputsize=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.method = "balance_sheet"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/balance_sheet"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CashFlowEndpoint(AsMixin, Endpoint):
    _name = "cash_flow"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 period=None,
                 outputsize=None,
                 start_date=None,
                 end_date=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.mic_code = mic_code
        self.method = "cash_flow"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cash_flow"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class OptionsExpirationEndpoint(AsMixin, Endpoint):
    """Deprecated: the `/options/expiration` endpoint has been retired by the API."""

    _name = "options_expiration"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "options_expiration"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/options/expiration"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class OptionsChainEndpoint(AsMixin, Endpoint):
    """Deprecated: the `/options/chain` endpoint has been retired by the API."""

    _name = "options_chain"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 expiration_date=None,
                 option_id=None,
                 side=None,
                 mic_code=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.expiration_date = expiration_date
        self.option_id = option_id
        self.side = side
        self.mic_code = mic_code
        self.method = "options_chain"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.expiration_date is not None:
            params["expiration_date"] = self.expiration_date
        if self.option_id is not None:
            params["option_id"] = self.option_id
        if self.side is not None:
            params["side"] = self.side
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/options/chain"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class KeyExecutivesEndpoint(AsMixin, Endpoint):
    _name = "key_executives"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "key_executives"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/key_executives"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class InstitutionalHoldersEndpoint(AsMixin, Endpoint):
    _name = "institutional_holders"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "institutional_holders"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/institutional_holders"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class FundHoldersEndpoint(AsMixin, Endpoint):
    _name = "fund_holders"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 mic_code=None,
                 figi=None,
                 isin=None,
                 cusip=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.country = country
        self.mic_code = mic_code
        self.method = "fund_holders"

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/fund_holders"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class APIUsageEndpoint(AsMixin, Endpoint):
    _name = "api_usage"

    def __init__(self, ctx, timezone=None):
        self.ctx = ctx
        self.timezone = timezone

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.timezone is not None:
            params["timezone"] = self.timezone
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/api_usage"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ADEndpoint(AsMixin, Endpoint):
    _name = "ad"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ad"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ad"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ADOSCEndpoint(AsMixin, Endpoint):
    _name = "adosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        fast_period=12,
        slow_period=26,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "adosc"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/adosc"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ADXEndpoint(AsMixin, Endpoint):
    _name = "adx"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "adx"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/adx"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ADXREndpoint(AsMixin, Endpoint):
    _name = "adxr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "adxr"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/adxr"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class APOEndpoint(AsMixin, Endpoint):
    _name = "apo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        fast_period=12,
        slow_period=26,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "apo"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/apo"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AROONEndpoint(AsMixin, Endpoint):
    _name = "aroon"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "aroon"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/aroon"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AROONOSCEndpoint(AsMixin, Endpoint):
    _name = "aroonosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "aroonosc"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/aroonosc"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ATREndpoint(AsMixin, Endpoint):
    _name = "atr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "atr"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/atr"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AVGPRICEEndpoint(AsMixin, Endpoint):
    _name = "avgprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "avgprice"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/avgprice"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BBANDSEndpoint(AsMixin, Endpoint):
    _name = "bbands"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=20,
        sd="2",
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "bbands"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.sd is not None:
            params["sd"] = self.sd
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/bbands"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BETAEndpoint(AsMixin, Endpoint):
    _name = "beta"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "beta"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/beta"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PercentBEndpoint(AsMixin, Endpoint):
    _name = "percent_b"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=20,
        sd="2",
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "percent_b"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.sd is not None:
            params["sd"] = self.sd
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/percent_b"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PivotPointsHLEndpoint(AsMixin, Endpoint):
    _name = "pivot_points_hl"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=10,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "pivot_points_hl"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/pivot_points_hl"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BOPEndpoint(AsMixin, Endpoint):
    _name = "bop"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "bop"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/bop"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CCIEndpoint(AsMixin, Endpoint):
    _name = "cci"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=20,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "cci"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cci"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CMOEndpoint(AsMixin, Endpoint):
    _name = "cmo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "cmo"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cmo"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class COPPOCKEndpoint(AsMixin, Endpoint):
    _name = "coppock"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        long_roc_period=14,
        short_roc_period=11,
        wma_period=0,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "cmo"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.long_roc_period = long_roc_period
        self.short_roc_period = short_roc_period
        self.wma_period = wma_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.long_roc_period is not None:
            params["long_roc_period"] = self.long_roc_period
        if self.short_roc_period is not None:
            params["short_roc_period"] = self.short_roc_period
        if self.wma_period is not None:
            params["wma_period"] = self.wma_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/coppock"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CEILEndpoint(AsMixin, Endpoint):
    _name = "ceil"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ceil"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ceil"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DEMAEndpoint(AsMixin, Endpoint):
    _name = "dema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "dema"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/dema"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DXEndpoint(AsMixin, Endpoint):
    _name = "dx"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "dx"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/dx"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EMAEndpoint(AsMixin, Endpoint):
    _name = "ema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ema"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ema"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EXPEndpoint(AsMixin, Endpoint):
    _name = "exp"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "exp"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/exp"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class FLOOREndpoint(AsMixin, Endpoint):
    _name = "floor"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "floor"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/floor"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HEIKINASHICANDLESEndpoint(AsMixin, Endpoint):
    _name = "heikinashicandles"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
        figi=None,
        isin=None,
        cusip=None,
    ):
        self.is_price = True
        self.meta_name = "heikinashicandles"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/heikinashicandles"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HLC3Endpoint(AsMixin, Endpoint):
    _name = "hlc3"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
        figi=None,
        isin=None,
        cusip=None,
    ):
        self.is_price = True
        self.meta_name = "hlc3"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/hlc3"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_DCPERIODEndpoint(AsMixin, Endpoint):
    _name = "ht_dcperiod"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_dcperiod"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_dcperiod"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_DCPHASEEndpoint(AsMixin, Endpoint):
    _name = "ht_dcphase"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_dcphase"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_dcphase"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_PHASOREndpoint(AsMixin, Endpoint):
    _name = "ht_phasor"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_phasor"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_phasor"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_SINEEndpoint(AsMixin, Endpoint):
    _name = "ht_sine"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_sine"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_sine"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_TRENDLINEEndpoint(AsMixin, Endpoint):
    _name = "ht_trendline"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_trendline"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_trendline"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class HT_TRENDMODEEndpoint(AsMixin, Endpoint):
    _name = "ht_trendmode"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ht_trendmode"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ht_trendmode"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ICHIMOKUEndpoint(AsMixin, Endpoint):
    _name = "ichimoku"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        conversion_line_period=9,
        base_line_period=26,
        leading_span_b_period=52,
        lagging_span_period=26,
        include_ahead_span_period=True,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "vwap"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.conversion_line_period = conversion_line_period
        self.base_line_period = base_line_period
        self.leading_span_b_period = leading_span_b_period
        self.lagging_span_period = lagging_span_period
        self.include_ahead_span_period = include_ahead_span_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.conversion_line_period is not None:
            params["conversion_line_period"] = self.conversion_line_period
        if self.base_line_period is not None:
            params["base_line_period"] = self.base_line_period
        if self.leading_span_b_period is not None:
            params["leading_span_b_period"] = self.leading_span_b_period
        if self.lagging_span_period is not None:
            params["lagging_span_period"] = self.lagging_span_period
        if self.include_ahead_span_period is not None:
            params["include_ahead_span_period"] = self.include_ahead_span_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ichimoku"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class KAMAEndpoint(AsMixin, Endpoint):
    _name = "kama"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "kama"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/kama"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class KELTNEREndpoint(AsMixin, Endpoint):
    _name = "keltner"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=20,
        atr_time_period=10,
        multiplier=2,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "keltner"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.atr_time_period = atr_time_period
        self.multiplier = multiplier
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.atr_time_period is not None:
            params["atr_time_period"] = self.atr_time_period
        if self.multiplier is not None:
            params["multiplier"] = self.multiplier
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/keltner"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class KSTEndpoint(AsMixin, Endpoint):
    _name = "kst"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        roc_period_1=10,
        roc_period_2=15,
        roc_period_3=20,
        roc_period_4=30,
        signal_period=9,
        sma_period_1=10,
        sma_period_2=10,
        sma_period_3=10,
        sma_period_4=15,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "kst"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.roc_period_1 = roc_period_1
        self.roc_period_2 = roc_period_2
        self.roc_period_3 = roc_period_3
        self.roc_period_4 = roc_period_4
        self.signal_period = signal_period
        self.sma_period_1 = sma_period_1
        self.sma_period_2 = sma_period_2
        self.sma_period_3 = sma_period_3
        self.sma_period_4 = sma_period_4
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.roc_period_1 is not None:
            params["roc_period_1"] = self.roc_period_1
        if self.roc_period_2 is not None:
            params["roc_period_2"] = self.roc_period_2
        if self.roc_period_3 is not None:
            params["roc_period_3"] = self.roc_period_3
        if self.roc_period_4 is not None:
            params["roc_period_4"] = self.roc_period_4
        if self.signal_period is not None:
            params["signal_period"] = self.signal_period
        if self.sma_period_1 is not None:
            params["sma_period_1"] = self.sma_period_1
        if self.sma_period_2 is not None:
            params["sma_period_2"] = self.sma_period_2
        if self.sma_period_3 is not None:
            params["sma_period_3"] = self.sma_period_3
        if self.sma_period_4 is not None:
            params["sma_period_4"] = self.sma_period_4
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/kst"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LINEARREGEndpoint(AsMixin, Endpoint):
    _name = "linearreg"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "linearreg"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/linearreg"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LINEARREGANGLEEndpoint(AsMixin, Endpoint):
    _name = "linearregangle"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "linearregangle"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/linearregangle"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LINEARREGINTERCEPTEndpoint(AsMixin, Endpoint):
    _name = "linearregintercept"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "linearregintercept"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/linearregintercept"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LINEARREGSLOPEEndpoint(AsMixin, Endpoint):
    _name = "linearregslope"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "linearregslope"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/linearregslope"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LNEndpoint(AsMixin, Endpoint):
    _name = "ln"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ln"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ln"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LOG10Endpoint(AsMixin, Endpoint):
    _name = "log10"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "log10"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/log10"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MAEndpoint(AsMixin, Endpoint):
    _name = "ma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ma"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ma"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MACDEndpoint(AsMixin, Endpoint):
    _name = "macd"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        fast_period=12,
        slow_period=26,
        signal_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "macd"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.signal_period is not None:
            params["signal_period"] = self.signal_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/macd"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MACDSlopeEndpoint(AsMixin, Endpoint):
    _name = "macd_slope"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        fast_period=12,
        slow_period=26,
        signal_period=9,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "macd_slope"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.signal_period is not None:
            params["signal_period"] = self.signal_period
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/macd_slope"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MACDEXTEndpoint(AsMixin, Endpoint):
    _name = "macdext"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        fast_period=12,
        fast_ma_type="SMA",
        slow_period=26,
        slow_ma_type="SMA",
        signal_period=9,
        signal_ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "macdext"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.fast_period = fast_period
        self.fast_ma_type = fast_ma_type
        self.slow_period = slow_period
        self.slow_ma_type = slow_ma_type
        self.signal_period = signal_period
        self.signal_ma_type = signal_ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.fast_ma_type is not None:
            params["fast_ma_type"] = self.fast_ma_type
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.slow_ma_type is not None:
            params["slow_ma_type"] = self.slow_ma_type
        if self.signal_period is not None:
            params["signal_period"] = self.signal_period
        if self.signal_ma_type is not None:
            params["signal_ma_type"] = self.signal_ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/macdext"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MAMAEndpoint(AsMixin, Endpoint):
    _name = "mama"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        fast_limit="0.5",
        slow_limit="0.05",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "mama"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.fast_limit = fast_limit
        self.slow_limit = slow_limit
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.fast_limit is not None:
            params["fast_limit"] = self.fast_limit
        if self.slow_limit is not None:
            params["slow_limit"] = self.slow_limit
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mama"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MAXEndpoint(AsMixin, Endpoint):
    _name = "max"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "max"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/max"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MAXINDEXEndpoint(AsMixin, Endpoint):
    _name = "maxindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "maxindex"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/maxindex"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class McGinleyDynamicEndpoint(AsMixin, Endpoint):
    _name = "mcginley_dynamic"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "mcginley_dynamic"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mcginley_dynamic"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MEDPRICEEndpoint(AsMixin, Endpoint):
    _name = "medprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "medprice"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/medprice"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MFIEndpoint(AsMixin, Endpoint):
    _name = "mfi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "mfi"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mfi"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MIDPOINTEndpoint(AsMixin, Endpoint):
    _name = "midpoint"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "midpoint"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/midpoint"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MIDPRICEEndpoint(AsMixin, Endpoint):
    _name = "midprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "midprice"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/midprice"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MINEndpoint(AsMixin, Endpoint):
    _name = "min"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "min"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/min"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MININDEXEndpoint(AsMixin, Endpoint):
    _name = "minindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "minindex"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/minindex"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MINMAXEndpoint(AsMixin, Endpoint):
    _name = "minmax"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "minmax"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/minmax"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MINMAXINDEXEndpoint(AsMixin, Endpoint):
    _name = "minmaxindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "minmaxindex"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/minmaxindex"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MINUS_DIEndpoint(AsMixin, Endpoint):
    _name = "minus_di"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "minus_di"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/minus_di"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MINUS_DMEndpoint(AsMixin, Endpoint):
    _name = "minus_dm"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "minus_dm"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/minus_dm"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MOMEndpoint(AsMixin, Endpoint):
    _name = "mom"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "mom"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mom"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class NATREndpoint(AsMixin, Endpoint):
    _name = "natr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "natr"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/natr"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class OBVEndpoint(AsMixin, Endpoint):
    _name = "obv"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "obv"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/obv"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PLUS_DIEndpoint(AsMixin, Endpoint):
    _name = "plus_di"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "plus_di"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/plus_di"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PLUS_DMEndpoint(AsMixin, Endpoint):
    _name = "plus_dm"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "plus_dm"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/plus_dm"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PPOEndpoint(AsMixin, Endpoint):
    _name = "ppo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        fast_period=10,
        slow_period=21,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ppo"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.fast_period is not None:
            params["fast_period"] = self.fast_period
        if self.slow_period is not None:
            params["slow_period"] = self.slow_period
        if self.ma_type is not None:
            params["ma_type"] = self.ma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ppo"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ROCEndpoint(AsMixin, Endpoint):
    _name = "roc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "roc"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/roc"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ROCPEndpoint(AsMixin, Endpoint):
    _name = "rocp"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "rocp"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/rocp"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ROCREndpoint(AsMixin, Endpoint):
    _name = "rocr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "rocr"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/rocr"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ROCR100Endpoint(AsMixin, Endpoint):
    _name = "rocr100"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "rocr100"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/rocr100"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class RSIEndpoint(AsMixin, Endpoint):
    _name = "rsi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "rsi"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/rsi"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class RVOLEndpoint(AsMixin, Endpoint):
    _name = "rvol"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "rvol"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/rvol"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SAREndpoint(AsMixin, Endpoint):
    _name = "sar"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        acceleration="0.02",
        maximum="0.2",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sar"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.acceleration = acceleration
        self.maximum = maximum
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.acceleration is not None:
            params["acceleration"] = self.acceleration
        if self.maximum is not None:
            params["maximum"] = self.maximum
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sar"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SMAEndpoint(AsMixin, Endpoint):
    _name = "sma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sma"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sma"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SQRTEndpoint(AsMixin, Endpoint):
    _name = "sqrt"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sqrt"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sqrt"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class STDDEVEndpoint(AsMixin, Endpoint):
    _name = "stddev"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        sd="2",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "stddev"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.sd is not None:
            params["sd"] = self.sd
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stddev"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class STOCHEndpoint(AsMixin, Endpoint):
    _name = "stoch"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        fast_k_period=14,
        slow_k_period=1,
        slow_d_period=3,
        slow_kma_type="SMA",
        slow_dma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "stoch"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.fast_k_period = fast_k_period
        self.slow_k_period = slow_k_period
        self.slow_d_period = slow_d_period
        self.slow_kma_type = slow_kma_type
        self.slow_dma_type = slow_dma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.fast_k_period is not None:
            params["fast_k_period"] = self.fast_k_period
        if self.slow_k_period is not None:
            params["slow_k_period"] = self.slow_k_period
        if self.slow_d_period is not None:
            params["slow_d_period"] = self.slow_d_period
        if self.slow_kma_type is not None:
            params["slow_kma_type"] = self.slow_kma_type
        if self.slow_dma_type is not None:
            params["slow_dma_type"] = self.slow_dma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stoch"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class STOCHFEndpoint(AsMixin, Endpoint):
    _name = "stochf"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        fast_k_period=14,
        fast_d_period=3,
        fast_dma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "stochf"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.fast_k_period = fast_k_period
        self.fast_d_period = fast_d_period
        self.fast_dma_type = fast_dma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.fast_k_period is not None:
            params["fast_k_period"] = self.fast_k_period
        if self.fast_d_period is not None:
            params["fast_d_period"] = self.fast_d_period
        if self.fast_dma_type is not None:
            params["fast_dma_type"] = self.fast_dma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stochf"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class STOCHRSIEndpoint(AsMixin, Endpoint):
    _name = "stochrsi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=14,
        fast_k_period=3,
        fast_d_period=3,
        fast_dma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
    ):
        self.is_indicator = True
        self.meta_name = "stochrsi"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.fast_k_period = fast_k_period
        self.fast_d_period = fast_d_period
        self.fast_dma_type = fast_dma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.fast_k_period is not None:
            params["fast_k_period"] = self.fast_k_period
        if self.fast_d_period is not None:
            params["fast_d_period"] = self.fast_d_period
        if self.fast_dma_type is not None:
            params["fast_dma_type"] = self.fast_dma_type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/stochrsi"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SuperTrendEndpoint(AsMixin, Endpoint):
    _name = "supertrend"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        multiplier=3,
        period=10,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "supertrend"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.multiplier = multiplier
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.multiplier is not None:
            params["multiplier"] = self.multiplier
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/supertrend"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class T3MAEndpoint(AsMixin, Endpoint):
    _name = "t3ma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        v_factor="0.7",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "t3ma"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.v_factor = v_factor
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.v_factor is not None:
            params["v_factor"] = self.v_factor
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/t3ma"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TEMAEndpoint(AsMixin, Endpoint):
    _name = "tema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "tema"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/tema"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TRANGEEndpoint(AsMixin, Endpoint):
    _name = "trange"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "trange"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/trange"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TRIMAEndpoint(AsMixin, Endpoint):
    _name = "trima"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "trima"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/trima"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TSFEndpoint(AsMixin, Endpoint):
    _name = "tsf"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "tsf"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/tsf"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TYPPRICEEndpoint(AsMixin, Endpoint):
    _name = "typprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "typprice"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/typprice"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ULTOSCEndpoint(AsMixin, Endpoint):
    _name = "ultosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period_1=7,
        time_period_2=14,
        time_period_3=28,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "ultosc"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period_1 = time_period_1
        self.time_period_2 = time_period_2
        self.time_period_3 = time_period_3
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period_1 is not None:
            params["time_period_1"] = self.time_period_1
        if self.time_period_2 is not None:
            params["time_period_2"] = self.time_period_2
        if self.time_period_3 is not None:
            params["time_period_3"] = self.time_period_3
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/ultosc"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class VAREndpoint(AsMixin, Endpoint):
    _name = "var"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "var"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/var"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class VWAPEndpoint(AsMixin, Endpoint):
    _name = "vwap"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        sd=None,
        sd_time_period=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "vwap"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.sd = sd
        self.sd_time_period = sd_time_period
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.sd is not None:
            params["sd"] = self.sd
        if self.sd_time_period is not None:
            params["sd_time_period"] = self.sd_time_period

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/vwap"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class WCLPRICEEndpoint(AsMixin, Endpoint):
    _name = "wclprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "wclprice"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/wclprice"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class WILLREndpoint(AsMixin, Endpoint):
    _name = "willr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "willr"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/willr"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class WMAEndpoint(AsMixin, Endpoint):
    _name = "wma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "wma"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/wma"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ExchangeScheduleEndpoint(AsMixin, Endpoint):
    _name = "exchange_schedule"

    def __init__(
        self,
        ctx,
        mic_name=None,
        mic_code=None,
        country=None,
        date=None,
    ):
        self.ctx = ctx
        self.mic_name = mic_name
        self.mic_code = mic_code
        self.country = country
        self.date = date

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.mic_name is not None:
            params["mic_name"] = self.mic_name
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.date is not None:
            params["date"] = self.date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/exchange_schedule"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CountriesEndpoint(AsMixin, Endpoint):
    _name = "countries"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):
        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/countries"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CrossListingsEndpoint(AsMixin, Endpoint):
    _name = "cross_listings"

    def __init__(
        self,
        ctx,
        symbol,
        exchange=None,
        mic_code=None,
        country=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cross_listings"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class IntervalsEndpoint(AsMixin, Endpoint):
    _name = "intervals"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):
        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/intervals"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class InstrumentTypeEndpoint(AsMixin, Endpoint):
    _name = "instrument_type"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON", debug=False):
        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/instrument_type"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TimeSeriesCrossEndpoint(AsMixin, Endpoint):
    _name = "time_series_cross"

    def __init__(
        self,
        ctx,
        base,
        quote,
        interval,
        base_type=None,
        base_exchange=None,
        base_mic_code=None,
        quote_type=None,
        quote_exchange=None,
        quote_mic_code=None,
        outputsize=None,
        delimiter=None,
        prepost=None,
        start_date=None,
        end_date=None,
        adjust=None,
        dp=None,
        timezone=None,
    ):
        self.ctx = ctx
        self.base = base
        self.quote = quote
        self.interval = interval
        self.base_type = base_type
        self.base_exchange = base_exchange
        self.base_mic_code = base_mic_code
        self.quote_type = quote_type
        self.quote_exchange = quote_exchange
        self.quote_mic_code = quote_mic_code
        self.outputsize = outputsize
        self.delimiter = delimiter
        self.prepost = prepost
        self.start_date = start_date
        self.end_date = end_date
        self.adjust = adjust
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.base is not None:
            params["base"] = self.base
        if self.quote is not None:
            params["quote"] = self.quote
        if self.interval is not None:
            params["interval"] = self.interval
        if self.base_type is not None:
            params["base_type"] = self.base_type
        if self.base_exchange is not None:
            params["base_exchange"] = self.base_exchange
        if self.base_mic_code is not None:
            params["base_mic_code"] = self.base_mic_code
        if self.quote_type is not None:
            params["quote_type"] = self.quote_type
        if self.quote_exchange is not None:
            params["quote_exchange"] = self.quote_exchange
        if self.quote_mic_code is not None:
            params["quote_mic_code"] = self.quote_mic_code
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.delimiter is not None:
            params["delimiter"] = self.delimiter
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/time_series/cross"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MarketMoversEndpoint(AsMixin, Endpoint):
    _name = "market_movers_market"

    def __init__(
        self,
        ctx,
        market,
        direction=None,
        outputsize=None,
        country=None,
        price_greater_than=None,
        dp=None,
    ):
        self.ctx = ctx
        self.market = market
        self.direction = direction
        self.outputsize = outputsize
        self.country = country
        self.price_greater_than = price_greater_than
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.direction is not None:
            params["direction"] = self.direction
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.country is not None:
            params["country"] = self.country
        if self.price_greater_than is not None:
            params["price_greater_than"] = self.price_greater_than
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/market_movers/{}".format(self.market)

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class IncomeStatementConsolidatedEndpoint(AsMixin, Endpoint):
    _name = "income_statement_consolidated"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
        period=None,
        start_date=None,
        end_date=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/income_statement/consolidated"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class BalanceSheetConsolidatedEndpoint(AsMixin, Endpoint):
    _name = "balance_sheet_consolidated"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
        period=None,
        start_date=None,
        end_date=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/balance_sheet/consolidated"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CashFlowConsolidatedEndpoint(AsMixin, Endpoint):
    _name = "cash_flow_consolidated"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
        period=None,
        start_date=None,
        end_date=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/cash_flow/consolidated"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MarketCapEndpoint(AsMixin, Endpoint):
    _name = "market_cap"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
        start_date=None,
        end_date=None,
        page=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/market_cap"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PressReleasesEndpoint(AsMixin, Endpoint):
    _name = "press_releases"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        start_date=None,
        end_date=None,
        timezone=None,
        language=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        self.language = language
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.language is not None:
            params["language"] = self.language
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/press_releases"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class LastChangeEndpoint(AsMixin, Endpoint):
    _name = "last_change_endpoint"

    def __init__(
        self,
        ctx,
        endpoint,
        start_date=None,
        symbol=None,
        exchange=None,
        mic_code=None,
        country=None,
        page=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.endpoint = endpoint
        self.start_date = start_date
        self.symbol = symbol
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/last_change/{}".format(self.endpoint)

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AnalystRatingsLightEndpoint(AsMixin, Endpoint):
    _name = "analyst_ratings_light"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        rating_change=None,
        outputsize=None,
        country=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.rating_change = rating_change
        self.outputsize = outputsize
        self.country = country

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.rating_change is not None:
            params["rating_change"] = self.rating_change
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/analyst_ratings/light"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AnalystRatingsUSEquitiesEndpoint(AsMixin, Endpoint):
    _name = "analyst_ratings_us_equities"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        rating_change=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.rating_change = rating_change
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.rating_change is not None:
            params["rating_change"] = self.rating_change
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/analyst_ratings/us_equities"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EarningsEstimateEndpoint(AsMixin, Endpoint):
    _name = "earnings_estimate"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/earnings_estimate"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class RevenueEstimateEndpoint(AsMixin, Endpoint):
    _name = "revenue_estimate"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/revenue_estimate"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EPSTrendEndpoint(AsMixin, Endpoint):
    _name = "eps_trend"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/eps_trend"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EPSRevisionsEndpoint(AsMixin, Endpoint):
    _name = "eps_revisions"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/eps_revisions"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class GrowthEstimatesEndpoint(AsMixin, Endpoint):
    _name = "growth_estimates"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/growth_estimates"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class PriceTargetEndpoint(AsMixin, Endpoint):
    _name = "price_target"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/price_target"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class RecommendationsEndpoint(AsMixin, Endpoint):
    _name = "recommendations"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.exchange = exchange

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/recommendations"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DirectHoldersEndpoint(AsMixin, Endpoint):
    _name = "direct_holders"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/direct_holders"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class EdgarFilingsArchiveEndpoint(AsMixin, Endpoint):
    _name = "edgar_filings_archive"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        exchange=None,
        mic_code=None,
        country=None,
        form_type=None,
        filled_from=None,
        filled_to=None,
        page=None,
        page_size=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code
        self.country = country
        self.form_type = form_type
        self.filled_from = filled_from
        self.filled_to = filled_to
        self.page = page
        self.page_size = page_size

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code
        if self.country is not None:
            params["country"] = self.country
        if self.form_type is not None:
            params["form_type"] = self.form_type
        if self.filled_from is not None:
            params["filled_from"] = self.filled_from
        if self.filled_to is not None:
            params["filled_to"] = self.filled_to
        if self.page is not None:
            params["page"] = self.page
        if self.page_size is not None:
            params["page_size"] = self.page_size

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/edgar_filings/archive"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SanctionsEndpoint(AsMixin, Endpoint):
    _name = "sanctions_source"

    def __init__(
        self,
        ctx,
        source,
    ):
        self.ctx = ctx
        self.source = source

    def execute(self, format="JSON", debug=False):
        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sanctions/{}".format(self.source)

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class TaxInfoEndpoint(AsMixin, Endpoint):
    _name = "tax_info"

    def __init__(
        self,
        ctx,
        symbol=None,
        isin=None,
        figi=None,
        cusip=None,
        exchange=None,
        mic_code=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.isin = isin
        self.figi = figi
        self.cusip = cusip
        self.exchange = exchange
        self.mic_code = mic_code

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.isin is not None:
            params["isin"] = self.isin
        if self.figi is not None:
            params["figi"] = self.figi
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/tax_info"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsDetailedListEndpoint(AsMixin, Endpoint):
    _name = "etfs_list"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        cik=None,
        country=None,
        fund_family=None,
        fund_type=None,
        page=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.cik = cik
        self.country = country
        self.fund_family = fund_family
        self.fund_type = fund_type
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.cik is not None:
            params["cik"] = self.cik
        if self.country is not None:
            params["country"] = self.country
        if self.fund_family is not None:
            params["fund_family"] = self.fund_family
        if self.fund_type is not None:
            params["fund_type"] = self.fund_type
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/list"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsTypeEndpoint(AsMixin, Endpoint):
    _name = "etfs_type"

    def __init__(
        self,
        ctx,
        country=None,
        fund_type=None,
    ):
        self.ctx = ctx
        self.country = country
        self.fund_type = fund_type

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.country is not None:
            params["country"] = self.country
        if self.fund_type is not None:
            params["fund_type"] = self.fund_type

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/type"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsFamilyEndpoint(AsMixin, Endpoint):
    _name = "etfs_family"

    def __init__(
        self,
        ctx,
        country=None,
        fund_family=None,
    ):
        self.ctx = ctx
        self.country = country
        self.fund_family = fund_family

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.country is not None:
            params["country"] = self.country
        if self.fund_family is not None:
            params["fund_family"] = self.fund_family

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/family"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsWorldEndpoint(AsMixin, Endpoint):
    _name = "etfs_world"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/world"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsWorldSummaryEndpoint(AsMixin, Endpoint):
    _name = "etfs_world_summary"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/world/summary"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsWorldCompositionEndpoint(AsMixin, Endpoint):
    _name = "etfs_world_composition"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/world/composition"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsWorldPerformanceEndpoint(AsMixin, Endpoint):
    _name = "etfs_world_performance"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/world/performance"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class ETFsWorldRiskEndpoint(AsMixin, Endpoint):
    _name = "etfs_world_risk"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/etfs/world/risk"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsListEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_list"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        cik=None,
        country=None,
        fund_family=None,
        fund_type=None,
        performance_rating=None,
        risk_rating=None,
        page=None,
        outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.cik = cik
        self.country = country
        self.fund_family = fund_family
        self.fund_type = fund_type
        self.performance_rating = performance_rating
        self.risk_rating = risk_rating
        self.page = page
        self.outputsize = outputsize

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.cik is not None:
            params["cik"] = self.cik
        if self.country is not None:
            params["country"] = self.country
        if self.fund_family is not None:
            params["fund_family"] = self.fund_family
        if self.fund_type is not None:
            params["fund_type"] = self.fund_type
        if self.performance_rating is not None:
            params["performance_rating"] = self.performance_rating
        if self.risk_rating is not None:
            params["risk_rating"] = self.risk_rating
        if self.page is not None:
            params["page"] = self.page
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/list"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsTypeEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_type"

    def __init__(
        self,
        ctx,
        fund_type=None,
        country=None,
    ):
        self.ctx = ctx
        self.fund_type = fund_type
        self.country = country

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.fund_type is not None:
            params["fund_type"] = self.fund_type
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/type"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsFamilyEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_family"

    def __init__(
        self,
        ctx,
        fund_family=None,
        country=None,
    ):
        self.ctx = ctx
        self.fund_family = fund_family
        self.country = country

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.fund_family is not None:
            params["fund_family"] = self.fund_family
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/family"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldSummaryEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_summary"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/summary"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldCompositionEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_composition"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/composition"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldPurchaseInfoEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_purchase_info"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/purchase_info"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldPerformanceEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_performance"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/performance"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldRiskEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_risk"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/risk"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldRatingsEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_ratings"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/ratings"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MutualFundsWorldSustainabilityEndpoint(AsMixin, Endpoint):
    _name = "mutual_funds_world_sustainability"

    def __init__(
        self,
        ctx,
        symbol=None,
        figi=None,
        isin=None,
        cusip=None,
        country=None,
        dp=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.country = country
        self.dp = dp

    def execute(self, format="JSON", debug=False):
        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.country is not None:
            params["country"] = self.country
        if self.dp is not None:
            params["dp"] = self.dp

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mutual_funds/world/sustainability"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)



class ADDEndpoint(AsMixin, Endpoint):
    _name = "add"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "add"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/add"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SUBEndpoint(AsMixin, Endpoint):
    _name = "sub"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sub"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sub"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class MULTEndpoint(AsMixin, Endpoint):
    _name = "mult"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "mult"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/mult"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DIVEndpoint(AsMixin, Endpoint):
    _name = "div"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "div"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/div"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SUMEndpoint(AsMixin, Endpoint):
    _name = "sum"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sum"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sum"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class AVGEndpoint(AsMixin, Endpoint):
    _name = "avg"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "avg"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/avg"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CRSIEndpoint(AsMixin, Endpoint):
    _name = "crsi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        rsi_period=3,
        up_down_length=2,
        percent_rank_period=100,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "crsi"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.rsi_period = rsi_period
        self.up_down_length = up_down_length
        self.percent_rank_period = percent_rank_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.rsi_period is not None:
            params["rsi_period"] = self.rsi_period
        if self.up_down_length is not None:
            params["up_down_length"] = self.up_down_length
        if self.percent_rank_period is not None:
            params["percent_rank_period"] = self.percent_rank_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/crsi"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class CORRELEndpoint(AsMixin, Endpoint):
    _name = "correl"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type_1="open",
        series_type_2="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "correl"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type_1 = series_type_1
        self.series_type_2 = series_type_2
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type_1 is not None:
            params["series_type_1"] = self.series_type_1
        if self.series_type_2 is not None:
            params["series_type_2"] = self.series_type_2
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/correl"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class DPOEndpoint(AsMixin, Endpoint):
    _name = "dpo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        series_type="close",
        time_period=9,
        centered="false",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "dpo"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.series_type = series_type
        self.time_period = time_period
        self.centered = centered
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.series_type is not None:
            params["series_type"] = self.series_type
        if self.time_period is not None:
            params["time_period"] = self.time_period
        if self.centered is not None:
            params["centered"] = self.centered
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/dpo"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SAREXTEndpoint(AsMixin, Endpoint):
    _name = "sarext"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        start_value=0,
        offset_on_reverse=0,
        acceleration_limit_long=0.02,
        acceleration_long=0.02,
        acceleration_max_long=0.2,
        acceleration_limit_short=0.02,
        acceleration_short=0.02,
        acceleration_max_short=0.2,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "sarext"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.start_value = start_value
        self.offset_on_reverse = offset_on_reverse
        self.acceleration_limit_long = acceleration_limit_long
        self.acceleration_long = acceleration_long
        self.acceleration_max_long = acceleration_max_long
        self.acceleration_limit_short = acceleration_limit_short
        self.acceleration_short = acceleration_short
        self.acceleration_max_short = acceleration_max_short
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.start_value is not None:
            params["start_value"] = self.start_value
        if self.offset_on_reverse is not None:
            params["offset_on_reverse"] = self.offset_on_reverse
        if self.acceleration_limit_long is not None:
            params["acceleration_limit_long"] = self.acceleration_limit_long
        if self.acceleration_long is not None:
            params["acceleration_long"] = self.acceleration_long
        if self.acceleration_max_long is not None:
            params["acceleration_max_long"] = self.acceleration_max_long
        if self.acceleration_limit_short is not None:
            params["acceleration_limit_short"] = self.acceleration_limit_short
        if self.acceleration_short is not None:
            params["acceleration_short"] = self.acceleration_short
        if self.acceleration_max_short is not None:
            params["acceleration_max_short"] = self.acceleration_max_short
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/sarext"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)


class SUPERTREND_HEIKINASHICANDLESEndpoint(AsMixin, Endpoint):
    _name = "supertrend_heikinashicandles"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        type=None,
        period=10,
        multiplier=3,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
        order="desc",
        prepost="false",
        mic_code=None,
        figi=None,
        isin=None,
        cusip=None,
        adjust=None,
        date=None,
        include_ohlc=None,
        previous_close=None,
    ):
        self.is_indicator = True
        self.meta_name = "supertrend_heikinashicandles"
        self.ctx = ctx
        self.symbol = symbol
        self.figi = figi
        self.isin = isin
        self.cusip = cusip
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.type = type
        self.period = period
        self.multiplier = multiplier
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone
        self.order = order
        self.prepost = prepost
        self.mic_code = mic_code
        self.adjust = adjust
        self.date = date
        self.include_ohlc = include_ohlc
        self.previous_close = previous_close

    def execute(self, format="JSON", debug=False):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.figi is not None:
            params["figi"] = self.figi
        if self.isin is not None:
            params["isin"] = self.isin
        if self.cusip is not None:
            params["cusip"] = self.cusip
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.period is not None:
            params["period"] = self.period
        if self.multiplier is not None:
            params["multiplier"] = self.multiplier
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date
        if self.dp is not None:
            params["dp"] = self.dp
        if self.timezone is not None:
            params["timezone"] = self.timezone
        if self.order is not None:
            params["order"] = self.order
        if self.prepost is not None:
            params["prepost"] = self.prepost
        if self.mic_code is not None:
            params["mic_code"] = self.mic_code

        if self.adjust is not None:
            params["adjust"] = self.adjust
        if self.date is not None:
            params["date"] = self.date
        if self.include_ohlc is not None:
            params["include_ohlc"] = self.include_ohlc
        if self.previous_close is not None:
            params["previous_close"] = self.previous_close
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        endpoint = "/supertrend_heikinashicandles"

        if debug:
            return build_url(self.ctx.base_url, endpoint, params)
        return self.ctx.http_client.get(endpoint, params=params)
