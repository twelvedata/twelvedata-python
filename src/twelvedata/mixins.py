# coding: utf-8

import csv
from .exceptions import (
    BadRequestError,
    InternalServerError,
    InvalidApiKeyError,
    TwelveDataError,
)
from .utils import convert_collection_to_pandas, convert_collection_to_pandas_multi_index, convert_pandas_to_plotly


__all__ = ("AsJsonMixin", "AsCsvMixin", "AsPandasMixin", "AsUrlMixin", "AsMixin")


class AsJsonMixin(object):
    # Top-level response keys that may carry the payload, derived from the
    # OpenAPI response schemas. Checked in order; the first one that is
    # present and truthy is returned. Must be an explicit ordered list —
    # iterating ``json.items()`` would make the result depend on
    # server-side key ordering.
    _JSON_PAYLOAD_KEYS = (
        "values",                 # time series & technical indicators
        "data",                   # reference-data lists, batch, tax_info
        "result",                 # bonds, funds, etfs/list, mutual_funds/list, ...
        "earnings",               # /earnings, /earnings_calendar
        "balance_sheet",          # /balance_sheet, /balance_sheet/consolidated
        "cash_flow",              # /cash_flow, /cash_flow/consolidated
        "income_statement",       # /income_statement, /income_statement/consolidated
        "statistics",             # /statistics
        "dividends",              # /dividends
        "splits",                 # /splits
        "earnings_estimate",      # /earnings_estimate
        "eps_revision",           # /eps_revisions
        "eps_trend",              # /eps_trend
        "growth_estimates",       # /growth_estimates
        "revenue_estimate",       # /revenue_estimate
        "price_target",           # /price_target
        "ratings",                # /analyst_ratings/*
        "trends",                 # /recommendations (primary payload)
        "rating",                 # /recommendations (single-value payload)
        "direct_holders",         # /direct_holders
        "fund_holders",           # /fund_holders
        "institutional_holders",  # /institutional_holders
        "insider_transactions",   # /insider_transactions
        "key_executives",         # /key_executives
        "market_cap",             # /market_cap
        "press_releases",         # /press_releases
        "etf",                    # /etfs/world, /etfs/world/*
        "mutual_fund",            # /mutual_funds/world, /mutual_funds/world/*
        "sanctions",              # /sanctions/{source}
    )

    def as_json(self):
        resp = self.execute(format="JSON")
        json = resp.json()
        if hasattr(self, 'is_batch') and self.is_batch:
            return json
        if not isinstance(json, dict):
            return json
        if json.get("status") == "error":
            return json
        if 'result' in json and isinstance(json['result'], dict) and 'list' in json['result'] \
                and isinstance(json['result']['list'], list):
            return json['result']['list']
        for key in self._JSON_PAYLOAD_KEYS:
            if key in json:
                return json[key]
        return json

    def as_raw_json(self):
        resp = self.execute(format="JSON")
        return resp.text


class AsCsvMixin(object):
    def as_csv(self, **kwargs):
        resp = self.execute(format="CSV")
        lines = resp.text.strip().split("\n")
        delimiter = "," if "," in lines[0] else ";"
        kwargs["delimiter"] = kwargs.get("delimiter", delimiter)
        return tuple(map(tuple, csv.reader(lines, **kwargs)))

    def as_raw_csv(self):
        resp = self.execute(format="CSV")
        return resp.text


# Strategy -> (kind, index_field). kind in {"datetime", "date", "grouped", "flat", "single"}.
# Endpoints not listed and without `is_indicator` fall through to ("flat", None) — a plain
# DataFrame with no forced index. Technical indicators are routed to the "datetime" strategy
# via the `is_indicator` flag set in utils.patch_endpoints_meta.
_PANDAS_STRATEGIES = {
    # explicit anchors for the datetime path (behavior unchanged)
    "time_series":                       ("datetime", "datetime"),
    "time_series_cross":                 ("datetime", "datetime"),
    "quote":                             ("datetime", "datetime"),
    "eod":                               ("datetime", "datetime"),
    "exchange_rate":                     ("single", None),
    "currency_conversion":               ("single", None),
    "earliest_timestamp":                ("datetime", "datetime"),
    "press_releases":                    ("datetime", "datetime"),
    "edgar_filings_archive":             ("date", "filed_at"),

    # date-indexed lists of records
    "splits":                            ("date", "date"),
    "dividends":                         ("date", "ex_date"),
    "earnings":                          ("date", "date"),
    "splits_calendar":                   ("date", "date"),
    "dividends_calendar":                ("date", "ex_date"),
    "balance_sheet":                     ("date", "fiscal_date"),
    "balance_sheet_consolidated":        ("date", "fiscal_date"),
    "cash_flow":                         ("date", "fiscal_date"),
    "cash_flow_consolidated":            ("date", "fiscal_date"),
    "income_statement":                  ("date", "fiscal_date"),
    "income_statement_consolidated":     ("date", "fiscal_date"),
    "earnings_estimate":                 ("date", "date"),
    "revenue_estimate":                  ("date", "date"),
    "eps_trend":                         ("date", "date"),
    "eps_revisions":                     ("date", "date"),
    "market_cap":                        ("date", "date"),
    "analyst_ratings_light":             ("date", "date"),
    "analyst_ratings_us_equities":       ("date", "date"),
    "insider_transactions":              ("date", "date_reported"),
    "institutional_holders":             ("date", "date_reported"),
    "fund_holders":                      ("date", "date_reported"),
    "direct_holders":                    ("date", "date_reported"),

    # dict[date_str -> list[record]] — flatten then date-index
    "earnings_calendar":                 ("grouped", "date"),
    "ipo_calendar":                      ("grouped", "date"),

    # list of records, no temporal key
    "stocks":                            ("flat", None),
    "stock_exchanges":                   ("flat", None),
    "forex_pairs":                       ("flat", None),
    "cryptocurrencies":                  ("flat", None),
    "etfs":                              ("flat", None),
    "indices":                           ("flat", None),
    "funds":                             ("flat", None),
    "bonds":                             ("flat", None),
    "commodities":                       ("flat", None),
    "exchanges":                         ("flat", None),
    "cryptocurrency_exchanges":          ("flat", None),
    "exchange_schedule":                 ("flat", None),
    "countries":                         ("flat", None),
    "cross_listings":                    ("flat", None),
    "intervals":                         ("flat", None),
    "instrument_type":                   ("flat", None),
    "symbol_search":                     ("flat", None),
    "technical_indicators":              ("flat", None),
    "market_state":                      ("flat", None),
    "market_movers_market":              ("flat", None),
    "last_change_endpoint":              ("flat", None),
    "sanctions_source":                  ("flat", None),
    "etfs_list":                         ("flat", None),
    "etfs_type":                         ("flat", None),
    "etfs_family":                       ("flat", None),
    "mutual_funds_list":                 ("flat", None),
    "mutual_funds_type":                 ("flat", None),
    "mutual_funds_family":               ("flat", None),
    "key_executives":                    ("flat", None),
    "options_expiration":                ("flat", None),
    "options_chain":                     ("flat", None),

    # single-record / metadata payload — wrap in 1-row DataFrame
    "profile":                           ("single", None),
    "statistics":                        ("single", None),
    "logo":                              ("single", None),
    "tax_info":                          ("single", None),
    "recommendations":                   ("single", None),
    "price_target":                      ("single", None),
    "growth_estimates":                  ("single", None),
    "price":                             ("single", None),
    "api_usage":                         ("single", None),
    "etfs_world":                        ("single", None),
    "etfs_world_summary":                ("single", None),
    "etfs_world_composition":            ("single", None),
    "etfs_world_performance":            ("single", None),
    "etfs_world_risk":                   ("single", None),
    "mutual_funds_world":                ("single", None),
    "mutual_funds_world_summary":        ("single", None),
    "mutual_funds_world_composition":    ("single", None),
    "mutual_funds_world_performance":    ("single", None),
    "mutual_funds_world_risk":           ("single", None),
    "mutual_funds_world_ratings":        ("single", None),
    "mutual_funds_world_purchase_info":  ("single", None),
    "mutual_funds_world_sustainability": ("single", None),
}


class AsPandasMixin(object):
    def as_pandas(self, **kwargs):
        import pandas as pd

        assert hasattr(self, "as_json")

        data = self.as_json()

        if isinstance(data, dict) and data.get("status") == "error":
            code = data.get("code")
            message = data.get("message", "API error")
            if code == 401:
                raise InvalidApiKeyError(message)
            if code == 400:
                raise BadRequestError(message)
            if isinstance(code, int) and code >= 500:
                raise InternalServerError(message)
            raise TwelveDataError(message)

        if getattr(self, "is_batch", False):
            return convert_collection_to_pandas_multi_index(data)

        if not data:
            return pd.DataFrame()

        if getattr(self, "is_indicator", False):
            kind, index_field = ("datetime", "datetime")
        else:
            kind, index_field = _PANDAS_STRATEGIES.get(
                getattr(self, "_name", "") or "", ("flat", None)
            )

        if kind == "datetime":
            return self.create_basic_df(data, pd, index_column="datetime", **kwargs)
        if kind == "date":
            return self.create_basic_df(data, pd, index_column=index_field, **kwargs)
        if kind == "grouped":
            rows = []
            for key, items in (data or {}).items():
                for item in items:
                    item[index_field] = key
                    rows.append(item)
            return self.create_basic_df(rows, pd, index_column=index_field, **kwargs)
        if kind == "single":
            if isinstance(data, list):
                rows = data
            elif isinstance(data, dict):
                rows = [data]
            else:
                rows = [{"value": data}]
            return pd.DataFrame(rows)

        # "flat" (default): list of records, no temporal index
        if isinstance(data, list) and data and not isinstance(data[0], dict):
            return pd.DataFrame({"value": data})
        df = convert_collection_to_pandas(data, **kwargs)
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
        return df

    @staticmethod
    def create_basic_df(data, pd, index_column="datetime", **kwargs):
        df = convert_collection_to_pandas(data, **kwargs)
        df = df.set_index(index_column)
        df.index = pd.to_datetime(df.index)

        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                df[col] = df[col]
        return df


class AsUrlMixin(object):
    def as_url(self, **kwargs):
        return self.execute(debug=True)


class AsMixin(AsJsonMixin, AsCsvMixin, AsPandasMixin, AsUrlMixin, object):
    pass
