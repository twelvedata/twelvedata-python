# coding: utf-8

import time
import pytimeparse
import re
import itertools
from collections import OrderedDict, Counter

from .endpoints import *
from .utils import apply_context_defaults, force_use_kwargs, parse_interval_in_minutes

__all__ = ("TimeSeries",)


class TimeSeries(object):
    def __init__(
            self, ctx, endpoints=(), price_endpoint=None, price_endpoint_enabled=True
    ):
        self.ctx = ctx
        self.price_endpoint_enabled = price_endpoint_enabled
        self.price_endpoint = price_endpoint or TimeSeriesEndpoint(
            self.ctx, **self.ctx.defaults
        )
        self.endpoints = endpoints

    def clone(self):
        return TimeSeries(
            ctx=self.ctx,
            endpoints=self.endpoints,
            price_endpoint=self.price_endpoint,
            price_endpoint_enabled=self.price_endpoint_enabled,
        )

    def as_json(self):
        out = OrderedDict()
        is_batch = False
        postfixes = self._generate_postfixes()

        error_symbols = []
        if self.price_endpoint_enabled:
            time_series_json = self.price_endpoint.as_json()
            is_batch = self.price_endpoint.is_batch
            for row_symbol in time_series_json:
                if self.price_endpoint.is_batch:
                    values = OrderedDict()
                    if time_series_json[row_symbol]['status'] == 'error':
                        error_symbols.append(row_symbol)
                        continue
                    for v in time_series_json[row_symbol]['values']:
                        values.setdefault(v["datetime"], {}).update(v)
                    out[row_symbol] = values
                else:
                    out.setdefault(row_symbol["datetime"], {}).update(row_symbol)

        for ep in self.endpoints:
            postfix = str(next(postfixes[ep.__class__]))
            indicator_json = ep.as_json()
            for row in indicator_json:
                if ep.is_batch:
                    if row.upper() in error_symbols:
                        continue
                    values = out[row]
                    for v in indicator_json[row]['values']:
                        if postfix:
                            v = {
                                (k if k == "datetime" else "{}_{}".format(k, postfix)): v
                                for k, v in v.items()
                            }
                        values.setdefault(v["datetime"], {}).update(v)
                    out[row] = values
                else:
                    if postfix:
                        row = {
                            (k if k == "datetime" else "{}_{}".format(k, postfix)): v
                            for k, v in row.items()
                        }
                    out.setdefault(row["datetime"], {}).update(row)

        if is_batch:
            for k, v in out.items():
                out[k] = tuple(v.values())
            return dict(out)

        return tuple(out.values())

    def as_csv(self, **kwargs):
        out = OrderedDict()
        postfixes = self._generate_postfixes()

        if self.price_endpoint_enabled:
            for row in self.price_endpoint.as_csv():
                out.setdefault(row[0], []).extend(row)

        for ep in self.endpoints:
            postfix = str(next(postfixes[ep.__class__]))

            for row in ep.as_csv(**kwargs):
                if row[0] == "datetime":
                    row = ["{}{}".format(header, postfix) for header in row[1:]]
                    row.insert(0, "datetime")
                if not out:
                    out.setdefault(row[0], []).extend(row)
                else:
                    out.setdefault(row[0], []).extend(row[1:])

        return tuple(out.values())

    def as_pandas(self, **kwargs):
        import pandas

        postfixes = self._generate_postfixes()

        if self.price_endpoint_enabled:
            df = self.price_endpoint.as_pandas()
        else:
            df = None

        for ep in self.endpoints:
            tmp_df = ep.as_pandas(**kwargs)
            tmp_df = tmp_df.add_suffix(str(next(postfixes[ep.__class__])))

            if df is None:
                df = tmp_df
                continue

            df = pandas.merge(
                df, tmp_df, how="left", left_index=True, right_index=True
            )

        return df

    def as_url(self, **kwargs):
        urls = list()
        if self.price_endpoint_enabled:
            urls.append(self.price_endpoint.as_url())
        for ep in self.endpoints:
            urls.append(ep.as_url())
        return urls

    def _has_overlays(self):
        return any(ep.is_overlay for ep in self.endpoints)

    def _count_subplots(self):
        """Count how many charts should be displayed"""
        if self.price_endpoint_enabled or self._has_overlays():
            subplots_count = 1
        else:
            subplots_count = 0

        for ep in self.endpoints:
            subplots_count += ep.is_indicator and not ep.is_overlay
        return subplots_count

    def _chart_title(self):
        return "{} - {}".format(
            self.ctx.defaults.get("symbol").upper(), self.ctx.defaults.get("interval")
        )

    def _generate_postfixes(self):
        # If user specified multiple same endpoints we should add postfixes
        postfixes = {}
        empty = itertools.cycle(("",))

        for cls, n in Counter(ep.__class__ for ep in self.endpoints).items():
            if n > 1:
                postfixes[cls] = itertools.count(1)
            else:
                postfixes[cls] = empty

        return postfixes

    def as_pyplot_figure(self, figsize=(16, 8), candle_width=0.0002):
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        from pandas.plotting import register_matplotlib_converters

        register_matplotlib_converters()

        plt.rcParams["figure.figsize"] = figsize
        subplots_count = self._count_subplots()

        def mark_xaxis_as_date(x):
            x.xaxis_date()
            x.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
            x.xaxis.set_major_locator(mticker.MaxNLocator(10))
            for label in x.xaxis.get_ticklabels():
                label.set_rotation(45)
            x.grid(True)

        # All subplots should be %25 from height of main plot
        if self.price_endpoint_enabled:
            gridspec = {
                "width_ratios": [1],
                "height_ratios": [4] + ([1] * (subplots_count - 1)),
            }
        else:
            gridspec = {"width_ratios": [1], "height_ratios": [1] * subplots_count}

        # Create multiple plots with shared X-axis
        fig, axs = plt.subplots(subplots_count, 1, sharex=True, gridspec_kw=gridspec)
        fig.suptitle(self._chart_title(), x=0.44, y=0.95)
        ax_iter = iter((axs,)) if subplots_count == 1 else iter(axs)

        # Binding a width of the candles to the interval, otherwise
        # the candles will be too thin
        interval = self.ctx.defaults.get("interval", "1min")
        interval_minutes = parse_interval_in_minutes(interval) or 1

        # Render price chart first
        price_ax = None
        if self.price_endpoint_enabled:
            price_ax = next(ax_iter)
            self.price_endpoint.render_matplotlib(
                ax=price_ax,
                candle_width=candle_width,
                interval_minutes=interval_minutes,
            )
            price_ax.yaxis.tick_right()
            price_ax.yaxis.set_label_position("right")
            mark_xaxis_as_date(price_ax)
        elif self._has_overlays():
            price_ax = next(ax_iter)

        # Render tech indicators
        # postfixes = self._generate_postfixes()
        # for ep in self.endpoints:
        #     if ep.is_overlay:
        #         ax = price_ax
        #     else:
        #         ax = next(ax_iter)
        #         ax.margins(0.25)
        #
        #     ax.yaxis.tick_right()
        #     ax.yaxis.set_label_position("right")
        #
        #     postfix = next(postfixes[ep.__class__])
        #     ep.render_matplotlib(
        #         ax=ax, interval_minutes=interval_minutes, postfix=postfix
        #     )
        #
        #     if not ep.is_overlay:
        #         mark_xaxis_as_date(ax)
        #
        #     ax.legend(loc="upper left")

        plt.subplots_adjust(wspace=0, hspace=0, left=0.1, right=0.8)
        plt.xlabel("Time")

        return fig

    def show_pyplot(self, figsize=(20, 10), candle_width=0.002):
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        mpl.use("WebAgg")
        self.as_pyplot_figure(figsize=figsize, candle_width=candle_width)
        plt.show()

    def as_plotly_figure(self):
        from plotly.subplots import make_subplots
        import plotly.graph_objs as go

        subplots_count = self._count_subplots()

        # All subplots should have %25 height from the main plot
        if self.price_endpoint_enabled:
            row_width = [1]
            row_width.extend([0.25] * (subplots_count - 1))
        else:
            row_width = [1] * subplots_count

        fig = make_subplots(
            rows=subplots_count,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0,
            row_width=row_width[::-1],
        )

        # Draw main plot
        if self.price_endpoint_enabled:
            price_traces = self.price_endpoint.render_plotly(fig=fig)
            fig.add_trace(price_traces[0], 1, 1)

            for trace in price_traces[1:]:
                fig.add_trace(trace)

        # Draw other subplots
        postfixes = self._generate_postfixes()

        overlay_endpoints = (ep for ep in self.endpoints if ep.is_overlay)
        for ep in overlay_endpoints:
            postfix = next(postfixes[ep.__class__])
            for ep_trace in ep.render_plotly(postfix=postfix):
                fig.add_trace(ep_trace)

        if self.price_endpoint_enabled or self._has_overlays():
            start_index = 2
        else:
            start_index = 1

        separate_endpoints = (ep for ep in self.endpoints if not ep.is_overlay)
        for idx, ep in enumerate(separate_endpoints, start=start_index):
            postfix = next(postfixes[ep.__class__])
            for ep_trace in ep.render_plotly(postfix=postfix):
                fig.add_trace(ep_trace, idx, 1)

        # Move all ticks on Y-axis to the right
        for yaxis in (fig.layout[attr] for attr in fig.layout if attr[:5] == "yaxis"):
            yaxis.side = "right"
            yaxis.mirror = "allticks"

        # Set title and remove rangeslider
        fig.update(
            layout_title={
                "text": self._chart_title(),
                "x": 0.5,
                "xanchor": "center",
                "y": 0.9,
                "yanchor": "top",
            },
            layout_xaxis_rangeslider_visible=False,
        )

        return fig

    def show_plotly(self):
        fig = self.as_plotly_figure()
        fig.show()

    def _with_endpoint(self, ep):
        ts = self.clone()
        ts.endpoints += (ep,)
        return ts

    def _with_price_endpoint(self, ep):
        ts = self.clone()
        ts.price_endpoint = ep
        return ts

    def without_ohlc(self):
        """
        Disable price data/chart
        """
        ts = self.clone()
        ts.price_endpoint_enabled = False
        return ts

    def with_ohlc(self):
        """
        Enable price data/chart
        """
        ts = self.clone()
        ts.price_endpoint_enabled = True
        return ts

    @force_use_kwargs
    @apply_context_defaults
    def with_ad(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of AD to chart builder

        Chaikin A/D Line(AD) calculates Advance/Decline of an asset. This
        indicator belongs to the group of Volume Indicators.

        This API call returns meta and time series values of AD. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Name of instrument you want to request
            For preffered stocks use dot(.) delimiterE.g. BRK.A or BRK.B will be
            correct
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ADEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_adosc(
            self,
            exchange=None,
            country=None,
            fast_period=12,
            slow_period=26,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ADOSC to chart builder

        Chaikin A/D Oscillator(ADOSC) is an indicator of indicator which has
        an idea to find relationship between increasing and deacreasing volume
        with price fluctuations. The Chaikin Oscillator measures the momentum
        of the Accumulation/Distribution Line(ADL) using two Exponential
        Moving Averages of varying length to the line(MACD).

        This API call returns meta and time series values of ADOSC. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Name of instrument you want to request
            For preffered stocks use dot(.) delimiter.
            E.g. BRK.A or BRK.B will be correct
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
            otherwise is ignored. Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param fast_period: Number of periods for fast moving average.
            Must be at least 1
        :param slow_period: Number of periods for slow moving average.
            Must be at least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ADOSCEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            fast_period=fast_period,
            slow_period=slow_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_adx(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ADX to chart builder

        Average Directional Movement Index(ADX) is used to decide if the price
        trend is strong.

        This API call returns meta and time series values of ADX. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency. E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ADXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_adxr(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ADXR to chart builder

        Average Directional Movement Index Rating(ADXR) is a smoothed version
        of ADX indicator. ADXR quantifies momentum change in the ADX.

        This API call returns meta and time series values of ADXR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency. E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ADXREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_apo(
            self,
            exchange=None,
            country=None,
            time_period=9,
            fast_period="12",
            slow_period="26",
            ma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of APO to chart builder

        Absolute Price Oscillator(APO) calculates the difference between two
        price moving averages.

        This API call returns meta and time series values of APO. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency. E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param fast_period: Number of periods for fast moving average. Must
        be at least 1
        :param slow_period: Number of periods for slow moving average. Must
        be at least 1
        :param ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = APOEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            fast_period=fast_period,
            slow_period=slow_period,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_aroon(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of AROON to chart builder

        Aroon Indicator(AROON) is used to identify if the price is trending.
        It can also spot beginning of new trend and it's strength.

        This API call returns meta and time series values of AROON. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = AROONEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_aroonosc(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of AROONOSC to chart builder

        Aroon Oscillator(AROONOSC) uses classic Aroon(Aroon Up and Aroon down)
        to measure the strength of persisting trend and it's chances to
        persist.

        This API call returns meta and time series values of AROONOSC. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = AROONOSCEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_atr(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ATR to chart builder

        Average True Range(ATR) is used to measure market volatility by
        decomposing all asset prices over specified time period.

        This API call returns meta and time series values of ATR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ATREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_avgprice(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of AVGPRICE to chart builder

        Average Price(AVGPRICE) uses formula: (open + high + low + close) / 4.

        This API call returns meta and time series values of AVGPRICE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = AVGPRICEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_bbands(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of BBANDS to chart builder

        Bollinger Bands(BBANDS) are volatility bands located above and below a
        moving average. Volatility size parameter depends on standard
        deviation.

        This API call returns meta and time series values of BBANDS. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param sd: Number of standard deviations. Must be at least 1
        :param ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = BBANDSEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            sd=sd,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_beta(
            self,
            exchange=None,
            country=None,
            series_type_1="open",
            series_type_2="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of BETA to chart builder

        Statistic Beta function.

        This API call returns meta and time series values of BBANDS. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type_1: Price type used as the first part of technical indicator
        :param series_type_2: Price type used as the second part of technical indicator
        :param time_period: Number of periods to average over. Takes values in the range from 1 to 800
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = BETAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type_1=series_type_1,
            series_type_2=series_type_2,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_percent_b(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Creates request builder for %B

        %B Indicator(%B) measures position of an asset price relative to upper
        and lower Bollinger Bands.

        This API call returns meta and time series values of %B. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param sd: Number of standard deviations. Must be at least 1
        :param ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = PercentBEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            sd=sd,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_pivot_points_hl(
            self,
            exchange=None,
            country=None,
            time_period=10,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Creates request builder for Pivot Points (High/Low)

        Pivot Points (High/Low) (PIVOT_POINTS_HL) are typically used to foresee potential price reversals.

        This API call returns meta and time series values of PIVOT_POINTS_HL. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time descending updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = PivotPointsHLEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_bop(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of BOP to chart builder

        Balance Of Power(BOP) measures relative strength between buyers and
        sellers by assessing the ability of move price to an extreme level.

        This API call returns meta and time series values of BOP. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = BOPEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_cci(
            self,
            exchange=None,
            country=None,
            time_period=20,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of CCI to chart builder

        Commodity Channel Index(CCI) is a universal indicator that can help to
        identify new trend and assess current critical conditions.

        This API call returns meta and time series values of CCI. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = CCIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ceil(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of CEIL to chart builder

        Vector CEIL(CEIL) transform input data with mathematical ceil
        function.

        This API call returns meta and time series values of CEIL. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = CEILEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_cmo(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of CMO to chart builder

        Chande Momentum Oscillator(CMO) is used to show overbought and
        oversold conditions.

        This API call returns meta and time series values of CMO. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = CMOEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_coppock(
            self,
            exchange=None,
            country=None,
            series_type="close",
            long_roc_period=14,
            short_roc_period=11,
            wma_period=10,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of COPPOCK to chart builder

        Coppock Curve(COPPOCK) is usually used to detect long-term trend changes, typically on monthly charts.

        This API call returns meta and time series values of CMO. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param long_roc_period: Number of periods for long term rate of change. Takes values in the range from 1 to 500
        :param short_roc_period: Number of periods for short term rate of change. Takes values in the range from 1 to 500
        :param wma_period: Number of periods for weighted moving average. Takes values in the range from 1 to 500
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = COPPOCKEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            long_roc_period=long_roc_period,
            short_roc_period=short_roc_period,
            wma_period=wma_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ceil(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of CEIL to chart builder

        Vector CEIL(CEIL) transform input data with mathematical ceil
        function.

        This API call returns meta and time series values of CEIL. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = CEILEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_dema(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of DEMA to chart builder

        Double Exponential Moving Average(DEMA) it used to eliminate lag. It
        does this by taking two Exponential Moving Averages(EMA)).

        This API call returns meta and time series values of DEMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = DEMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_dx(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of DX to chart builder

        Directional Movement Index(DX) identifies in which direction the price
        is moving.

        This API call returns meta and time series values of DX. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = DXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ema(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of EMA to chart builder

        Exponential Moving Average(EMA) it places greater importance on recent
        data points than the normal Moving Average(MA).

        This API call returns meta and time series values of EMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = EMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_exp(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of EXP to chart builder

        Exponential(EXP) transform input data with mathematical exponent
        function.

        This API call returns meta and time series values of EXP. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = EXPEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_floor(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of FLOOR to chart builder

        Vector FLOOR(FLOOR) transform input data with mathematical floor
        function.

        This API call returns meta and time series values of FLOOR. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = FLOOREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_heikinashicandles(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HEIKINASHICANDLES to chart builder

        Heikin-Ashi Candles(HEIKINASHICANDLES) translating from Japanese it
        means "average bar". It can be used detect market trends and predict
        future price fluctuations..

        This API call returns meta and time series values of
        HEIKINASHICANDLES. Meta object consists of general information about
        requested technical indicator. Time series is the array of objects
        ordered by time desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HEIKINASHICANDLESEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_price_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_hlc3(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HLC3 to chart builder

        High, Low, Close Average(HLC3) gives alternative candlesticks patter.
        Every element is defined as follows: (high + low + close) / 3.

        This API call returns meta and time series values of HLC3. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HLC3Endpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_price_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_dcperiod(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_DCPERIOD to chart builder

        Hilbert Transform Dominant Cycle Period(HT_DCPERIOD) is part of
        Hilbert Transforms concepts. You can reed more about it in the Rocket
        Science for Traders book by John F. Ehlers.

        This API call returns meta and time series values of HT_DCPERIOD. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_DCPERIODEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_dcphase(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_DCPHASE to chart builder

        Hilbert Transform Dominant Cycle Phase(HT_DCPHASE) is part of Hilbert
        Transforms concepts. You can reed more about it in the Rocket Science
        for Traders book by John F. Ehlers.

        This API call returns meta and time series values of HT_DCPHASE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_DCPHASEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_phasor(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_PHASOR to chart builder

        Hilbert Transform Phasor Components(HT_PHASOR) is part of Hilbert
        Transforms concepts. You can reed more about it in the Rocket Science
        for Traders book by John F. Ehlers.

        This API call returns meta and time series values of HT_PHASOR. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_PHASOREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_sine(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_SINE to chart builder

        Hilbert Transform SineWave(HT_SINE) is part of Hilbert Transforms
        concepts. You can reed more about it in the Rocket Science for Traders
        book by John F. Ehlers.

        This API call returns meta and time series values of HT_SINE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_SINEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_trendline(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_TRENDLINE to chart builder

        Hilbert Transform Instantaneous Trendline(HT_TRENDLINE) comes from the
        concept of Digital Signal Processing (DSP). It creates complex signals
        from the simple chart data. You can reed more about it in the Rocket
        Science for Traders book by John F. Ehlers.

        This API call returns meta and time series values of HT_TRENDLINE.
        Meta object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_TRENDLINEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ht_trendmode(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of HT_TRENDMODE to chart builder

        Hilbert Transform Trend vs Cycle Mode(HT_TRENDMODE) is part of Hilbert
        Transforms concepts. You can reed more about it in the Rocket Science
        for Traders book by John F. Ehlers.

        This API call returns meta and time series values of HT_TRENDMODE.
        Meta object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = HT_TRENDMODEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ichimoku(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ICHIMOKU to chart builder

        Ichimoku Kinkō Hyō(ICHIMOKU) is a group of technical indicators that shows trend direction, momentum,
        and support & resistance levels. Overall it tends to improve the accuracy of forecasts.

        This API call returns meta and time series values of HT_TRENDLINE.
        Meta object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param conversion_line_period: Takes values in the range from 1 to 800
        :param base_line_period: Takes values in the range from 1 to 800
        :param leading_span_b_period: Takes values in the range from 1 to 800
        :param lagging_span_period: Takes values in the range from 1 to 800
        :param include_ahead_span_period: Specifies if the span values ahead the current moment should be returned
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ICHIMOKUEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            conversion_line_period=conversion_line_period,
            base_line_period=base_line_period,
            leading_span_b_period=leading_span_b_period,
            lagging_span_period=lagging_span_period,
            include_ahead_span_period=include_ahead_span_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_kama(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of KAMA to chart builder

        Kaufman's Adaptive Moving Average(KAMA) is a type of Moving
        Average(MA) that incorporates market noise and volatility.

        This API call returns meta and time series values of KAMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = KAMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_keltner(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of KELTNER to chart builder

        Keltner Channels(KELTNER) is a volatility indicator used to spot trend changes and accelerations.

        This API call returns meta and time series values of KELTNER. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at least 1
        :param atr_time_period: Takes values in the range from 1 to 800
        :param multiplier: Multiplier is the number by which the range is shifted
        :param ma_type: Type of Moving Average to be used
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = KELTNEREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            atr_time_period=atr_time_period,
            multiplier=multiplier,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_kst(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of KST to chart builder

        Know Sure Thing(KST) calculates price momentum for four distinct price cycles(ROC).

        This API call returns meta and time series values of KST. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param roc_period_1:
        :param roc_period_2:
        :param roc_period_3:
        :param roc_period_4:
        :param signal_period:
        :param sma_period_1:
        :param sma_period_2:
        :param sma_period_3:
        :param sma_period_4:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = KSTEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            roc_period_1=roc_period_1,
            roc_period_2=roc_period_2,
            roc_period_3=roc_period_3,
            roc_period_4=roc_period_4,
            signal_period=signal_period,
            sma_period_1=sma_period_1,
            sma_period_2=sma_period_2,
            sma_period_3=sma_period_3,
            sma_period_4=sma_period_4,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_linearreg(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LINEARREG to chart builder

        Linear Regression(LINEARREG) is used to determine trend direction by a
        straight line.

        This API call returns meta and time series values of LINEARREG. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LINEARREGEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_linearregangle(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LINEARREGANGLE to chart builder

        Linear Regression Angle(LINEARREGANGLE) calculates the angle of the
        linear regression trendline.

        This API call returns meta and time series values of LINEARREGANGLE.
        Meta object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LINEARREGANGLEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_linearregintercept(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LINEARREGINTERCEPT to chart builder

        Linear Regression Intercept(LINEARREGINTERCEPT) calculates the
        intercept for the linear regression trendline for each data point.

        This API call returns meta and time series values of
        LINEARREGINTERCEPT. Meta object consists of general information about
        requested technical indicator. Time series is the array of objects
        ordered by time desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LINEARREGINTERCEPTEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_linearregslope(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LINEARREGSLOPE to chart builder

        Linear Regression Slope(LINEARREGSLOPE) calculates the slope for the
        linear regression trendline for each data point.

        This API call returns meta and time series values of LINEARREGSLOPE.
        Meta object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LINEARREGSLOPEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ln(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LN to chart builder

        Natural Logarithm to the base of constant e(LN) transforms all data
        points with natural logarithm.

        This API call returns meta and time series values of LN. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LNEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_log10(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of LOG10 to chart builder

        Logarithm to base 10(LOG10) transforms all data points with logarithm
        to base 10.

        This API call returns meta and time series values of LOG10. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = LOG10Endpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ma(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MA to chart builder

        Moving Average(MA) is used to smooth out price fluctuations and get
        rid of market noise.

        This API call returns meta and time series values of MA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_macd(
            self,
            exchange=None,
            country=None,
            series_type="close",
            fast_period="12",
            slow_period="26",
            signal_period="9",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MACD to chart builder

        Moving Average Convergence Divergence(MACD) is a trend following
        momentum indicator which works by subtracting the longer moving
        average from the shorter one. MACD has an unstable period ~ 100.

        This API call returns meta and time series values of MACD. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param fast_period: Number of periods for fast moving average. Must
        be at least 1
        :param slow_period: Number of periods for slow moving average. Must
        be at least 1
        :param signal_period: Number of periods to be plotted on MACD line.
        Must be at least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MACDEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_macd_slope(
            self,
            exchange=None,
            country=None,
            series_type="close",
            fast_period="12",
            slow_period="26",
            signal_period="9",
            time_period="9",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MACD_SLOPE to chart builder

        Moving Average Convergence Divergence Regression Slope(MACD_SLOPE) shows
        slopes of macd line, signal line, and histogram. A negative and rising slope
        shows improvement within a downtrend. A positive and falling slope shows
        deterioration within an uptrend. MACD has an unstable period of ~ 100.

        This API call returns meta and time series values of MACD SLOPE. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param fast_period: Number of periods for fast moving average. Must
        be at least 1
        :param slow_period: Number of periods for slow moving average. Must
        be at least 1
        :param signal_period: Number of periods to be plotted on MACD line.
        Must be at least 1
        :param time_period: Number of periods to average over. Takes values in the range from 1 to 800.
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MACDSlopeEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_macdext(
            self,
            exchange=None,
            country=None,
            series_type="close",
            fast_period="12",
            fast_ma_type="SMA",
            slow_period="26",
            slow_ma_type="SMA",
            signal_period="9",
            signal_ma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MACDEXT to chart builder

        Moving Average Convergence Divergence Extended(MACDEXT) gives greater
        control over MACD input parameters. MACDEXT has an unstable period ~
        100.

        This API call returns meta and time series values of MACDEXT. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param fast_period: Number of periods for fast moving average. Must
        be at least 1
        :param fast_ma_type:
        :param slow_period: Number of periods for slow moving average. Must
        be at least 1
        :param slow_ma_type:
        :param signal_period: Number of periods to be plotted on MACD line.
        Must be at least 1
        :param signal_ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MACDEXTEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            fast_period=fast_period,
            fast_ma_type=fast_ma_type,
            slow_period=slow_period,
            slow_ma_type=slow_ma_type,
            signal_period=signal_period,
            signal_ma_type=signal_ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_mama(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MAMA to chart builder

        MESA Adaptive Moving Average(MAMA) adapts to price fluctuations based
        on the rate of change of Hilbert Transform Discriminator. More about
        MAMA can be read here.

        This API call returns meta and time series values of MAMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param fast_limit:
        :param slow_limit:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MAMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            fast_limit=fast_limit,
            slow_limit=slow_limit,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_max(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MAX to chart builder

        Highest value over period(MAX).

        This API call returns meta and time series values of MAX. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MAXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_maxindex(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MAXINDEX to chart builder

        Index of highest value over period(MAXINDEX).

        This API call returns meta and time series values of MAXINDEX. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MAXINDEXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_mcginley_dynamic(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MCGINLEY_DYNAMIC to chart builder

        McGinley Dynamic(MCGINLEY_DYNAMIC) keeps all the benefits from the moving averages but adds an adjustment to market speed.

        This API call returns meta and time series values of MCGINLEY_DYNAMIC. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = McGinleyDynamicEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_medprice(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MEDPRICE to chart builder

        Median Price(MEDPRICE).

        This API call returns meta and time series values of MEDPRICE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MEDPRICEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_mfi(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MFI to chart builder

        Money Flow Index(MFI) is used to identify overbought and oversold levels in an asset. In some cases,
        it can be used to detect divergences, which might be a sign of upcoming trend changes.

        This API call returns "meta" and "time_series" values of MFI. "meta" object consist of general information
        about the requested technical indicator. "time_series" is the array of objects ordered by time
        descending updated in real-time.

        :param symbol: Name of instrument you want to request
            For preffered stocks use dot(.) delimiter. E.g. BRK.A or BRK.B will be correct
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MFIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_midpoint(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MIDPOINT to chart builder

        MidPoint over period(MIDPOINT) is calculated as: (highest value +
        lowest value) / 2.

        This API call returns meta and time series values of MIDPOINT. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MIDPOINTEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_midprice(
            self,
            exchange=None,
            country=None,
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MIDPRICE to chart builder

        Midpoint Price over period(MIDPRICE) is calculated as: (highest high +
        lowest low) / 2.

        This API call returns meta and time series values of MIDPRICE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MIDPRICEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_min(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MIN to chart builder

        Lowest value over period(MIN).

        This API call returns meta and time series values of MIN. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MINEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_minindex(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MININDEX to chart builder

        Index of lowest value over period(MININDEX).

        This API call returns meta and time series values of MININDEX. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MININDEXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_minmax(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MINMAX to chart builder

        Lowest and highest values over period(MINMAX).

        This API call returns meta and time series values of MINMAX. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MINMAXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_minmaxindex(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MINMAXINDEX to chart builder

        Indexes of lowest and highest values over period(MINMAXINDEX).

        This API call returns meta and time series values of MINMAXINDEX. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MINMAXINDEXEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_minus_di(
            self,
            exchange=None,
            country=None,
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MINUS_DI to chart builder

        Minus Directional Indicator(MINUS_DI) is a component of the Average
        Directional Index(ADX) and it measures the existence of downtrend.

        This API call returns meta and time series values of MINUS_DI. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MINUS_DIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_minus_dm(
            self,
            exchange=None,
            country=None,
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MINUS_DM to chart builder

        Minus Directional Movement(MINUS_DM) is calculated as: Previous Low -
        Low.

        This API call returns meta and time series values of MINUS_DM. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MINUS_DMEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_mom(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of MOM to chart builder

        Momentum(MOM) compares current price with the previous price N
        timeperiods ago.

        This API call returns meta and time series values of MOM. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = MOMEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_natr(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of NATR to chart builder

        Normalized Average True Range(NATR) is used to compare and analyze
        across different price levels due to its normalized quality, which
        might be more effective than the original ATR.

        This API call returns meta and time series values of NATR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = NATREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_obv(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of OBV to chart builder

        On Balance Volume(OBV) is a momentum indicator which uses volume flow
        to forecast upcoming price changes.

        This API call returns meta and time series values of OBV. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Name of instrument you want to request
        For preffered stocks use dot(.) delimiterE.g. BRK.A or BRK.B will be
        correct
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = OBVEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_plus_di(
            self,
            exchange=None,
            country=None,
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of PLUS_DI to chart builder

        Plus Directional Indicator(PLUS_DI) is a component of the Average
        Directional Index(ADX) and it measures the existence of uptrend.

        This API call returns meta and time series values of PLUS_DI. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = PLUS_DIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_plus_dm(
            self,
            exchange=None,
            country=None,
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of PLUS_DM to chart builder

        Plus Directional Movement(PLUS_DM) is calculated as: High - Previous
        High.

        This API call returns meta and time series values of PLUS_DM. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = PLUS_DMEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ppo(
            self,
            exchange=None,
            country=None,
            series_type="close",
            fast_period="10",
            slow_period="21",
            ma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of PPO to chart builder

        Percentage Price Oscillator(PPO) shows relationship between two Moving
        Averages(MA) as a percentage.

        This API call returns meta and time series values of PPO. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param fast_period: Number of periods for fast moving average. Must
        be at least 1
        :param slow_period: Number of periods for slow moving average. Must
        be at least 1
        :param ma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = PPOEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            fast_period=fast_period,
            slow_period=slow_period,
            ma_type=ma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_roc(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ROC to chart builder

        Rate of change(ROC) calculates rate of change between current price
        and price n timeperiods ago. Formula: ((price / prevPrice) - 1) * 100.

        This API call returns meta and time series values of ROC. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ROCEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_rocp(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ROCP to chart builder

        Rate of change percentage(ROCP) calculates rate of change in % between
        current price and price n timeperiods ago. Formula: (price -
        prevPrice) / prevPrice.

        This API call returns meta and time series values of ROCP. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ROCPEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_rocr(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ROCR to chart builder

        Rate of change ratio(ROCR) calculates ratio between current price and
        price n timeperiods ago. Formula: (price / prevPrice).

        This API call returns meta and time series values of ROCR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ROCREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_rocr100(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ROCR100 to chart builder

        Rate of change ratio 100 scale(ROCR100) calculates ratio with 100
        scale between current price and price n timeperiods ago. Formula:
        (price / prevPrice) * 100.

        This API call returns meta and time series values of ROCR100. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ROCR100Endpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_rsi(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of RSI to chart builder

        Relative Strength Index(RSI) is a momentum indicator which calculates
        the magnitude of a price changes to assess the overbought and oversold
        conditions in the price of an asset.

        This API call returns meta and time series values of RSI. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = RSIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_rvol(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of RVOL to chart builder

        Relative Volume Indicator(RVOL) shows how the current trading volume
        is compared to past volume over a given period.

        This API call returns meta and time series values of RVOL. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = RVOLEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_sar(
            self,
            acceleration="0.02",
            maximum="0.2",
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of SAR to chart builder

        Parabolic SAR(SAR) is used to identify and spot upcoming asset
        momentum.

        This API call returns meta and time series values of SAR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param acceleration:
        :param maximum:
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = SAREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            acceleration=acceleration,
            maximum=maximum,
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_sma(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of SMA to chart builder

        Simple Moving Average(SMA) is an arithmetic moving average calculated
        by adding latest closing prices and them dividing them by number of
        time periods.

        This API call returns meta and time series values of SMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = SMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_sqrt(
            self,
            exchange=None,
            country=None,
            series_type="close",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of SQRT to chart builder

        Square Root(SQRT) transform input data with square root.

        This API call returns meta and time series values of SQRT. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = SQRTEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_stddev(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of STDDEV to chart builder

        Standard Deviation(STDDEV) is used to measure volatility. Might be
        important when assessing risks.

        This API call returns meta and time series values of STDDEV. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param sd: Number of standard deviations. Must be at least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = STDDEVEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            sd=sd,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_stoch(
            self,
            exchange=None,
            country=None,
            fast_k_period="14",
            slow_k_period="1",
            slow_d_period="3",
            slow_kma_type="SMA",
            slow_dma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of STOCH to chart builder

        Stochastic Oscillator(STOCH) is used to decide if the price trend is
        strong.

        This API call returns meta and time series values of STOCH. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param fast_k_period:
        :param slow_k_period:
        :param slow_d_period:
        :param slow_kma_type:
        :param slow_dma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = STOCHEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            fast_k_period=fast_k_period,
            slow_k_period=slow_k_period,
            slow_d_period=slow_d_period,
            slow_kma_type=slow_kma_type,
            slow_dma_type=slow_dma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_stochf(
            self,
            exchange=None,
            country=None,
            fast_k_period="14",
            fast_d_period="3",
            fast_dma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of STOCHF to chart builder

        Stochastic Fast(STOCHF) is more sensitive to price changes, therefore
        it changes direction more quickly.

        This API call returns meta and time series values of STOCHF. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param fast_k_period:
        :param fast_d_period:
        :param fast_dma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = STOCHFEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            fast_k_period=fast_k_period,
            fast_d_period=fast_d_period,
            fast_dma_type=fast_dma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_stochrsi(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=14,
            fast_k_period="3",
            fast_d_period="3",
            fast_dma_type="SMA",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of STOCHRSI to chart builder

        Stochastic RSI(STOCHRSI) this indicator takes advantages of both
        indicators STOCH and RSI. It is used to determine level of overbought
        and oversold as well as current market trend of an asset.

        This API call returns meta and time series values of STOCHRSI. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param fast_k_period:
        :param fast_d_period:
        :param fast_dma_type:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = STOCHRSIEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            fast_k_period=fast_k_period,
            fast_d_period=fast_d_period,
            fast_dma_type=fast_dma_type,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_supertrend(
            self,
            exchange=None,
            country=None,
            multiplier=3,
            period=10,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of SuperTrend to chart builder

        SuperTrend Indicator(SUPERTREND) is mostly used on intraday timeframes to detect
        the price upward or downward direction in the trending market.

        This API call returns meta and time series values of SuperTrend. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param multiplier: Multiplier is the number by which the range is multiplied
        :param period: Period of the ATR indicator
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = SuperTrendEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            multiplier=multiplier,
            period=period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_t3ma(
            self,
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
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of T3MA to chart builder

        T3MA(T3MA).

        This API call returns meta and time series values of T3MA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param v_factor:
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = T3MAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            v_factor=v_factor,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_tema(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of TEMA to chart builder

        Triple Exponential Moving Average(TEMA) it smooths out price
        fluctuations, making it more trend detection more transparent without
        the lag.

        This API call returns meta and time series values of TEMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = TEMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_trange(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of TRANGE to chart builder

        True Range(TRANGE) usually is used as the base when calculating other
        indicators. TRANGE determines the normal trading range of an asset.

        This API call returns meta and time series values of TRANGE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = TRANGEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_trima(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of TRIMA to chart builder

        Triangular Moving Average(TRIMA) it smooths out price fluctuations,
        but places more weight on the prices in middle of the time period.

        This API call returns meta and time series values of TRIMA. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = TRIMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_tsf(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of TSF to chart builder

        Time Series Forecast(TSF) calculates trend based on last points of
        multiple regression trendlines.

        This API call returns meta and time series values of TSF. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = TSFEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_typprice(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of TYPPRICE to chart builder

        Typical Price(TYPPRICE).

        This API call returns meta and time series values of TYPPRICE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = TYPPRICEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_ultosc(
            self,
            exchange=None,
            country=None,
            time_period_1="7",
            time_period_2="14",
            time_period_3="28",
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of ULTOSC to chart builder

        Ultimate Oscillator(ULTOSC) takes into account three different time
        periods to enhance quality of overbought and oversold signals.

        This API call returns meta and time series values of ULTOSC. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period_1: Number of periods to average over. Must be at
        least 1
        :param time_period_2: Number of periods to average over. Must be at
        least 1
        :param time_period_3: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = ULTOSCEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period_1=time_period_1,
            time_period_2=time_period_2,
            time_period_3=time_period_3,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_var(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of VAR to chart builder

        Variance(VAR) calculates the spread between data points to determine
        how far are they from the mean.

        This API call returns meta and time series values of VAR. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
        calculated
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = VAREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_vwap(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of VWAP to chart builder

        Volume Weighted Average Price(VWAP) is commonly used as a trading benchmark
        that gives an average price at which the instrument has been trading during the day.

        This API call returns meta and time series values of VWAP. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = VWAPEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_wclprice(
            self,
            exchange=None,
            country=None,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of WCLPRICE to chart builder

        Weighted Close Price(WCLPRICE) usually is used as the base for other
        indicators for smoothness. Formula: (high + low + close * 2) / 4.

        This API call returns meta and time series values of WCLPRICE. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
                Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
                Country where instrument is traded
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
                Exchange for local exchange time2. UTC for datetime at
                universal UTC standard3. Timezone name according to IANA Time
                Zone Database. E.g. America/New_York, Asia/Singapore. Full
                list of timezones can be found here.Take note that IANA
                Timezone name is case-sensitive.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = WCLPRICEEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_willr(
            self,
            exchange=None,
            country=None,
            time_period=14,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of WILLR to chart builder

        Williams %R(WILLR) calculates overbought and oversold levels. It can
        also be used to find entry and exit signals.

        This API call returns meta and time series values of WILLR. Meta
        object consists of general information about requested technical
        indicator. Time series is the array of objects ordered by time
        desceding updated realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param time_period: Number of periods to average over. Must be at
        least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = WILLREndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)

    @force_use_kwargs
    @apply_context_defaults
    def with_wma(
            self,
            exchange=None,
            country=None,
            series_type="close",
            time_period=9,
            outputsize=30,
            start_date=None,
            end_date=None,
            dp=5,
            timezone="Exchange",
            prepost="false",
            mic_code=None,
    ):
        """
        Add request builder of WMA to chart builder

        Weighted Moving Average(WMA) it smooths out price fluctuations, it
        puts more weight on recent data points and less on past.

        This API call returns meta and time series values of WMA. Meta object
        consists of general information about requested technical indicator.
        Time series is the array of objects ordered by time desceding updated
        realtime.

        :param symbol: Instrument symbol, can be any stock, forex or
            cryptocurrency E.g. AAPL, EUR/USD, ETH/BTC, ...
        :param interval: Interval between two consecutive points in time series
        :param exchange: Only is applicable to stocks and cryptocurrencies
        otherwise is ignored
            Exchange where instrument is traded
        :param country: Only is applicable to stocks otherwise is ignored
            Country where instrument is traded
        :param series_type: Price type on which technical indicator is
            calculated
        :param time_period: Number of periods to average over. Must be at
            least 1
        :param outputsize: Number of last datapoints to retrieve
        :param start_date: Start date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param end_date: End date of selection, accepts "yyyy-MM-dd hh:mm:ss" and "yyyy-MM-dd" formats
        :param dp: Specifies number of decimal places for floating values
        :param timezone: Timezone at which output datetime will be displayed
            Exchange for local exchange time2. UTC for datetime at universal
            UTC standard3. Timezone name according to IANA Time Zone
            Database. E.g. America/New_York, Asia/Singapore. Full list of
            timezones can be found here.Take note that IANA Timezone name is
            case-sensitive.
        :param prepost: Available at the 1min, 5min, 15min, and 30min intervals for all US equities.
        :param mic_code: Mic code value for filter.

        :returns: chart builder
        :rtype: ChartEndpoint
        """
        ep = WMAEndpoint(
            ctx=self.ctx,
            symbol=self.ctx.defaults["symbol"],
            interval=self.ctx.defaults["interval"],
            exchange=exchange,
            country=country,
            series_type=series_type,
            time_period=time_period,
            outputsize=outputsize,
            start_date=start_date,
            end_date=end_date,
            dp=dp,
            timezone=timezone,
            prepost=prepost,
            mic_code=mic_code,
        )
        return self._with_endpoint(ep)
