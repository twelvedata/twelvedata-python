# coding: utf-8

import csv
from .utils import convert_collection_to_pandas, convert_collection_to_pandas_multi_index, convert_pandas_to_plotly


__all__ = ("AsJsonMixin", "AsCsvMixin", "AsPandasMixin", "AsUrlMixin", "AsMixin")


class AsJsonMixin(object):
    def as_json(self):
        resp = self.execute(format="JSON")
        json = resp.json()
        if hasattr(self, 'is_batch') and self.is_batch:
            return json
        if json.get("status") == "ok":
            return json.get("data") or json.get("values") or json.get("earnings") or []
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
        df.index = pd.to_datetime(df.index, infer_datetime_format=True)

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        return df


class AsUrlMixin(object):
    def as_url(self, **kwargs):
        return self.execute(debug=True)


class AsMixin(AsJsonMixin, AsCsvMixin, AsPandasMixin, AsUrlMixin, object):
    pass
