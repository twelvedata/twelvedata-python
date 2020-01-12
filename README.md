<p align="center"><img src="https://res.cloudinary.com/dnz8pwg9r/image/upload/v1577895073/logo-python_xjrv79.png" width="400"></p>



# Twelve Data API

Official python library for Twelve Data API. This package supports all main features of the API:

* Get stock, forex and cryptocurrency OHLC time series.
* Get over 90+ technical indicators.
* Output data as: `json`, `csv`, `pandas`
* Full support for static and dynamic charts.

![chart example](https://github.com/twelvedata/twelvedata-python/blob/master/asset/chart-example.gif)

Free **API Key** is required. It might be requested [here](https://twelvedata.com/apikey)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Twelve Data API library (without optional dependencies):

```bash
pip install twelvedata
```

Or install with pandas support:

```bash
pip install twelvedata[pandas]
```

Or install with pandas, matplotlib and plotly support used for charting:

```
pip install twelvedata[pandas,matplotlib,plotly]
```

## Usage

* [Time series](#Time-series)
* [Technical Indicators](#Technical-indicators)
* [Charts](#Charts)

##### Supported parameters

| Parameter  | Description                                                  | Type   | Required |
| ---------- | :----------------------------------------------------------- | ------ | -------- |
| symbol     | stock ticker (e.g. AAPL, MSFT); <br />physical currency pair (e.g. EUR/USD, CNY/JPY);<br />digital currency pair (BTC/USD, XRP/ETH) | string | yes      |
| interval   | time frame: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month | string | yes      |
| apikey     | your personal API Key, if you don't have one - get it [here](https://twelvedata.com/apikey) | string | yes      |
| exchange   | if symbol is traded in multiple exchanges specify the desired one, valid for both stocks and cryptocurrencies | string | no       |
| country    | if symbol is traded in multiple countries specify the desired one, valid for stocks | string | no       |
| outputsize | number of data points to retrieve                            | int    | no       |
| timezone   | timezone at which output datetime will be displayed, supports: `UTC`, `Exchange` or according to IANA Time Zone Database | string | no       |
| start_date | start date and time of sampling period, accepts `yyyy-MM-dd` or `yyyy-MM-dd hh:mm:ss` format | string | no       |
| end_date   | end date and time of sampling period, accepts `yyyy-MM-dd` or `yyyy-MM-dd hh:mm:ss` format | string | no       |

### Time series

* `TDClient` requires `api_key` parameter. It accepts all common parameters.
* `TDClient.time_series()` accepts all common parameters. Time series may be converted to several formats:
  * `TDClient.time_series().as_json()` - will return JSON array
  * `TDClient.time_series().as_csv()` - will return CSV with header
  * `TDClient.time_series().as_pandas()` - will return pandas.DataFrame

```python
from twelvedata import TDClient
# Initialize client - api_key parameter is requiered
td = TDClient(apikey="YOUR_API_KEY_HERE")
# Construct the necessary time serie
ts = td.time_series(
    symbol="AAPL",
    interval="1min",
    outputsize=10,
    timezone="America/New_York",
)
# Returns pandas.DataFrame
ts.as_pandas()
```

### Technical indicators

This Python library supports all indicators implemented by Twelve Data. Full list of 90+ technical indicators   may be found in [API Documentation](https://twelvedata.com/docs).

* Technical indicators are part of `TDClient.time_series()` object.
* It has universal format `TDClient.time_series().with_{Technical Indicator Name}`, e.g. `.with_bbands()`, `.with_percent_b()`, `.with_macd()`
* Indicator object accepts all parameters according to its specification in [API Documentation](https://twelvedata.com/docs), e.g. `.with_bbands()` accepts: `series_type`, `time_period`, `sd`, `ma_type`. If parameter is not provided it will be set to default.
* Indicators may be used in arbitrary order and conjugated, e.g. `TDClient.time_series().with_aroon().with_adx().with_ema()`
* By default, technical indicator will output with OHLC values. If you do not need OHLC, specify `TDClient.time_series().without_ohlc()`

```python
from twelvedata import TDClient

td = TDClient(apikey="YOUR_API_KEY_HERE")
ts = td.time_series(
    symbol="ETH/BTC",
    exchange="Huobi",
    interval="5min",
    outputsize=22,
    timezone="America/New_York",
)
# Returns: OHLC, BBANDS(close, 20, 2, EMA), PLUS_DI(9), WMA(20), WMA(40)
ts.with_bbands(ma_type="EMA").with_plus_di().with_wma(time_period=20).with_wma(time_period=40).as_pandas()

# Returns: STOCH(14, 1, 3, SMA, SMA), TSF(close, 9)
ts.without_ohlc().with_stoch().with_tsf().as_json()
```

### Charts

* [Static](#Static)
* [Interactive](#Interactive)

Charts support OHLC, technical indicators and custom bars.

#### Static

Static charting is based on `matplotlib` library. Make sure you have installed it.

* Use `.as_pyplot_figure()`

```python
from twelvedata import TDClient

td = TDClient(apikey="YOUR_API_KEY_HERE")
ts = td.time_series(
    symbol="MSFT",
    outputsize=75,
    interval="1day",
)
# 1. Returns OHLCV chart
ts.as_pyplot_figure()

# 2. Returns OHLCV + BBANDS(close, 20, 2, SMA) + %B(close, 20, 2 SMA) + STOCH(14, 3, 3, SMA, SMA)
ts.with_bbands().with_percent_b().with_stoch(slow_k_period=3).as_pyplot_figure()
```

#### Interactive

Interactive charting is based on `plotly` library. Make sure you have installed it.

* Use `.as_plotly_figure()`

```python
from twelvedata import TDClient

td = TDClient(apikey="YOUR_API_KEY_HERE")
ts = td.time_series(
    symbol="DNR",
    outputsize=50,
    interval="1week",
)
# 1. Returns OHLCV chart
ts.as_plotly_figure()

# 2. Returns OHLCV + EMA(close, 7) + MAMA(close, 0.5, 0.05) + MOM(close, 9) + MACD(close, 12, 26, 9)
ts.with_ema(time_period=7).with_mama().with_mom().with_macd().as_plotly_figure()
```

## Support

Visit our official website [https://twelvedata.com](https://twelvedata.com) or reach out to the Twelve Data team at [info@twelvedata.com](mailto:info@twelvedata.com?subject=Python%20library%20question).

## Roadmap

- [ ] Save-load chart templates
- [ ] Auto-update charts
- [x] Custom plots coloring
- [x] Interactive charts (plotly)
- [x] Static charts (matplotlib)
- [x] Pandas support

## Contributing

1. Clone repo and create a new branch: `$ git checkout https://github.com/twelvedata/twelvedata -b name_for_new_branch`.
2. Make changes and test.
3. Submit Pull Request with comprehensive description of changes.

## License

This package is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
