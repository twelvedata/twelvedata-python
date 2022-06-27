# coding: utf-8

import inspect
import operator
import functools
import textwrap
import pytimeparse

from .exceptions import BadRequestError


def patch_endpoints_meta(ctx):
    """
    Loads technical indicators metadata from the remote source 
    and patches endpoint classes according to the loaded metadata.
    """
    from . import endpoints

    if hasattr(patch_endpoints_meta, "patched"):
        return

    meta_ep = endpoints.TechIndicatorsMetaEndpoint(ctx)
    all_meta = meta_ep.as_json()

    for ep in (getattr(endpoints, attr) for attr in endpoints.__all__):
        meta = all_meta.get(ep._name)

        if meta is None:
            continue
        else:
            ep.is_indicator = True

        if "overlay" in meta:
            ep.is_overlay = meta["overlay"]

        if "output_values" in meta:
            ep.colormap = {
                k: v["default_color"]
                for k, v in meta["output_values"].items()
                if "default_color" in v
            }

        if "tinting" in meta:
            fill_area = meta["tinting"].get("area") or {}
            ep.fill_area = fill_area

    setattr(patch_endpoints_meta, "patched", True)


def force_use_kwargs(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if args:
            raise RuntimeError("Use kwargs only, please")
        return func(self, **kwargs)

    return wrapper


def apply_context_defaults(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func_args = inspect.getargs(func.__code__).args
        func_args.remove("self")

        _kwargs = {k: v for k, v in self.ctx.defaults.items() if k in func_args}
        _kwargs.update(kwargs)
        return func(self, *args, **_kwargs)

    return wrapper


def convert_pandas_to_plotly(df, **kwargs):
    """
    Converts pandas DataFrame to plotly figure

    :param df: pandas DataFrame
    """
    try:
        import plotly.graph_objs as go
    except ImportError:
        raise ImportError(
            textwrap.dedent(
                """
                    No module named 'plotly'. You can install it with follow command:

                    > pip install twelvedata[pandas, plotly] 

                    or 

                    > pip install plotly
                """
            ).strip()
        )

    traces = [
        go.Scatter(x=df.index, y=df[col], mode="lines", name=col) for col in df.columns
    ]

    return go.Figure(traces)


def add_null_obj_values(obj, columns) -> dict:
    for col in columns:
        if col not in obj:
            obj[col] = None
    return obj


def convert_collection_to_pandas(val, indexing_type=None):
    """
    Converts list/dict to DataFrame

    :param val: list or dict
    :returns: pandas DataFrame
    """
    try:
        import pandas
    except ImportError:
        raise ImportError(
            textwrap.dedent(
                """
                    No module named 'pandas'. You can install it with follow command:

                    > pip install twelvedata[pandas] 

                    or 

                    > pip install pandas
                """
            ).strip()
        )

    if isinstance(val, (list, tuple)):
        if len(val) == 0:
            return pandas.DataFrame()
        else:
            columns_beg = tuple(val[0].keys())
            columns_end = tuple(val[-1].keys())
            get_row = operator.itemgetter(*columns_end)
            data = [get_row(add_null_obj_values(obj, columns_end)) if
                    columns_beg != columns_end else
                    get_row(obj) for obj in val]
            return pandas.DataFrame(data, columns=columns_end)
    elif isinstance(val, dict):
        try:
            return pandas.DataFrame.from_dict(val, orient="index", dtype="float")
        except ValueError:
            return pandas.DataFrame.from_dict(
                {'data_key': val}, orient="index", dtype="object"
            )
    else:
        raise ValueError("Expected list, tuple or dict, but {} found".format(type(val)))


def convert_collection_to_pandas_multi_index(val):
    try:
        import pandas
    except ImportError:
        raise ImportError(
            textwrap.dedent(
                """
                    No module named 'pandas'. You can install it with follow command:

                    > pip install twelvedata[pandas] 

                    or 

                    > pip install pandas
                """
            ).strip()
        )

    columns = ()
    for symbol, data in val.items():
        if data['status'] == 'error':
            raise BadRequestError(data['message'])
        keys = list(data['values'][-1].keys())[1:]
        if len(keys) > len(columns):
            columns = keys

    arr = []
    multi_index = []

    for symbol, data in val.items():
        if 'values' in data:
            values = data['values']
            for quote in values:
                candle = tuple(quote.values())
                multi_index.append((symbol, candle[0]))
                arr.append(candle[1:])

    idx = pandas.MultiIndex.from_tuples(multi_index)

    return pandas.DataFrame(arr, index=idx, columns=columns)


def parse_interval_in_minutes(interval):
    """
    Parses the interval and tries to return its value as minutes.

    :param interval: string such as 1min, 5min, 10h, 12week and etc.
    :returns: int or None
    """

    # Pytimeparse can't handle months, so we replace 1 month with 5 weeks. 
    # The value is not exact, but it is quite acceptable for our needs
    if 'month' in interval:
        tmp = interval.replace('month', '').strip()
        if tmp.isnumeric():
            interval = "{}week".format(5 * int(tmp))

    secs = pytimeparse.parse(interval)

    if secs is not None:
        return secs / 60
    else:
        return None
