# coding: utf-8

from .endpoints import *

VOL_CHART_HEIGHT = 0.15
CANDLE_WIDTH = 0.0002
BAR_WIDTH = 0.0002
COLOR_UP = "#26a69a"
COLOR_DOWN = "#ef5350"


class RenderContext(object):
    fig = None
    interval_minutes = 1
    fill_area = None
    colormap = {}
    postfix = ""


class ChartRender(object):
    def render(self, backend, df, **kwargs):
        getattr(self, "render_{}".format(backend))(df, **kwargs)

    def _slice(self, df):
        if getattr(self, "cols", None):
            df = df.loc[:, self.cols]
        return df

    def _label(self, ctx, col):
        return "{}{}".format(col, ctx.postfix)


class CandlestickRender(ChartRender):
    def __init__(self, opens, highs, lows, closes, volume=None):
        self.volume = volume
        self.ohlc = (opens, highs, lows, closes)

    def render_plotly(self, ctx, df, **kwargs):
        import plotly.graph_objects as go

        fig = ctx.fig
        (opens, highs, lows, closes) = self.ohlc

        data = [
            go.Candlestick(
                x=df.index,
                open=df[opens],
                high=df[highs],
                low=df[lows],
                close=df[closes],
                increasing=go.candlestick.Increasing(
                    line=go.candlestick.increasing.Line(color=COLOR_UP)
                ),
                decreasing=go.candlestick.Decreasing(
                    line=go.candlestick.decreasing.Line(color=COLOR_DOWN)
                ),
                name="Price",
            )
        ]

        if self.volume and self.volume in df:
            volume_colors = [
                COLOR_UP if i != 0 and df[closes][i] > df[opens][i] else COLOR_DOWN
                for i in range(len(df[closes]))
            ]

            # Visually separate the price chart from the volume chart
            ymin = min(
                df[opens].min(), df[highs].min(), df[lows].min(), df[closes].min()
            )
            ymax = max(
                df[opens].max(), df[highs].max(), df[lows].max(), df[closes].max()
            )
            fig.layout["yaxis"].range = [ymin - (ymax - ymin) * VOL_CHART_HEIGHT, ymax]

            data.append(
                go.Bar(
                    x=df.index,
                    y=df[self.volume],
                    marker=go.bar.Marker(color=volume_colors),
                    name="Volume",
                    yaxis="y666",
                )
            )

            y_scaler = 1.0 / VOL_CHART_HEIGHT

            fig.layout["yaxis666"] = go.layout.YAxis(
                range=[0, df[self.volume].max() * y_scaler],
                overlaying="y1",
                anchor="x1",
                showgrid=False,
                showticklabels=False,
            )

        return data

    def render_matplotlib(self, ctx, df, ax, **kwargs):
        import mplfinance as mpf
        import pandas as pd

        df.index = pd.to_datetime(df.index)
        if self.volume and self.volume in df:
            mc = mpf.make_marketcolors(up=COLOR_UP, down=COLOR_DOWN,
                                       edge='inherit',
                                       wick='black',
                                       ohlc='i',
                                       volume='in')
            s = mpf.make_mpf_style(marketcolors=mc)
            mpf.plot(df, type='candle', volume=True, style=s)
        else:
            mc = mpf.make_marketcolors(up=COLOR_UP, down=COLOR_DOWN,
                                       edge='inherit',
                                       wick='black',
                                       ohlc='i')
            s = mpf.make_mpf_style(marketcolors=mc)
            mpf.plot(df, type='candle', volume=False, style=s)


class LineRender(ChartRender):
    def __init__(self, *cols):
        self.cols = cols

    def render_plotly(self, ctx, df, **kwargs):
        import plotly.graph_objects as go

        df = self._slice(df)
        return [
            go.Scatter(
                x=df.index,
                y=df[col],
                name=self._label(ctx, col),
                line={"color": ctx.colormap.get(col)},
            )
            for col in df.columns
        ]

    def render_matplotlib(self, ctx, df, ax, **kwargs):
        kwargs.pop("candle_width", None)
        df = self._slice(df)
        for col in df.columns:
            df[col].plot(
                ax=ax,
                color=ctx.colormap.get(col),
                label=self._label(ctx, col),
                **kwargs
            )


class PointsRender(ChartRender):
    def __init__(self, *cols):
        self.cols = cols

    def render_plotly(self, ctx, df, **kwargs):
        import plotly.graph_objects as go

        df = self._slice(df)
        return [
            go.Scatter(
                x=df.index,
                y=df[col],
                name=self._label(ctx, col),
                mode="markers",
                marker={"color": ctx.colormap.get(col)},
            )
            for col in df.columns
        ]

    def render_matplotlib(self, ctx, df, ax, **kwargs):

        df = self._slice(df)
        for col in df.columns:
            tmp_df = df.loc[:, [col]].reset_index()
            tmp_df.plot.scatter(
                x=df.index.name,
                y=col,
                ax=ax,
                color=ctx.colormap.get(col),
                label=self._label(ctx, col),
                **kwargs
            )


class HistogramRender(ChartRender):
    def __init__(self, col):
        self.cols = (col,)

    def render_plotly(self, ctx, df, **kwargs):
        import plotly.graph_objects as go

        df = self._slice(df)
        return [
            go.Bar(
                x=df.index,
                y=df[col],
                name=self._label(ctx, col),
                marker={"color": ctx.colormap.get(col)},
            )
            for col in df.columns
        ]

    def render_matplotlib(self, ctx, df, ax, **kwargs):
        df = self._slice(df)
        col = self.cols[0]
        ax.bar(
            df.index,
            df[col],
            align="center",
            width=BAR_WIDTH * ctx.interval_minutes,
            color=ctx.colormap.get(col),
            label=self._label(ctx, col),
        )


class FillAreaRender(ChartRender):
    def _prepare_bound(self, df, bound):
        if isinstance(bound, (int, float)):
            bound = [bound] * len(df)
        elif bound in df:
            bound = df[bound]
        else:
            bound = None
        return bound

    def _extract_variables(self, df, fill_area):
        color = fill_area.get("color")
        opacity = fill_area.get("transparency")

        lower = fill_area.get("lower_bound")
        lower = self._prepare_bound(df, lower)

        upper = fill_area.get("upper_bound")
        upper = self._prepare_bound(df, upper)

        return (color, lower, upper, opacity)

    def render_plotly(self, ctx, df, **kwargs):
        import plotly.graph_objs as go

        if not ctx.fill_area:
            return ()

        color, lower, upper, opacity = self._extract_variables(df, ctx.fill_area)
        if not (color and lower is not None and upper is not None and opacity):
            return ()

        trace0 = go.Scatter(
            x=df.index,
            y=lower,
            fill=None,
            mode="lines",
            opacity=opacity,
            showlegend=False,
            line={"color": color, "width": 0},
        )

        trace1 = go.Scatter(
            x=df.index,
            y=upper,
            fill="tonexty",
            mode="lines",
            opacity=opacity,
            showlegend=False,
            line={"color": color, "width": 0},
        )

        return (trace0, trace1)

    def render_matplotlib(self, ctx, df, ax, **kwargs):
        import matplotlib.pyplot as plt

        if not ctx.fill_area:
            return

        color, lower, upper, alpha = self._extract_variables(df, ctx.fill_area)
        if not (color and lower is not None and upper is not None and alpha):
            return

        ax.fill_between(df.index, lower, upper, facecolor=color, alpha=alpha)


LR = LineRender()

FAR = FillAreaRender()


RENDER_BY_NAME = {
    "candle": CandlestickRender,
    "points": PointsRender,
    "histogram": HistogramRender,
    "line": LineRender,
}


RENDERS_MAPPING = {
    ADOSCEndpoint: [LR],
    ADEndpoint: [LR],
    ADXREndpoint: [LR],
    ADXEndpoint: [LR],
    APOEndpoint: [LR],
    AROONOSCEndpoint: [LR],
    AROONEndpoint: [LR],
    ATREndpoint: [LR],
    AVGPRICEEndpoint: [LR],
    BBANDSEndpoint: [LR, FAR],
    BETAEndpoint: [LR],
    BOPEndpoint: [LR],
    CCIEndpoint: [LR, FAR],
    CEILEndpoint: [LR],
    CMOEndpoint: [LR],
    COPPOCKEndpoint: [LR],
    DEMAEndpoint: [LR],
    DXEndpoint: [LR],
    EMAEndpoint: [LR],
    EXPEndpoint: [LR],
    FLOOREndpoint: [LR],
    HEIKINASHICANDLESEndpoint: [
        CandlestickRender("heikinopens", "heikinhighs", "heikinlows", "heikincloses")
    ],
    HLC3Endpoint: [LR],
    HT_DCPERIODEndpoint: [LR],
    HT_DCPHASEEndpoint: [LR],
    HT_PHASOREndpoint: [LR],
    HT_SINEEndpoint: [LR],
    HT_TRENDLINEEndpoint: [LR],
    HT_TRENDMODEEndpoint: [LR],
    ICHIMOKUEndpoint: [LR],
    KAMAEndpoint: [LR],
    KELTNEREndpoint: [LR],
    KSTEndpoint: [LR],
    LINEARREGANGLEEndpoint: [LR],
    LINEARREGINTERCEPTEndpoint: [LR],
    LINEARREGEndpoint: [LR],
    LINEARREGSLOPEEndpoint: [LR],
    LNEndpoint: [LR],
    LOG10Endpoint: [LR],
    MACDEndpoint: [LineRender("macd", "macd_signal"), HistogramRender("macd_hist"), ],
    MACDSlopeEndpoint: [LR],
    MACDEXTEndpoint: [LR],
    MAMAEndpoint: [LR],
    MAEndpoint: [LR],
    MAXINDEXEndpoint: [LR],
    MAXEndpoint: [LR],
    McGinleyDynamicEndpoint: [LR],
    MEDPRICEEndpoint: [LR],
    MFIEndpoint: [LR],
    MIDPOINTEndpoint: [LR],
    MIDPRICEEndpoint: [LR],
    MININDEXEndpoint: [LR],
    MINMAXINDEXEndpoint: [LR],
    MINMAXEndpoint: [LR],
    MINEndpoint: [LR],
    MINUS_DIEndpoint: [LR],
    MINUS_DMEndpoint: [LR],
    MOMEndpoint: [LR],
    NATREndpoint: [LR],
    OBVEndpoint: [LR],
    PLUS_DIEndpoint: [LR],
    PLUS_DMEndpoint: [LR],
    PPOEndpoint: [LR],
    PercentBEndpoint: [LR, FAR],
    PivotPointsHLEndpoint: [PointsRender("pivot_point_h", "pivot_point_l")],
    ROCPEndpoint: [LR],
    ROCR100Endpoint: [LR],
    ROCREndpoint: [LR],
    ROCEndpoint: [LR],
    RSIEndpoint: [LR, FAR],
    RVOLEndpoint: [LR],
    SAREndpoint: [PointsRender("sar")],
    SMAEndpoint: [LR],
    SQRTEndpoint: [LR],
    STDDEVEndpoint: [LR],
    STOCHFEndpoint: [LR, FAR],
    STOCHRSIEndpoint: [LR, FAR],
    STOCHEndpoint: [LR, FAR],
    SuperTrendEndpoint: [LR],
    T3MAEndpoint: [LR],
    TEMAEndpoint: [LR],
    TRANGEEndpoint: [LR],
    TRIMAEndpoint: [LR],
    TSFEndpoint: [LR],
    TYPPRICEEndpoint: [LR],
    TimeSeriesEndpoint: [CandlestickRender("open", "high", "low", "close", "volume")],
    ULTOSCEndpoint: [LR],
    VAREndpoint: [LR],
    VWAPEndpoint: [LR],
    WCLPRICEEndpoint: [LR],
    WILLREndpoint: [LR, FAR],
    WMAEndpoint: [LR],
}
