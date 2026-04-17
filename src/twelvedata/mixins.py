# coding: utf-8

import csv
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
        if isinstance(json, dict) and json.get("status") == "ok":
            if 'result' in json and isinstance(json['result'], dict) and 'list' in json['result'] \
                    and isinstance(json['result']['list'], list):
                return json['result']['list']
            for key in self._JSON_PAYLOAD_KEYS:
                value = json.get(key)
                if value:
                    return value
            return []
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


class AsPandasMixin(object):
    def as_pandas(self, **kwargs):
        import pandas as pd

        assert hasattr(self, "as_json")

        data = self.as_json()
        if hasattr(self, "is_batch") and self.is_batch:
            df = convert_collection_to_pandas_multi_index(data)
        elif hasattr(self, "method") and self.method == "earnings":
            df = self.create_basic_df(data, pd, index_column="date", **kwargs)
        elif hasattr(self, "method") and self.method == "earnings_calendar":
            modified_data = []
            for date, row in data.items():
                for earning in row:
                    earning["date"] = date
                    modified_data.append(earning)

            df = self.create_basic_df(modified_data, pd, index_column="date", **kwargs)
        else:
            df = self.create_basic_df(data, pd, **kwargs)

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
