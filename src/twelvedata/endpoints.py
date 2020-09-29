import itertools
from .mixins import AsMixin


__all__ = (
    "ADOSCEndpoint",
    "ADEndpoint",
    "ADXREndpoint",
    "ADXEndpoint",
    "APOEndpoint",
    "AROONOSCEndpoint",
    "AROONEndpoint",
    "ATREndpoint",
    "AVGPRICEEndpoint",
    "BBANDSEndpoint",
    "BOPEndpoint",
    "CCIEndpoint",
    "CEILEndpoint",
    "CMOEndpoint",
    "COPPOCKEndpoint",
    "CryptocurrenciesListEndpoint",
    "CryptocurrencyExchangesListEndpoint",
    "DEMAEndpoint",
    "DXEndpoint",
    "EarliestTimestampEndpoint",
    "EarningsCalendarEndpoint",
    "EarningsEndpoint",
    "EMAEndpoint",
    "ETFListEndpoint",
    "ExchangesListEndpoint",
    "EXPEndpoint",
    "FLOOREndpoint",
    "ForexPairsListEndpoint",
    "HEIKINASHICANDLESEndpoint",
    "HLC3Endpoint",
    "HT_DCPERIODEndpoint",
    "HT_DCPHASEEndpoint",
    "HT_PHASOREndpoint",
    "HT_SINEEndpoint",
    "HT_TRENDLINEEndpoint",
    "HT_TRENDMODEEndpoint",
    "ICHIMOKUEndpoint",
    "IndicesListEndpoint",
    "KAMAEndpoint",
    "KELTNEREndpoint",
    "KSTEndpoint",
    "LINEARREGANGLEEndpoint",
    "LINEARREGINTERCEPTEndpoint",
    "LINEARREGEndpoint",
    "LINEARREGSLOPEEndpoint",
    "LNEndpoint",
    "LOG10Endpoint",
    "MACDEXTEndpoint",
    "MACDEndpoint",
    "MAMAEndpoint",
    "MAEndpoint",
    "MAXINDEXEndpoint",
    "MAXEndpoint",
    "McGinleyDynamicEndpoint",
    "MEDPRICEEndpoint",
    "MIDPOINTEndpoint",
    "MIDPRICEEndpoint",
    "MININDEXEndpoint",
    "MINMAXINDEXEndpoint",
    "MINMAXEndpoint",
    "MINEndpoint",
    "MINUS_DIEndpoint",
    "MINUS_DMEndpoint",
    "MOMEndpoint",
    "NATREndpoint",
    "OBVEndpoint",
    "PLUS_DIEndpoint",
    "PLUS_DMEndpoint",
    "PPOEndpoint",
    "PercentBEndpoint",
    "ROCPEndpoint",
    "ROCR100Endpoint",
    "ROCREndpoint",
    "ROCEndpoint",
    "RSIEndpoint",
    "SAREndpoint",
    "SMAEndpoint",
    "SQRTEndpoint",
    "STDDEVEndpoint",
    "STOCHFEndpoint",
    "STOCHRSIEndpoint",
    "STOCHEndpoint",
    "SymbolSearchEndpoint",
    "StockExchangesListEndpoint",
    "StocksListEndpoint",
    "SuperTrendEndpoint",
    "T3MAEndpoint",
    "TEMAEndpoint",
    "TRANGEEndpoint",
    "TRIMAEndpoint",
    "TSFEndpoint",
    "TYPPRICEEndpoint",
    "TechIndicatorsMetaEndpoint",
    "TimeSeriesEndpoint",
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
    elif isinstance(symbol, list):
        if len(symbol) == 1:
            return symbol, False
        elif len(symbol) > 1:
            return ','.join(symbol), True


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

        df = self.as_pandas()
        return tuple(
            itertools.chain(
                *(
                    render.render_plotly(ctx, df, **kwargs)
                    for render in RENDERS_MAPPING[self.__class__]
                )
            )
        )


class TimeSeriesEndpoint(AsMixin, Endpoint):
    _name = "time_series"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_price = True
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/time_series", params=params)


class TechIndicatorsMetaEndpoint(AsMixin, Endpoint):
    _name = "technical_indicators"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):
        params = {}
        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/technical_indicators", params=params)


class StocksListEndpoint(AsMixin, Endpoint):
    _name = "stocks"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stocks", params=params)


class StockExchangesListEndpoint(AsMixin, Endpoint):
    _name = "stock_exchanges"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):

        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stock_exchanges", params=params)


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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.currency_base is not None:
            params["currency_base"] = self.currency_base
        if self.currency_quote is not None:
            params["currency_quote"] = self.currency_quote

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/forex_pairs", params=params)


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

    def execute(self, format="JSON"):

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
        return self.ctx.http_client.get("/cryptocurrencies", params=params)


class ETFListEndpoint(AsMixin, Endpoint):
    _name = "etf"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/etf", params=params)


class IndicesListEndpoint(AsMixin, Endpoint):
    _name = "indices"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/indices", params=params)


class ExchangesListEndpoint(AsMixin, Endpoint):
    _name = "exchanges"

    def __init__(self,
                 ctx,
                 type=None,
                 name=None,
                 code=None,
                 country=None,
    ):
        self.ctx = ctx
        self.type = type
        self.name = name
        self.code = code
        self.country = country

    def execute(self, format="JSON"):

        params = {}
        if self.type is not None:
            params["type"] = self.type
        if self.name is not None:
            params["name"] = self.name
        if self.code is not None:
            params["code"] = self.code
        if self.country is not None:
            params["country"] = self.country

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/exchanges", params=params)


class CryptocurrencyExchangesListEndpoint(AsMixin, Endpoint):
    _name = "cryptocurrency_exchanges"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):

        params = {}

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/cryptocurrency_exchanges", params=params)


class TechnicalIndicatorsListEndpoint(AsMixin, Endpoint):
    _name = "technical_indicators"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, format="JSON"):

        params = {}

        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/technical_indicators", params=params)


class SymbolSearchEndpoint(AsMixin, Endpoint):
    _name = "indices"

    def __init__(self,
                 ctx,
                 symbol=None,
                 outputsize=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.outputsize = outputsize

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize

        params["format"] = "JSON"
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/symbol_search", params=params)


class EarliestTimestampEndpoint(AsMixin, Endpoint):
    _name = "earliest_timestamp"

    def __init__(self,
                 ctx,
                 symbol=None,
                 interval=None,
                 exchange=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earliest_timestamp", params=params)


class EarningsEndpoint(AsMixin, Endpoint):
    _name = "earnings"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
                 period=None,
                 outputsize=None,
                 start_date=None,
                 end_date=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.period = period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.method = "earnings"

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.period is not None:
            params["period"] = self.period
        if self.outputsize is not None:
            params["outputsize"] = self.outputsize
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earnings", params=params)


class EarningsCalendarEndpoint(AsMixin, Endpoint):
    _name = "earnings_calendar"

    def __init__(self,
                 ctx,
                 symbol=None,
                 exchange=None,
                 country=None,
                 type=None,
                 period=None,
                 start_date=None,
                 end_date=None,
    ):
        self.ctx = ctx
        self.symbol = symbol
        self.exchange = exchange
        self.country = country
        self.type = type
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.method = "earnings_calendar"

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"] = self.symbol
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
        if self.type is not None:
            params["type"] = self.type
        if self.period is not None:
            params["period"] = self.period
        if self.start_date is not None:
            params["start_date"] = self.start_date
        if self.end_date is not None:
            params["end_date"] = self.end_date

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/earnings_calendar", params=params)


class ADEndpoint(AsMixin, Endpoint):
    _name = "ad"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ad"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ad", params=params)


class ADOSCEndpoint(AsMixin, Endpoint):
    _name = "adosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        fast_period=12,
        slow_period=26,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "adosc"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/adosc", params=params)


class ADXEndpoint(AsMixin, Endpoint):
    _name = "adx"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "adx"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/adx", params=params)


class ADXREndpoint(AsMixin, Endpoint):
    _name = "adxr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "adxr"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/adxr", params=params)


class APOEndpoint(AsMixin, Endpoint):
    _name = "apo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        fast_period=12,
        slow_period=26,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "apo"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/apo", params=params)


class AROONEndpoint(AsMixin, Endpoint):
    _name = "aroon"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "aroon"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/aroon", params=params)


class AROONOSCEndpoint(AsMixin, Endpoint):
    _name = "aroonosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "aroonosc"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/aroonosc", params=params)


class ATREndpoint(AsMixin, Endpoint):
    _name = "atr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "atr"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/atr", params=params)


class AVGPRICEEndpoint(AsMixin, Endpoint):
    _name = "avgprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "avgprice"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/avgprice", params=params)


class BBANDSEndpoint(AsMixin, Endpoint):
    _name = "bbands"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=20,
        sd="2",
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "bbands"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/bbands", params=params)


class PercentBEndpoint(AsMixin, Endpoint):
    _name = "percent_b"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=20,
        sd="2",
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "percent_b"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/percent_b", params=params)


class BOPEndpoint(AsMixin, Endpoint):
    _name = "bop"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "bop"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/bop", params=params)


class CCIEndpoint(AsMixin, Endpoint):
    _name = "cci"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=20,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "cci"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/cci", params=params)


class CEILEndpoint(AsMixin, Endpoint):
    _name = "ceil"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ceil"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ceil", params=params)


class CMOEndpoint(AsMixin, Endpoint):
    _name = "cmo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "cmo"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/cmo", params=params)


class COPPOCKEndpoint(AsMixin, Endpoint):
    _name = "coppock"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        long_roc_period=14,
        short_roc_period=11,
        wma_period=0,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "cmo"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.long_roc_period = long_roc_period
        self.short_roc_period = short_roc_period
        self.wma_period = wma_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/coppock", params=params)


class CEILEndpoint(AsMixin, Endpoint):
    _name = "ceil"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ceil"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ceil", params=params)


class DEMAEndpoint(AsMixin, Endpoint):
    _name = "dema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "dema"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/dema", params=params)


class DXEndpoint(AsMixin, Endpoint):
    _name = "dx"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "dx"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/dx", params=params)


class EMAEndpoint(AsMixin, Endpoint):
    _name = "ema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ema"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ema", params=params)


class EXPEndpoint(AsMixin, Endpoint):
    _name = "exp"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "exp"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/exp", params=params)


class FLOOREndpoint(AsMixin, Endpoint):
    _name = "floor"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "floor"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/floor", params=params)


class HEIKINASHICANDLESEndpoint(AsMixin, Endpoint):
    _name = "heikinashicandles"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_price = True
        self.meta_name = "heikinashicandles"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/heikinashicandles", params=params)


class HLC3Endpoint(AsMixin, Endpoint):
    _name = "hlc3"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_price = True
        self.meta_name = "hlc3"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/hlc3", params=params)


class HT_DCPERIODEndpoint(AsMixin, Endpoint):
    _name = "ht_dcperiod"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_dcperiod"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_dcperiod", params=params)


class HT_DCPHASEEndpoint(AsMixin, Endpoint):
    _name = "ht_dcphase"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_dcphase"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_dcphase", params=params)


class HT_PHASOREndpoint(AsMixin, Endpoint):
    _name = "ht_phasor"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_phasor"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_phasor", params=params)


class HT_SINEEndpoint(AsMixin, Endpoint):
    _name = "ht_sine"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_sine"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_sine", params=params)


class HT_TRENDLINEEndpoint(AsMixin, Endpoint):
    _name = "ht_trendline"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_trendline"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_trendline", params=params)


class HT_TRENDMODEEndpoint(AsMixin, Endpoint):
    _name = "ht_trendmode"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ht_trendmode"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ht_trendmode", params=params)


class ICHIMOKUEndpoint(AsMixin, Endpoint):
    _name = "ichimoku"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "vwap"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ichimoku", params=params)


class KAMAEndpoint(AsMixin, Endpoint):
    _name = "kama"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "kama"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/kama", params=params)


class KELTNEREndpoint(AsMixin, Endpoint):
    _name = "keltner"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "keltner"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/keltner", params=params)


class KSTEndpoint(AsMixin, Endpoint):
    _name = "kst"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "kst"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/kst", params=params)


class LINEARREGEndpoint(AsMixin, Endpoint):
    _name = "linearreg"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "linearreg"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/linearreg", params=params)


class LINEARREGANGLEEndpoint(AsMixin, Endpoint):
    _name = "linearregangle"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "linearregangle"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/linearregangle", params=params)


class LINEARREGINTERCEPTEndpoint(AsMixin, Endpoint):
    _name = "linearregintercept"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "linearregintercept"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/linearregintercept", params=params)


class LINEARREGSLOPEEndpoint(AsMixin, Endpoint):
    _name = "linearregslope"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "linearregslope"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/linearregslope", params=params)


class LNEndpoint(AsMixin, Endpoint):
    _name = "ln"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ln"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ln", params=params)


class LOG10Endpoint(AsMixin, Endpoint):
    _name = "log10"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "log10"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/log10", params=params)


class MAEndpoint(AsMixin, Endpoint):
    _name = "ma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ma"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ma", params=params)


class MACDEndpoint(AsMixin, Endpoint):
    _name = "macd"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        fast_period=12,
        slow_period=26,
        signal_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "macd"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/macd", params=params)


class MACDEXTEndpoint(AsMixin, Endpoint):
    _name = "macdext"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "macdext"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/macdext", params=params)


class MAMAEndpoint(AsMixin, Endpoint):
    _name = "mama"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        fast_limit="0.5",
        slow_limit="0.05",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "mama"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.fast_limit = fast_limit
        self.slow_limit = slow_limit
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/mama", params=params)


class MAXEndpoint(AsMixin, Endpoint):
    _name = "max"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "max"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/max", params=params)


class MAXINDEXEndpoint(AsMixin, Endpoint):
    _name = "maxindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "maxindex"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/maxindex", params=params)


class McGinleyDynamicEndpoint(AsMixin, Endpoint):
    _name = "mcginley_dynamic"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "mcginley_dynamic"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/mcginley_dynamic", params=params)


class MEDPRICEEndpoint(AsMixin, Endpoint):
    _name = "medprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "medprice"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/medprice", params=params)


class MFIEndpoint(AsMixin, Endpoint):
    _name = "mfi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "mfi"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/mfi", params=params)


class MIDPOINTEndpoint(AsMixin, Endpoint):
    _name = "midpoint"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "midpoint"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/midpoint", params=params)


class MIDPRICEEndpoint(AsMixin, Endpoint):
    _name = "midprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "midprice"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/midprice", params=params)


class MINEndpoint(AsMixin, Endpoint):
    _name = "min"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "min"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/min", params=params)


class MININDEXEndpoint(AsMixin, Endpoint):
    _name = "minindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "minindex"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/minindex", params=params)


class MINMAXEndpoint(AsMixin, Endpoint):
    _name = "minmax"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "minmax"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/minmax", params=params)


class MINMAXINDEXEndpoint(AsMixin, Endpoint):
    _name = "minmaxindex"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "minmaxindex"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/minmaxindex", params=params)


class MINUS_DIEndpoint(AsMixin, Endpoint):
    _name = "minus_di"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "minus_di"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/minus_di", params=params)


class MINUS_DMEndpoint(AsMixin, Endpoint):
    _name = "minus_dm"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "minus_dm"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/minus_dm", params=params)


class MOMEndpoint(AsMixin, Endpoint):
    _name = "mom"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "mom"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/mom", params=params)


class NATREndpoint(AsMixin, Endpoint):
    _name = "natr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "natr"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/natr", params=params)


class OBVEndpoint(AsMixin, Endpoint):
    _name = "obv"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "obv"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/obv", params=params)


class PLUS_DIEndpoint(AsMixin, Endpoint):
    _name = "plus_di"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "plus_di"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/plus_di", params=params)


class PLUS_DMEndpoint(AsMixin, Endpoint):
    _name = "plus_dm"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "plus_dm"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/plus_dm", params=params)


class PPOEndpoint(AsMixin, Endpoint):
    _name = "ppo"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        fast_period=10,
        slow_period=21,
        ma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ppo"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ppo", params=params)


class ROCEndpoint(AsMixin, Endpoint):
    _name = "roc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "roc"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/roc", params=params)


class ROCPEndpoint(AsMixin, Endpoint):
    _name = "rocp"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "rocp"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/rocp", params=params)


class ROCREndpoint(AsMixin, Endpoint):
    _name = "rocr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "rocr"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/rocr", params=params)


class ROCR100Endpoint(AsMixin, Endpoint):
    _name = "rocr100"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "rocr100"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/rocr100", params=params)


class RSIEndpoint(AsMixin, Endpoint):
    _name = "rsi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "rsi"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/rsi", params=params)


class SAREndpoint(AsMixin, Endpoint):
    _name = "sar"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        acceleration="0.02",
        maximum="0.2",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "sar"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.acceleration = acceleration
        self.maximum = maximum
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/sar", params=params)


class SMAEndpoint(AsMixin, Endpoint):
    _name = "sma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "sma"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/sma", params=params)


class SQRTEndpoint(AsMixin, Endpoint):
    _name = "sqrt"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "sqrt"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/sqrt", params=params)


class STDDEVEndpoint(AsMixin, Endpoint):
    _name = "stddev"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        sd="2",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "stddev"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.sd = sd
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stddev", params=params)


class STOCHEndpoint(AsMixin, Endpoint):
    _name = "stoch"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "stoch"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stoch", params=params)


class STOCHFEndpoint(AsMixin, Endpoint):
    _name = "stochf"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        fast_k_period=14,
        fast_d_period=3,
        fast_dma_type="SMA",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "stochf"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.fast_k_period = fast_k_period
        self.fast_d_period = fast_d_period
        self.fast_dma_type = fast_dma_type
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stochf", params=params)


class STOCHRSIEndpoint(AsMixin, Endpoint):
    _name = "stochrsi"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
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
    ):
        self.is_indicator = True
        self.meta_name = "stochrsi"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
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

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/stochrsi", params=params)


class SuperTrendEndpoint(AsMixin, Endpoint):
    _name = "supertrend"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        multiplier=3,
        period=10,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "supertrend"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.multiplier = multiplier
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/supertrend", params=params)


class T3MAEndpoint(AsMixin, Endpoint):
    _name = "t3ma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        v_factor="0.7",
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "t3ma"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.v_factor = v_factor
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/t3ma", params=params)


class TEMAEndpoint(AsMixin, Endpoint):
    _name = "tema"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "tema"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/tema", params=params)


class TRANGEEndpoint(AsMixin, Endpoint):
    _name = "trange"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "trange"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/trange", params=params)


class TRIMAEndpoint(AsMixin, Endpoint):
    _name = "trima"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "trima"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/trima", params=params)


class TSFEndpoint(AsMixin, Endpoint):
    _name = "tsf"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "tsf"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/tsf", params=params)


class TYPPRICEEndpoint(AsMixin, Endpoint):
    _name = "typprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "typprice"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/typprice", params=params)


class ULTOSCEndpoint(AsMixin, Endpoint):
    _name = "ultosc"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period_1=7,
        time_period_2=14,
        time_period_3=28,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "ultosc"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period_1 = time_period_1
        self.time_period_2 = time_period_2
        self.time_period_3 = time_period_3
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/ultosc", params=params)


class VAREndpoint(AsMixin, Endpoint):
    _name = "var"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "var"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/var", params=params)


class VWAPEndpoint(AsMixin, Endpoint):
    _name = "vwap"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "vwap"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/vwap", params=params)


class WCLPRICEEndpoint(AsMixin, Endpoint):
    _name = "wclprice"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "wclprice"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/wclprice", params=params)


class WILLREndpoint(AsMixin, Endpoint):
    _name = "willr"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        time_period=14,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "willr"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/willr", params=params)


class WMAEndpoint(AsMixin, Endpoint):
    _name = "wma"

    def __init__(
        self,
        ctx,
        symbol,
        interval,
        exchange=None,
        country=None,
        series_type="close",
        time_period=9,
        outputsize=30,
        start_date=None,
        end_date=None,
        dp=5,
        timezone="Exchange",
    ):
        self.is_indicator = True
        self.meta_name = "wma"
        self.ctx = ctx
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        self.country = country
        self.series_type = series_type
        self.time_period = time_period
        self.outputsize = outputsize
        self.start_date = start_date
        self.end_date = end_date
        self.dp = dp
        self.timezone = timezone

    def execute(self, format="JSON"):

        params = {}
        if self.symbol is not None:
            params["symbol"], self.is_batch = get_symbol(self.symbol)
        if self.interval is not None:
            params["interval"] = self.interval
        if self.exchange is not None:
            params["exchange"] = self.exchange
        if self.country is not None:
            params["country"] = self.country
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

        params["format"] = format
        params["apikey"] = self.ctx.apikey
        return self.ctx.http_client.get("/wma", params=params)
