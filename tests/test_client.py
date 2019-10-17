#!/usr/bin/env python
# coding: utf-8

import pytest

from matplotlib import pyplot as plt
from twelvedata import TDClient
from twelvedata.http_client import DefaultHttpClient


_cache = {}


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


def _init_client():
    return TDClient(
        "581ac79badee4d67bf613474081998db",
        http_client=CachedHttpClient("https://api.twelvedata.com"),
    )


def _init_ts():
    td = _init_client()
    return td.time_series(symbol="AAPL", interval="1min", outputsize=1)


def test_get_stocks_list():
    td = _init_client()
    td.get_stocks_list().as_json()
    td.get_stocks_list().as_csv()


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


def test_time_series():
    ts = _init_ts()
    ts.as_json()
    ts.as_csv()
    ts.as_pandas()
    ts.as_plot()
    ts.as_plotly()
    plt.close()


def test_time_series_get_stocks_list():
    ts = _init_ts()
    ts.get_stocks_list().as_json()
    ts.get_stocks_list().as_csv()
    ts.get_stocks_list().as_pandas()
    ts.get_stocks_list().as_plot()
    ts.get_stocks_list().as_plotly()
    plt.close()


def test_time_series_get_forex_list():
    ts = _init_ts()
    ts.get_forex_list().as_json()
    ts.get_forex_list().as_csv()
    ts.get_forex_list().as_pandas()
    ts.get_forex_list().as_plot()
    ts.get_forex_list().as_plotly()
    plt.close()


def test_time_series_get_cryptocurrency_list():
    ts = _init_ts()
    ts.get_cryptocurrency_list().as_json()
    ts.get_cryptocurrency_list().as_csv()
    ts.get_cryptocurrency_list().as_pandas()
    ts.get_cryptocurrency_list().as_plot()
    ts.get_cryptocurrency_list().as_plotly()
    plt.close()


def test_time_series_get_ad():
    ts = _init_ts()
    ts.get_ad().as_json()
    ts.get_ad().as_csv()
    ts.get_ad().as_pandas()
    ts.get_ad().as_plot()
    ts.get_ad().as_plotly()
    plt.close()


def test_time_series_get_adosc():
    ts = _init_ts()
    ts.get_adosc().as_json()
    ts.get_adosc().as_csv()
    ts.get_adosc().as_pandas()
    ts.get_adosc().as_plot()
    ts.get_adosc().as_plotly()
    plt.close()


def test_time_series_get_adx():
    ts = _init_ts()
    ts.get_adx().as_json()
    ts.get_adx().as_csv()
    ts.get_adx().as_pandas()
    ts.get_adx().as_plot()
    ts.get_adx().as_plotly()
    plt.close()


def test_time_series_get_adxr():
    ts = _init_ts()
    ts.get_adxr().as_json()
    ts.get_adxr().as_csv()
    ts.get_adxr().as_pandas()
    ts.get_adxr().as_plot()
    ts.get_adxr().as_plotly()
    plt.close()


def test_time_series_get_apo():
    ts = _init_ts()
    ts.get_apo().as_json()
    ts.get_apo().as_csv()
    ts.get_apo().as_pandas()
    ts.get_apo().as_plot()
    ts.get_apo().as_plotly()
    plt.close()


def test_time_series_get_aroon():
    ts = _init_ts()
    ts.get_aroon().as_json()
    ts.get_aroon().as_csv()
    ts.get_aroon().as_pandas()
    ts.get_aroon().as_plot()
    ts.get_aroon().as_plotly()
    plt.close()


def test_time_series_get_aroonosc():
    ts = _init_ts()
    ts.get_aroonosc().as_json()
    ts.get_aroonosc().as_csv()
    ts.get_aroonosc().as_pandas()
    ts.get_aroonosc().as_plot()
    ts.get_aroonosc().as_plotly()
    plt.close()


def test_time_series_get_atr():
    ts = _init_ts()
    ts.get_atr().as_json()
    ts.get_atr().as_csv()
    ts.get_atr().as_pandas()
    ts.get_atr().as_plot()
    ts.get_atr().as_plotly()
    plt.close()


def test_time_series_get_avgprice():
    ts = _init_ts()
    ts.get_avgprice().as_json()
    ts.get_avgprice().as_csv()
    ts.get_avgprice().as_pandas()
    ts.get_avgprice().as_plot()
    ts.get_avgprice().as_plotly()
    plt.close()


def test_time_series_get_bbands():
    ts = _init_ts()
    ts.get_bbands().as_json()
    ts.get_bbands().as_csv()
    ts.get_bbands().as_pandas()
    ts.get_bbands().as_plot()
    ts.get_bbands().as_plotly()
    plt.close()


def test_time_series_get_percent_b():
    ts = _init_ts()
    ts.get_percent_b().as_json()
    ts.get_percent_b().as_csv()
    ts.get_percent_b().as_pandas()
    ts.get_percent_b().as_plot()
    ts.get_percent_b().as_plotly()
    plt.close()


def test_time_series_get_bop():
    ts = _init_ts()
    ts.get_bop().as_json()
    ts.get_bop().as_csv()
    ts.get_bop().as_pandas()
    ts.get_bop().as_plot()
    ts.get_bop().as_plotly()
    plt.close()


def test_time_series_get_cci():
    ts = _init_ts()
    ts.get_cci().as_json()
    ts.get_cci().as_csv()
    ts.get_cci().as_pandas()
    ts.get_cci().as_plot()
    ts.get_cci().as_plotly()
    plt.close()


def test_time_series_get_ceil():
    ts = _init_ts()
    ts.get_ceil().as_json()
    ts.get_ceil().as_csv()
    ts.get_ceil().as_pandas()
    ts.get_ceil().as_plot()
    ts.get_ceil().as_plotly()
    plt.close()


def test_time_series_get_cmo():
    ts = _init_ts()
    ts.get_cmo().as_json()
    ts.get_cmo().as_csv()
    ts.get_cmo().as_pandas()
    ts.get_cmo().as_plot()
    ts.get_cmo().as_plotly()
    plt.close()


def test_time_series_get_ceil():
    ts = _init_ts()
    ts.get_ceil().as_json()
    ts.get_ceil().as_csv()
    ts.get_ceil().as_pandas()
    ts.get_ceil().as_plot()
    ts.get_ceil().as_plotly()
    plt.close()


def test_time_series_get_dema():
    ts = _init_ts()
    ts.get_dema().as_json()
    ts.get_dema().as_csv()
    ts.get_dema().as_pandas()
    ts.get_dema().as_plot()
    ts.get_dema().as_plotly()
    plt.close()


def test_time_series_get_dx():
    ts = _init_ts()
    ts.get_dx().as_json()
    ts.get_dx().as_csv()
    ts.get_dx().as_pandas()
    ts.get_dx().as_plot()
    ts.get_dx().as_plotly()
    plt.close()


def test_time_series_get_ema():
    ts = _init_ts()
    ts.get_ema().as_json()
    ts.get_ema().as_csv()
    ts.get_ema().as_pandas()
    ts.get_ema().as_plot()
    ts.get_ema().as_plotly()
    plt.close()


def test_time_series_get_exp():
    ts = _init_ts()
    ts.get_exp().as_json()
    ts.get_exp().as_csv()
    ts.get_exp().as_pandas()
    ts.get_exp().as_plot()
    ts.get_exp().as_plotly()
    plt.close()


def test_time_series_get_floor():
    ts = _init_ts()
    ts.get_floor().as_json()
    ts.get_floor().as_csv()
    ts.get_floor().as_pandas()
    ts.get_floor().as_plot()
    ts.get_floor().as_plotly()
    plt.close()


def test_time_series_get_heikinashicandles():
    ts = _init_ts()
    ts.get_heikinashicandles().as_json()
    ts.get_heikinashicandles().as_csv()
    ts.get_heikinashicandles().as_pandas()
    ts.get_heikinashicandles().as_plot()
    ts.get_heikinashicandles().as_plotly()
    plt.close()


def test_time_series_get_hlc3():
    ts = _init_ts()
    ts.get_hlc3().as_json()
    ts.get_hlc3().as_csv()
    ts.get_hlc3().as_pandas()
    ts.get_hlc3().as_plot()
    ts.get_hlc3().as_plotly()
    plt.close()


def test_time_series_get_ht_dcperiod():
    ts = _init_ts()
    ts.get_ht_dcperiod().as_json()
    ts.get_ht_dcperiod().as_csv()
    ts.get_ht_dcperiod().as_pandas()
    ts.get_ht_dcperiod().as_plot()
    ts.get_ht_dcperiod().as_plotly()
    plt.close()


def test_time_series_get_ht_dcphase():
    ts = _init_ts()
    ts.get_ht_dcphase().as_json()
    ts.get_ht_dcphase().as_csv()
    ts.get_ht_dcphase().as_pandas()
    ts.get_ht_dcphase().as_plot()
    ts.get_ht_dcphase().as_plotly()
    plt.close()


def test_time_series_get_ht_phasor():
    ts = _init_ts()
    ts.get_ht_phasor().as_json()
    ts.get_ht_phasor().as_csv()
    ts.get_ht_phasor().as_pandas()
    ts.get_ht_phasor().as_plot()
    ts.get_ht_phasor().as_plotly()
    plt.close()


def test_time_series_get_ht_sine():
    ts = _init_ts()
    ts.get_ht_sine().as_json()
    ts.get_ht_sine().as_csv()
    ts.get_ht_sine().as_pandas()
    ts.get_ht_sine().as_plot()
    ts.get_ht_sine().as_plotly()
    plt.close()


def test_time_series_get_ht_trendline():
    ts = _init_ts()
    ts.get_ht_trendline().as_json()
    ts.get_ht_trendline().as_csv()
    ts.get_ht_trendline().as_pandas()
    ts.get_ht_trendline().as_plot()
    ts.get_ht_trendline().as_plotly()
    plt.close()


def test_time_series_get_ht_trendmode():
    ts = _init_ts()
    ts.get_ht_trendmode().as_json()
    ts.get_ht_trendmode().as_csv()
    ts.get_ht_trendmode().as_pandas()
    ts.get_ht_trendmode().as_plot()
    ts.get_ht_trendmode().as_plotly()
    plt.close()


def test_time_series_get_kama():
    ts = _init_ts()
    ts.get_kama().as_json()
    ts.get_kama().as_csv()
    ts.get_kama().as_pandas()
    ts.get_kama().as_plot()
    ts.get_kama().as_plotly()
    plt.close()


def test_time_series_get_linearreg():
    ts = _init_ts()
    ts.get_linearreg().as_json()
    ts.get_linearreg().as_csv()
    ts.get_linearreg().as_pandas()
    ts.get_linearreg().as_plot()
    ts.get_linearreg().as_plotly()
    plt.close()


def test_time_series_get_linearregangle():
    ts = _init_ts()
    ts.get_linearregangle().as_json()
    ts.get_linearregangle().as_csv()
    ts.get_linearregangle().as_pandas()
    ts.get_linearregangle().as_plot()
    ts.get_linearregangle().as_plotly()
    plt.close()


def test_time_series_get_linearregintercept():
    ts = _init_ts()
    ts.get_linearregintercept().as_json()
    ts.get_linearregintercept().as_csv()
    ts.get_linearregintercept().as_pandas()
    ts.get_linearregintercept().as_plot()
    ts.get_linearregintercept().as_plotly()
    plt.close()


def test_time_series_get_linearregslope():
    ts = _init_ts()
    ts.get_linearregslope().as_json()
    ts.get_linearregslope().as_csv()
    ts.get_linearregslope().as_pandas()
    ts.get_linearregslope().as_plot()
    ts.get_linearregslope().as_plotly()
    plt.close()


def test_time_series_get_ln():
    ts = _init_ts()
    ts.get_ln().as_json()
    ts.get_ln().as_csv()
    ts.get_ln().as_pandas()
    ts.get_ln().as_plot()
    ts.get_ln().as_plotly()
    plt.close()


def test_time_series_get_log10():
    ts = _init_ts()
    ts.get_log10().as_json()
    ts.get_log10().as_csv()
    ts.get_log10().as_pandas()
    ts.get_log10().as_plot()
    ts.get_log10().as_plotly()
    plt.close()


def test_time_series_get_ma():
    ts = _init_ts()
    ts.get_ma().as_json()
    ts.get_ma().as_csv()
    ts.get_ma().as_pandas()
    ts.get_ma().as_plot()
    ts.get_ma().as_plotly()
    plt.close()


def test_time_series_get_macd():
    ts = _init_ts()
    ts.get_macd().as_json()
    ts.get_macd().as_csv()
    ts.get_macd().as_pandas()
    ts.get_macd().as_plot()
    ts.get_macd().as_plotly()
    plt.close()


def test_time_series_get_macdext():
    ts = _init_ts()
    ts.get_macdext().as_json()
    ts.get_macdext().as_csv()
    ts.get_macdext().as_pandas()
    ts.get_macdext().as_plot()
    ts.get_macdext().as_plotly()
    plt.close()


def test_time_series_get_mama():
    ts = _init_ts()
    ts.get_mama().as_json()
    ts.get_mama().as_csv()
    ts.get_mama().as_pandas()
    ts.get_mama().as_plot()
    ts.get_mama().as_plotly()
    plt.close()


def test_time_series_get_max():
    ts = _init_ts()
    ts.get_max().as_json()
    ts.get_max().as_csv()
    ts.get_max().as_pandas()
    ts.get_max().as_plot()
    ts.get_max().as_plotly()
    plt.close()


def test_time_series_get_maxindex():
    ts = _init_ts()
    ts.get_maxindex().as_json()
    ts.get_maxindex().as_csv()
    ts.get_maxindex().as_pandas()
    ts.get_maxindex().as_plot()
    ts.get_maxindex().as_plotly()
    plt.close()


def test_time_series_get_medprice():
    ts = _init_ts()
    ts.get_medprice().as_json()
    ts.get_medprice().as_csv()
    ts.get_medprice().as_pandas()
    ts.get_medprice().as_plot()
    ts.get_medprice().as_plotly()
    plt.close()


def test_time_series_get_midpoint():
    ts = _init_ts()
    ts.get_midpoint().as_json()
    ts.get_midpoint().as_csv()
    ts.get_midpoint().as_pandas()
    ts.get_midpoint().as_plot()
    ts.get_midpoint().as_plotly()
    plt.close()


def test_time_series_get_midprice():
    ts = _init_ts()
    ts.get_midprice().as_json()
    ts.get_midprice().as_csv()
    ts.get_midprice().as_pandas()
    ts.get_midprice().as_plot()
    ts.get_midprice().as_plotly()
    plt.close()


def test_time_series_get_min():
    ts = _init_ts()
    ts.get_min().as_json()
    ts.get_min().as_csv()
    ts.get_min().as_pandas()
    ts.get_min().as_plot()
    ts.get_min().as_plotly()
    plt.close()


def test_time_series_get_minindex():
    ts = _init_ts()
    ts.get_minindex().as_json()
    ts.get_minindex().as_csv()
    ts.get_minindex().as_pandas()
    ts.get_minindex().as_plot()
    ts.get_minindex().as_plotly()
    plt.close()


def test_time_series_get_minmax():
    ts = _init_ts()
    ts.get_minmax().as_json()
    ts.get_minmax().as_csv()
    ts.get_minmax().as_pandas()
    ts.get_minmax().as_plot()
    ts.get_minmax().as_plotly()
    plt.close()


def test_time_series_get_minmaxindex():
    ts = _init_ts()
    ts.get_minmaxindex().as_json()
    ts.get_minmaxindex().as_csv()
    ts.get_minmaxindex().as_pandas()
    ts.get_minmaxindex().as_plot()
    ts.get_minmaxindex().as_plotly()
    plt.close()


def test_time_series_get_minus_di():
    ts = _init_ts()
    ts.get_minus_di().as_json()
    ts.get_minus_di().as_csv()
    ts.get_minus_di().as_pandas()
    ts.get_minus_di().as_plot()
    ts.get_minus_di().as_plotly()
    plt.close()


def test_time_series_get_minus_dm():
    ts = _init_ts()
    ts.get_minus_dm().as_json()
    ts.get_minus_dm().as_csv()
    ts.get_minus_dm().as_pandas()
    ts.get_minus_dm().as_plot()
    ts.get_minus_dm().as_plotly()
    plt.close()


def test_time_series_get_mom():
    ts = _init_ts()
    ts.get_mom().as_json()
    ts.get_mom().as_csv()
    ts.get_mom().as_pandas()
    ts.get_mom().as_plot()
    ts.get_mom().as_plotly()
    plt.close()


def test_time_series_get_natr():
    ts = _init_ts()
    ts.get_natr().as_json()
    ts.get_natr().as_csv()
    ts.get_natr().as_pandas()
    ts.get_natr().as_plot()
    ts.get_natr().as_plotly()
    plt.close()


def test_time_series_get_obv():
    ts = _init_ts()
    ts.get_obv().as_json()
    ts.get_obv().as_csv()
    ts.get_obv().as_pandas()
    ts.get_obv().as_plot()
    ts.get_obv().as_plotly()
    plt.close()


def test_time_series_get_plus_di():
    ts = _init_ts()
    ts.get_plus_di().as_json()
    ts.get_plus_di().as_csv()
    ts.get_plus_di().as_pandas()
    ts.get_plus_di().as_plot()
    ts.get_plus_di().as_plotly()
    plt.close()


def test_time_series_get_plus_dm():
    ts = _init_ts()
    ts.get_plus_dm().as_json()
    ts.get_plus_dm().as_csv()
    ts.get_plus_dm().as_pandas()
    ts.get_plus_dm().as_plot()
    ts.get_plus_dm().as_plotly()
    plt.close()


def test_time_series_get_ppo():
    ts = _init_ts()
    ts.get_ppo().as_json()
    ts.get_ppo().as_csv()
    ts.get_ppo().as_pandas()
    ts.get_ppo().as_plot()
    ts.get_ppo().as_plotly()
    plt.close()


def test_time_series_get_roc():
    ts = _init_ts()
    ts.get_roc().as_json()
    ts.get_roc().as_csv()
    ts.get_roc().as_pandas()
    ts.get_roc().as_plot()
    ts.get_roc().as_plotly()
    plt.close()


def test_time_series_get_rocp():
    ts = _init_ts()
    ts.get_rocp().as_json()
    ts.get_rocp().as_csv()
    ts.get_rocp().as_pandas()
    ts.get_rocp().as_plot()
    ts.get_rocp().as_plotly()
    plt.close()


def test_time_series_get_rocr():
    ts = _init_ts()
    ts.get_rocr().as_json()
    ts.get_rocr().as_csv()
    ts.get_rocr().as_pandas()
    ts.get_rocr().as_plot()
    ts.get_rocr().as_plotly()
    plt.close()


def test_time_series_get_rocr100():
    ts = _init_ts()
    ts.get_rocr100().as_json()
    ts.get_rocr100().as_csv()
    ts.get_rocr100().as_pandas()
    ts.get_rocr100().as_plot()
    ts.get_rocr100().as_plotly()
    plt.close()


def test_time_series_get_rsi():
    ts = _init_ts()
    ts.get_rsi().as_json()
    ts.get_rsi().as_csv()
    ts.get_rsi().as_pandas()
    ts.get_rsi().as_plot()
    ts.get_rsi().as_plotly()
    plt.close()


def test_time_series_get_sar():
    ts = _init_ts()
    ts.get_sar().as_json()
    ts.get_sar().as_csv()
    ts.get_sar().as_pandas()
    ts.get_sar().as_plot()
    ts.get_sar().as_plotly()
    plt.close()


def test_time_series_get_sma():
    ts = _init_ts()
    ts.get_sma().as_json()
    ts.get_sma().as_csv()
    ts.get_sma().as_pandas()
    ts.get_sma().as_plot()
    ts.get_sma().as_plotly()
    plt.close()


def test_time_series_get_sqrt():
    ts = _init_ts()
    ts.get_sqrt().as_json()
    ts.get_sqrt().as_csv()
    ts.get_sqrt().as_pandas()
    ts.get_sqrt().as_plot()
    ts.get_sqrt().as_plotly()
    plt.close()


def test_time_series_get_stddev():
    ts = _init_ts()
    ts.get_stddev().as_json()
    ts.get_stddev().as_csv()
    ts.get_stddev().as_pandas()
    ts.get_stddev().as_plot()
    ts.get_stddev().as_plotly()
    plt.close()


def test_time_series_get_stoch():
    ts = _init_ts()
    ts.get_stoch().as_json()
    ts.get_stoch().as_csv()
    ts.get_stoch().as_pandas()
    ts.get_stoch().as_plot()
    ts.get_stoch().as_plotly()
    plt.close()


def test_time_series_get_stochf():
    ts = _init_ts()
    ts.get_stochf().as_json()
    ts.get_stochf().as_csv()
    ts.get_stochf().as_pandas()
    ts.get_stochf().as_plot()
    ts.get_stochf().as_plotly()
    plt.close()


def test_time_series_get_stochrsi():
    ts = _init_ts()
    ts.get_stochrsi().as_json()
    ts.get_stochrsi().as_csv()
    ts.get_stochrsi().as_pandas()
    ts.get_stochrsi().as_plot()
    ts.get_stochrsi().as_plotly()
    plt.close()


def test_time_series_get_t3ma():
    ts = _init_ts()
    ts.get_t3ma().as_json()
    ts.get_t3ma().as_csv()
    ts.get_t3ma().as_pandas()
    ts.get_t3ma().as_plot()
    ts.get_t3ma().as_plotly()
    plt.close()


def test_time_series_get_tema():
    ts = _init_ts()
    ts.get_tema().as_json()
    ts.get_tema().as_csv()
    ts.get_tema().as_pandas()
    ts.get_tema().as_plot()
    ts.get_tema().as_plotly()
    plt.close()


def test_time_series_get_trange():
    ts = _init_ts()
    ts.get_trange().as_json()
    ts.get_trange().as_csv()
    ts.get_trange().as_pandas()
    ts.get_trange().as_plot()
    ts.get_trange().as_plotly()
    plt.close()


def test_time_series_get_trima():
    ts = _init_ts()
    ts.get_trima().as_json()
    ts.get_trima().as_csv()
    ts.get_trima().as_pandas()
    ts.get_trima().as_plot()
    ts.get_trima().as_plotly()
    plt.close()


def test_time_series_get_tsf():
    ts = _init_ts()
    ts.get_tsf().as_json()
    ts.get_tsf().as_csv()
    ts.get_tsf().as_pandas()
    ts.get_tsf().as_plot()
    ts.get_tsf().as_plotly()
    plt.close()


def test_time_series_get_typprice():
    ts = _init_ts()
    ts.get_typprice().as_json()
    ts.get_typprice().as_csv()
    ts.get_typprice().as_pandas()
    ts.get_typprice().as_plot()
    ts.get_typprice().as_plotly()
    plt.close()


def test_time_series_get_ultosc():
    ts = _init_ts()
    ts.get_ultosc().as_json()
    ts.get_ultosc().as_csv()
    ts.get_ultosc().as_pandas()
    ts.get_ultosc().as_plot()
    ts.get_ultosc().as_plotly()
    plt.close()


def test_time_series_get_var():
    ts = _init_ts()
    ts.get_var().as_json()
    ts.get_var().as_csv()
    ts.get_var().as_pandas()
    ts.get_var().as_plot()
    ts.get_var().as_plotly()
    plt.close()


def test_time_series_get_wclprice():
    ts = _init_ts()
    ts.get_wclprice().as_json()
    ts.get_wclprice().as_csv()
    ts.get_wclprice().as_pandas()
    ts.get_wclprice().as_plot()
    ts.get_wclprice().as_plotly()
    plt.close()


def test_time_series_get_willr():
    ts = _init_ts()
    ts.get_willr().as_json()
    ts.get_willr().as_csv()
    ts.get_willr().as_pandas()
    ts.get_willr().as_plot()
    ts.get_willr().as_plotly()
    plt.close()


def test_time_series_get_wma():
    ts = _init_ts()
    ts.get_wma().as_json()
    ts.get_wma().as_csv()
    ts.get_wma().as_pandas()
    ts.get_wma().as_plot()
    ts.get_wma().as_plotly()
    plt.close()


def _init_chart():
    td = _init_client()
    return (
        td.chart(symbol="AAPL", interval="1min")
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
        .with_kama()
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
        .with_t3ma()
        .with_tema()
        .with_trange()
        .with_trima()
        .with_tsf()
        .with_typprice()
        .with_ultosc()
        .with_var()
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


def test_chart_plot():
    chart = _init_chart()
    chart.as_plot()
    chart.as_plotly()
    plt.close()
