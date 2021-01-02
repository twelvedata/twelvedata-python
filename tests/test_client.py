#!/usr/bin/env python
# coding: utf-8

import json
import pytest
from requests import Response
from unittest.mock import patch, MagicMock, PropertyMock

from matplotlib import pyplot as plt
from twelvedata import TDClient
from twelvedata.http_client import DefaultHttpClient
from twelvedata.exceptions import (
    BadRequestError,
    InternalServerError,
    InvalidApiKeyError,
    TwelveDataError,
)


_cache = {}


API_URL = 'https://api.twelvedata.com'


class CachedHttpClient(DefaultHttpClient, object):
    def get(self, *args, **kwargs):
        global _cache

        h = "{}{}".format(args, kwargs)

        if h in _cache:
            return _cache[h]
        else:
            resp = super(CachedHttpClient, self).get(*args, **kwargs)
            _cache[h] = resp
            return resp


def _fake_resp(status_code):
    resp = Response()
    resp.status_code = status_code
    return resp


def _fake_json_resp(json_content):
    resp = MagicMock(spec=Response)
    type(resp).ok = PropertyMock(return_value=True)
    resp.json = MagicMock(return_value=json_content)
    type(resp).headers = PropertyMock(return_value={})
    resp.status_code = 200
    return resp


def _init_client():
    return TDClient(
        "demo",
        http_client=CachedHttpClient(API_URL),
    )


def _init_ts():
    td = _init_client()
    return td.time_series(symbol="AAPL", interval="1min", outputsize=1)


def _init_batch_ts(symbols):
    td = _init_client()
    return td.time_series(symbol=symbols, interval="1min", outputsize=1)


def test_get_stocks_list():
    td = _init_client()
    td.get_stocks_list(exchange='NASDAQ').as_json()
    td.get_stocks_list(exchange='NASDAQ').as_csv()


def test_get_stock_exchanges_list():
    td = _init_client()
    td.get_stock_exchanges_list().as_json()
    td.get_stock_exchanges_list().as_csv()


def test_get_forex_pairs_list():
    td = _init_client()
    td.get_forex_pairs_list().as_json()
    td.get_forex_pairs_list().as_csv()


def test_get_cryptocurrencies_list():
    td = _init_client()
    td.get_cryptocurrencies_list().as_json()
    td.get_cryptocurrencies_list().as_csv()


def test_get_etf_list():
    td = _init_client()
    td.get_etf_list().as_json()
    td.get_etf_list().as_csv()


def test_get_indices_list():
    td = _init_client()
    td.get_indices_list().as_json()
    td.get_indices_list().as_csv()


def test_get_technical_indicators_list():
    td = _init_client()
    td.get_technical_indicators_list().as_json()


def test_get_exchanges_list():
    td = _init_client()
    td.get_exchanges_list().as_json()
    td.get_exchanges_list().as_csv()


def test_symbol_search():
    td = _init_client()
    td.symbol_search().as_json()


def test_earliest_timestamp():
    td = _init_client()
    td.get_earliest_timestamp(symbol="AAPL", interval="1day").as_json()


def test_time_series():
    ts = _init_ts()
    ts.as_json()
    ts.as_csv()
    ts.as_pandas()
    ts.as_plotly_figure()
    plt.close()


def test_time_series_get_ad():
    ts = _init_ts()
    ts.with_ad().as_json()
    ts.with_ad().as_csv()
    ts.with_ad().as_pandas()
    ts.with_ad().as_plotly_figure()
    plt.close()


def test_time_series_get_adosc():
    ts = _init_ts()
    ts.with_adosc().as_json()
    ts.with_adosc().as_csv()
    ts.with_adosc().as_pandas()
    ts.with_adosc().as_plotly_figure()
    plt.close()


def test_time_series_get_adx():
    ts = _init_ts()
    ts.with_adx().as_json()
    ts.with_adx().as_csv()
    ts.with_adx().as_pandas()
    ts.with_adx().as_plotly_figure()
    plt.close()


def test_time_series_get_adxr():
    ts = _init_ts()
    ts.with_adxr().as_json()
    ts.with_adxr().as_csv()
    ts.with_adxr().as_pandas()
    ts.with_adxr().as_plotly_figure()
    plt.close()


def test_time_series_get_apo():
    ts = _init_ts()
    ts.with_apo().as_json()
    ts.with_apo().as_csv()
    ts.with_apo().as_pandas()
    ts.with_apo().as_plotly_figure()
    plt.close()


def test_time_series_get_aroon():
    ts = _init_ts()
    ts.with_aroon().as_json()
    ts.with_aroon().as_csv()
    ts.with_aroon().as_pandas()
    ts.with_aroon().as_plotly_figure()
    plt.close()


def test_time_series_get_aroonosc():
    ts = _init_ts()
    ts.with_aroonosc().as_json()
    ts.with_aroonosc().as_csv()
    ts.with_aroonosc().as_pandas()
    ts.with_aroonosc().as_plotly_figure()
    plt.close()


def test_time_series_get_atr():
    ts = _init_ts()
    ts.with_atr().as_json()
    ts.with_atr().as_csv()
    ts.with_atr().as_pandas()
    ts.with_atr().as_plotly_figure()
    plt.close()


def test_time_series_get_avgprice():
    ts = _init_ts()
    ts.with_avgprice().as_json()
    ts.with_avgprice().as_csv()
    ts.with_avgprice().as_pandas()
    ts.with_avgprice().as_plotly_figure()
    plt.close()


def test_time_series_get_bbands():
    ts = _init_ts()
    ts.with_bbands().as_json()
    ts.with_bbands().as_csv()
    ts.with_bbands().as_pandas()
    ts.with_bbands().as_plotly_figure()
    plt.close()


def test_time_series_get_percent_b():
    ts = _init_ts()
    ts.with_percent_b().as_json()
    ts.with_percent_b().as_csv()
    ts.with_percent_b().as_pandas()
    ts.with_percent_b().as_plotly_figure()
    plt.close()


def test_time_series_get_bop():
    ts = _init_ts()
    ts.with_bop().as_json()
    ts.with_bop().as_csv()
    ts.with_bop().as_pandas()
    ts.with_bop().as_plotly_figure()
    plt.close()


def test_time_series_get_cci():
    ts = _init_ts()
    ts.with_cci().as_json()
    ts.with_cci().as_csv()
    ts.with_cci().as_pandas()
    ts.with_cci().as_plotly_figure()
    plt.close()


def test_time_series_get_ceil():
    ts = _init_ts()
    ts.with_ceil().as_json()
    ts.with_ceil().as_csv()
    ts.with_ceil().as_pandas()
    ts.with_ceil().as_plotly_figure()
    plt.close()


def test_time_series_get_cmo():
    ts = _init_ts()
    ts.with_cmo().as_json()
    ts.with_cmo().as_csv()
    ts.with_cmo().as_pandas()
    ts.with_cmo().as_plotly_figure()
    plt.close()


def test_time_series_get_coppock():
    ts = _init_ts()
    ts.with_coppock().as_json()
    ts.with_coppock().as_csv()
    ts.with_coppock().as_pandas()
    ts.with_coppock().as_plotly_figure()
    plt.close()


def test_time_series_get_dema():
    ts = _init_ts()
    ts.with_dema().as_json()
    ts.with_dema().as_csv()
    ts.with_dema().as_pandas()
    ts.with_dema().as_plotly_figure()
    plt.close()


def test_time_series_get_dx():
    ts = _init_ts()
    ts.with_dx().as_json()
    ts.with_dx().as_csv()
    ts.with_dx().as_pandas()
    ts.with_dx().as_plotly_figure()
    plt.close()


def test_time_series_get_ema():
    ts = _init_ts()
    ts.with_ema().as_json()
    ts.with_ema().as_csv()
    ts.with_ema().as_pandas()
    ts.with_ema().as_plotly_figure()
    plt.close()


def test_time_series_get_exp():
    ts = _init_ts()
    ts.with_exp().as_json()
    ts.with_exp().as_csv()
    ts.with_exp().as_pandas()
    ts.with_exp().as_plotly_figure()
    plt.close()


def test_time_series_get_floor():
    ts = _init_ts()
    ts.with_floor().as_json()
    ts.with_floor().as_csv()
    ts.with_floor().as_pandas()
    ts.with_floor().as_plotly_figure()
    plt.close()


def test_time_series_get_heikinashicandles():
    ts = _init_ts()
    ts.with_heikinashicandles().as_json()
    ts.with_heikinashicandles().as_csv()
    ts.with_heikinashicandles().as_pandas()
    ts.with_heikinashicandles().as_plotly_figure()
    plt.close()


def test_time_series_get_hlc3():
    ts = _init_ts()
    ts.with_hlc3().as_json()
    ts.with_hlc3().as_csv()
    ts.with_hlc3().as_pandas()
    ts.with_hlc3().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_dcperiod():
    ts = _init_ts()
    ts.with_ht_dcperiod().as_json()
    ts.with_ht_dcperiod().as_csv()
    ts.with_ht_dcperiod().as_pandas()
    ts.with_ht_dcperiod().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_dcphase():
    ts = _init_ts()
    ts.with_ht_dcphase().as_json()
    ts.with_ht_dcphase().as_csv()
    ts.with_ht_dcphase().as_pandas()
    ts.with_ht_dcphase().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_phasor():
    ts = _init_ts()
    ts.with_ht_phasor().as_json()
    ts.with_ht_phasor().as_csv()
    ts.with_ht_phasor().as_pandas()
    ts.with_ht_phasor().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_sine():
    ts = _init_ts()
    ts.with_ht_sine().as_json()
    ts.with_ht_sine().as_csv()
    ts.with_ht_sine().as_pandas()
    ts.with_ht_sine().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_trendline():
    ts = _init_ts()
    ts.with_ht_trendline().as_json()
    ts.with_ht_trendline().as_csv()
    ts.with_ht_trendline().as_pandas()
    ts.with_ht_trendline().as_plotly_figure()
    plt.close()


def test_time_series_get_ht_trendmode():
    ts = _init_ts()
    ts.with_ht_trendmode().as_json()
    ts.with_ht_trendmode().as_csv()
    ts.with_ht_trendmode().as_pandas()
    ts.with_ht_trendmode().as_plotly_figure()
    plt.close()


def test_time_series_get_ichimoku():
    ts = _init_ts()
    ts.with_ichimoku().as_json()
    ts.with_ichimoku().as_csv()
    ts.with_ichimoku().as_pandas()
    ts.with_ichimoku().as_plotly_figure()
    plt.close()


def test_time_series_get_kama():
    ts = _init_ts()
    ts.with_kama().as_json()
    ts.with_kama().as_csv()
    ts.with_kama().as_pandas()
    ts.with_kama().as_plotly_figure()
    plt.close()


def test_time_series_get_keltner():
    ts = _init_ts()
    ts.with_keltner().as_json()
    ts.with_keltner().as_csv()
    ts.with_keltner().as_pandas()
    ts.with_keltner().as_plotly_figure()
    plt.close()


def test_time_series_get_kst():
    ts = _init_ts()
    ts.with_kst().as_json()
    ts.with_kst().as_csv()
    ts.with_kst().as_pandas()
    ts.with_kst().as_plotly_figure()
    plt.close()


def test_time_series_get_linearreg():
    ts = _init_ts()
    ts.with_linearreg().as_json()
    ts.with_linearreg().as_csv()
    ts.with_linearreg().as_pandas()
    ts.with_linearreg().as_plotly_figure()
    plt.close()


def test_time_series_get_linearregangle():
    ts = _init_ts()
    ts.with_linearregangle().as_json()
    ts.with_linearregangle().as_csv()
    ts.with_linearregangle().as_pandas()
    ts.with_linearregangle().as_plotly_figure()
    plt.close()


def test_time_series_get_linearregintercept():
    ts = _init_ts()
    ts.with_linearregintercept().as_json()
    ts.with_linearregintercept().as_csv()
    ts.with_linearregintercept().as_pandas()
    ts.with_linearregintercept().as_plotly_figure()
    plt.close()


def test_time_series_get_linearregslope():
    ts = _init_ts()
    ts.with_linearregslope().as_json()
    ts.with_linearregslope().as_csv()
    ts.with_linearregslope().as_pandas()
    ts.with_linearregslope().as_plotly_figure()
    plt.close()


def test_time_series_get_ln():
    ts = _init_ts()
    ts.with_ln().as_json()
    ts.with_ln().as_csv()
    ts.with_ln().as_pandas()
    ts.with_ln().as_plotly_figure()
    plt.close()


def test_time_series_get_log10():
    ts = _init_ts()
    ts.with_log10().as_json()
    ts.with_log10().as_csv()
    ts.with_log10().as_pandas()
    ts.with_log10().as_plotly_figure()
    plt.close()


def test_time_series_get_ma():
    ts = _init_ts()
    ts.with_ma().as_json()
    ts.with_ma().as_csv()
    ts.with_ma().as_pandas()
    ts.with_ma().as_plotly_figure()
    plt.close()


def test_time_series_get_macd():
    ts = _init_ts()
    ts.with_macd().as_json()
    ts.with_macd().as_csv()
    ts.with_macd().as_pandas()
    ts.with_macd().as_plotly_figure()
    plt.close()


def test_time_series_get_macdext():
    ts = _init_ts()
    ts.with_macdext().as_json()
    ts.with_macdext().as_csv()
    ts.with_macdext().as_pandas()
    ts.with_macdext().as_plotly_figure()
    plt.close()


def test_time_series_get_mama():
    ts = _init_ts()
    ts.with_mama().as_json()
    ts.with_mama().as_csv()
    ts.with_mama().as_pandas()
    ts.with_mama().as_plotly_figure()
    plt.close()


def test_time_series_get_max():
    ts = _init_ts()
    ts.with_max().as_json()
    ts.with_max().as_csv()
    ts.with_max().as_pandas()
    ts.with_max().as_plotly_figure()
    plt.close()


def test_time_series_get_maxindex():
    ts = _init_ts()
    ts.with_maxindex().as_json()
    ts.with_maxindex().as_csv()
    ts.with_maxindex().as_pandas()
    ts.with_maxindex().as_plotly_figure()
    plt.close()


def test_time_series_get_mcginley_dynamic():
    ts = _init_ts()
    ts.with_mcginley_dynamic().as_json()
    ts.with_mcginley_dynamic().as_csv()
    ts.with_mcginley_dynamic().as_pandas()
    ts.with_mcginley_dynamic().as_plotly_figure()
    plt.close()


def test_time_series_get_medprice():
    ts = _init_ts()
    ts.with_medprice().as_json()
    ts.with_medprice().as_csv()
    ts.with_medprice().as_pandas()
    ts.with_medprice().as_plotly_figure()
    plt.close()


def test_time_series_get_mfi():
    ts = _init_ts()
    ts.with_mfi().as_json()
    ts.with_mfi().as_csv()
    ts.with_mfi().as_pandas()
    ts.with_mfi().as_plotly_figure()
    plt.close()


def test_time_series_get_midpoint():
    ts = _init_ts()
    ts.with_midpoint().as_json()
    ts.with_midpoint().as_csv()
    ts.with_midpoint().as_pandas()
    ts.with_midpoint().as_plotly_figure()
    plt.close()


def test_time_series_get_midprice():
    ts = _init_ts()
    ts.with_midprice().as_json()
    ts.with_midprice().as_csv()
    ts.with_midprice().as_pandas()
    ts.with_midprice().as_plotly_figure()
    plt.close()


def test_time_series_get_min():
    ts = _init_ts()
    ts.with_min().as_json()
    ts.with_min().as_csv()
    ts.with_min().as_pandas()
    ts.with_min().as_plotly_figure()
    plt.close()


def test_time_series_get_minindex():
    ts = _init_ts()
    ts.with_minindex().as_json()
    ts.with_minindex().as_csv()
    ts.with_minindex().as_pandas()
    ts.with_minindex().as_plotly_figure()
    plt.close()


def test_time_series_get_minmax():
    ts = _init_ts()
    ts.with_minmax().as_json()
    ts.with_minmax().as_csv()
    ts.with_minmax().as_pandas()
    ts.with_minmax().as_plotly_figure()
    plt.close()


def test_time_series_get_minmaxindex():
    ts = _init_ts()
    ts.with_minmaxindex().as_json()
    ts.with_minmaxindex().as_csv()
    ts.with_minmaxindex().as_pandas()
    ts.with_minmaxindex().as_plotly_figure()
    plt.close()


def test_time_series_get_minus_di():
    ts = _init_ts()
    ts.with_minus_di().as_json()
    ts.with_minus_di().as_csv()
    ts.with_minus_di().as_pandas()
    ts.with_minus_di().as_plotly_figure()
    plt.close()


def test_time_series_get_minus_dm():
    ts = _init_ts()
    ts.with_minus_dm().as_json()
    ts.with_minus_dm().as_csv()
    ts.with_minus_dm().as_pandas()
    ts.with_minus_dm().as_plotly_figure()
    plt.close()


def test_time_series_get_mom():
    ts = _init_ts()
    ts.with_mom().as_json()
    ts.with_mom().as_csv()
    ts.with_mom().as_pandas()
    ts.with_mom().as_plotly_figure()
    plt.close()


def test_time_series_get_natr():
    ts = _init_ts()
    ts.with_natr().as_json()
    ts.with_natr().as_csv()
    ts.with_natr().as_pandas()
    ts.with_natr().as_plotly_figure()
    plt.close()


def test_time_series_get_obv():
    ts = _init_ts()
    ts.with_obv().as_json()
    ts.with_obv().as_csv()
    ts.with_obv().as_pandas()
    ts.with_obv().as_plotly_figure()
    plt.close()


def test_time_series_get_plus_di():
    ts = _init_ts()
    ts.with_plus_di().as_json()
    ts.with_plus_di().as_csv()
    ts.with_plus_di().as_pandas()
    ts.with_plus_di().as_plotly_figure()
    plt.close()


def test_time_series_get_plus_dm():
    ts = _init_ts()
    ts.with_plus_dm().as_json()
    ts.with_plus_dm().as_csv()
    ts.with_plus_dm().as_pandas()
    ts.with_plus_dm().as_plotly_figure()
    plt.close()


def test_time_series_get_ppo():
    ts = _init_ts()
    ts.with_ppo().as_json()
    ts.with_ppo().as_csv()
    ts.with_ppo().as_pandas()
    ts.with_ppo().as_plotly_figure()
    plt.close()


def test_time_series_get_roc():
    ts = _init_ts()
    ts.with_roc().as_json()
    ts.with_roc().as_csv()
    ts.with_roc().as_pandas()
    ts.with_roc().as_plotly_figure()
    plt.close()


def test_time_series_get_rocp():
    ts = _init_ts()
    ts.with_rocp().as_json()
    ts.with_rocp().as_csv()
    ts.with_rocp().as_pandas()
    ts.with_rocp().as_plotly_figure()
    plt.close()


def test_time_series_get_rocr():
    ts = _init_ts()
    ts.with_rocr().as_json()
    ts.with_rocr().as_csv()
    ts.with_rocr().as_pandas()
    ts.with_rocr().as_plotly_figure()
    plt.close()


def test_time_series_get_rocr100():
    ts = _init_ts()
    ts.with_rocr100().as_json()
    ts.with_rocr100().as_csv()
    ts.with_rocr100().as_pandas()
    ts.with_rocr100().as_plotly_figure()
    plt.close()


def test_time_series_get_rsi():
    ts = _init_ts()
    ts.with_rsi().as_json()
    ts.with_rsi().as_csv()
    ts.with_rsi().as_pandas()
    ts.with_rsi().as_plotly_figure()
    plt.close()


def test_time_series_get_sar():
    ts = _init_ts()
    ts.with_sar().as_json()
    ts.with_sar().as_csv()
    ts.with_sar().as_pandas()
    ts.with_sar().as_plotly_figure()
    plt.close()


def test_time_series_get_sma():
    ts = _init_ts()
    ts.with_sma().as_json()
    ts.with_sma().as_csv()
    ts.with_sma().as_pandas()
    ts.with_sma().as_plotly_figure()
    plt.close()


def test_time_series_get_sqrt():
    ts = _init_ts()
    ts.with_sqrt().as_json()
    ts.with_sqrt().as_csv()
    ts.with_sqrt().as_pandas()
    ts.with_sqrt().as_plotly_figure()
    plt.close()


def test_time_series_get_stddev():
    ts = _init_ts()
    ts.with_stddev().as_json()
    ts.with_stddev().as_csv()
    ts.with_stddev().as_pandas()
    ts.with_stddev().as_plotly_figure()
    plt.close()


def test_time_series_get_stoch():
    ts = _init_ts()
    ts.with_stoch().as_json()
    ts.with_stoch().as_csv()
    ts.with_stoch().as_pandas()
    ts.with_stoch().as_plotly_figure()
    plt.close()


def test_time_series_get_stochf():
    ts = _init_ts()
    ts.with_stochf().as_json()
    ts.with_stochf().as_csv()
    ts.with_stochf().as_pandas()
    ts.with_stochf().as_plotly_figure()
    plt.close()


def test_time_series_get_stochrsi():
    ts = _init_ts()
    ts.with_stochrsi().as_json()
    ts.with_stochrsi().as_csv()
    ts.with_stochrsi().as_pandas()
    ts.with_stochrsi().as_plotly_figure()
    plt.close()


def test_time_series_get_supertrend():
    ts = _init_ts()
    ts.with_supertrend().as_json()
    ts.with_supertrend().as_csv()
    ts.with_supertrend().as_pandas()
    ts.with_supertrend().as_plotly_figure()
    plt.close()


def test_time_series_get_t3ma():
    ts = _init_ts()
    ts.with_t3ma().as_json()
    ts.with_t3ma().as_csv()
    ts.with_t3ma().as_pandas()
    ts.with_t3ma().as_plotly_figure()
    plt.close()


def test_time_series_get_tema():
    ts = _init_ts()
    ts.with_tema().as_json()
    ts.with_tema().as_csv()
    ts.with_tema().as_pandas()
    ts.with_tema().as_plotly_figure()
    plt.close()


def test_time_series_get_trange():
    ts = _init_ts()
    ts.with_trange().as_json()
    ts.with_trange().as_csv()
    ts.with_trange().as_pandas()
    ts.with_trange().as_plotly_figure()
    plt.close()


def test_time_series_get_trima():
    ts = _init_ts()
    ts.with_trima().as_json()
    ts.with_trima().as_csv()
    ts.with_trima().as_pandas()
    ts.with_trima().as_plotly_figure()
    plt.close()


def test_time_series_get_tsf():
    ts = _init_ts()
    ts.with_tsf().as_json()
    ts.with_tsf().as_csv()
    ts.with_tsf().as_pandas()
    ts.with_tsf().as_plotly_figure()
    plt.close()


def test_time_series_get_typprice():
    ts = _init_ts()
    ts.with_typprice().as_json()
    ts.with_typprice().as_csv()
    ts.with_typprice().as_pandas()
    ts.with_typprice().as_plotly_figure()
    plt.close()


def test_time_series_get_ultosc():
    ts = _init_ts()
    ts.with_ultosc().as_json()
    ts.with_ultosc().as_csv()
    ts.with_ultosc().as_pandas()
    ts.with_ultosc().as_plotly_figure()
    plt.close()


def test_time_series_get_var():
    ts = _init_ts()
    ts.with_var().as_json()
    ts.with_var().as_csv()
    ts.with_var().as_pandas()
    ts.with_var().as_plotly_figure()
    plt.close()


def test_time_series_get_vwap():
    ts = _init_ts()
    ts.with_vwap().as_json()
    ts.with_vwap().as_csv()
    ts.with_vwap().as_pandas()
    ts.with_vwap().as_plotly_figure()
    plt.close()


def test_time_series_get_wclprice():
    ts = _init_ts()
    ts.with_wclprice().as_json()
    ts.with_wclprice().as_csv()
    ts.with_wclprice().as_pandas()
    ts.with_wclprice().as_plotly_figure()
    plt.close()


def test_time_series_get_willr():
    ts = _init_ts()
    ts.with_willr().as_json()
    ts.with_willr().as_csv()
    ts.with_willr().as_pandas()
    ts.with_willr().as_plotly_figure()
    plt.close()


def test_time_series_get_wma():
    ts = _init_ts()
    ts.with_wma().as_json()
    ts.with_wma().as_csv()
    ts.with_wma().as_pandas()
    ts.with_wma().as_plotly_figure()
    plt.close()


def _init_chart():
    td = _init_client()
    return (
        td.time_series(symbol="AAPL", interval="1min")
        .with_ad()
        .with_adosc()
        .with_adx()
        .with_adxr()
        .with_apo()
        .with_aroon()
        .with_aroonosc()
        .with_atr()
        .with_avgprice()
        .with_bbands()
        .with_percent_b()
        .with_bop()
        .with_cci()
        .with_ceil()
        .with_cmo()
        .with_coppock()
        .with_ceil()
        .with_dema()
        .with_dx()
        .with_ema()
        .with_exp()
        .with_floor()
        .with_heikinashicandles()
        .with_hlc3()
        .with_ht_dcperiod()
        .with_ht_dcphase()
        .with_ht_phasor()
        .with_ht_sine()
        .with_ht_trendline()
        .with_ht_trendmode()
        .with_ichimoku()
        .with_kama()
        .with_keltner()
        .with_kst()
        .with_linearreg()
        .with_linearregangle()
        .with_linearregintercept()
        .with_linearregslope()
        .with_ln()
        .with_log10()
        .with_ma()
        .with_macd()
        .with_macdext()
        .with_mama()
        .with_max()
        .with_maxindex()
        .with_mcginley_dynamic()
        .with_medprice()
        .with_midpoint()
        .with_midprice()
        .with_min()
        .with_minindex()
        .with_minmax()
        .with_minmaxindex()
        .with_minus_di()
        .with_minus_dm()
        .with_mom()
        .with_natr()
        .with_obv()
        .with_plus_di()
        .with_plus_dm()
        .with_ppo()
        .with_roc()
        .with_rocp()
        .with_rocr()
        .with_rocr100()
        .with_rsi()
        .with_sar()
        .with_sma()
        .with_sqrt()
        .with_stddev()
        .with_stoch()
        .with_stochf()
        .with_stochrsi()
        .with_supertrend()
        .with_t3ma()
        .with_tema()
        .with_trange()
        .with_trima()
        .with_tsf()
        .with_typprice()
        .with_ultosc()
        .with_var()
        .with_vwap()
        .with_wclprice()
        .with_willr()
        .with_wma()
    )


def test_chart_json():
    chart = _init_chart()
    chart.as_json()


def test_chart_csv():
    chart = _init_chart()
    chart.as_csv()


def test_chart_pandas():
    chart = _init_chart()
    chart.as_pandas()


# def test_chart_plot():
#     chart = _init_chart()
#     chart.as_plotly_figure()
    # plt.close()


def test_string_batch():
    batch_ts = _init_batch_ts('AAPL,RY,EUR/USD,BTC/USD:Huobi,')
    batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()


def test_list_batch():
    batch_ts = _init_batch_ts(['AAPL', 'RY', 'EUR/USD', 'BTC/USD:Huobi'])
    batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()


@patch('twelvedata.http_client.requests.get', return_value=_fake_resp(500))
def test_http_internal_server_error_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InternalServerError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 500, "message": "error message"}')),
)
def test_http_internal_server_error_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InternalServerError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_resp(400))
def test_http_bad_request_error_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(BadRequestError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 400, "message": "error message"}')),
       )
def test_http_bad_request_error_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(BadRequestError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_resp(401))
def test_http_invalid_api_key_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InvalidApiKeyError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 401, "message": "error message"}')),
       )
def test_http_invalid_api_key_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InvalidApiKeyError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_resp(520))
def test_http_other_invalid_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(TwelveDataError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.requests.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 520, "message": "error message"}')),
       )
def test_http_other_invalid_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(TwelveDataError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})
