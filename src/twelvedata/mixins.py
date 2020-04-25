# coding: utf-8

import csv
from .utils import convert_collection_to_pandas, convert_collection_to_pandas_multi_index, convert_pandas_to_plotly


__all__ = ("AsJsonMixin", "AsCsvMixin", "AsPandasMixin", "AsPlotMixin", "AsMixin")


class AsJsonMixin(object):
    def as_json(self):
        resp = self.execute(format="JSON")
        json = resp.json()
        if hasattr(self, 'is_batch') and self.is_batch:
            return json
        if json.get("status") == "ok":
            return json.get("data") or json.get("values") or []

    def as_raw_json(self):
        resp = self.execute(format="JSON")
        return resp.text


class AsCsvMixin(object):
    def as_csv(self, **kwargs):
        resp = self.execute(format="CSV")
        lines = resp.text.strip().split("\n")
        kwargs["delimiter"] = kwargs.get("delimiter", ";")
        return tuple(map(tuple, csv.reader(lines, **kwargs)))

    def as_raw_csv(self):
        resp = self.execute(format="CSV")
        return resp.text


class AsPandasMixin(object):
    def as_pandas(self, **kwargs):
        import pandas as pd

        assert hasattr(self, "as_json")

        data = self.as_json()
        if hasattr(self, 'is_batch') and self.is_batch:
            df = convert_collection_to_pandas_multi_index(data)
        else:
            df = convert_collection_to_pandas(data, **kwargs)
            df = df.set_index("datetime")
            df.index = pd.to_datetime(df.index, infer_datetime_format=True)

            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="ignore")

        return df


class AsMixin(AsJsonMixin, AsCsvMixin, AsPandasMixin, object):
    pass
