#!/usr/bin/env python
# coding: utf-8

import json
import os
import pytest
from requests import Response
from unittest.mock import patch, MagicMock, PropertyMock

import pandas as pd
from matplotlib import pyplot as plt
from twelvedata import TDClient
from twelvedata.http_client import DefaultHttpClient
from twelvedata.exceptions import (
    BadRequestError,
    InternalServerError,
    InvalidApiKeyError,
    TwelveDataError,
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


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
        os.environ.get("TWELVEDATA_API_KEY", "demo"),
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
    assert td.get_stocks_list(exchange='NASDAQ').as_json()
    td.get_stocks_list(exchange='NASDAQ').as_csv()
    assert not td.get_stocks_list(exchange='NASDAQ').as_pandas().empty
    td.get_stocks_list(exchange='NASDAQ').as_url()


def test_get_stock_exchanges_list():
    td = _init_client()
    assert td.get_stock_exchanges_list().as_json()
    td.get_stock_exchanges_list().as_csv()
    assert not td.get_stock_exchanges_list().as_pandas().empty
    td.get_stock_exchanges_list().as_url()


def test_get_forex_pairs_list():
    td = _init_client()
    assert td.get_forex_pairs_list().as_json()
    td.get_forex_pairs_list().as_csv()
    assert not td.get_forex_pairs_list().as_pandas().empty
    td.get_forex_pairs_list().as_url()


def test_get_cryptocurrencies_list():
    td = _init_client()
    assert td.get_cryptocurrencies_list().as_json()
    td.get_cryptocurrencies_list().as_csv()
    assert not td.get_cryptocurrencies_list().as_pandas().empty
    td.get_cryptocurrencies_list().as_url()


def test_get_funds_list():
    td = _init_client()
    params = {'outputsize': 10, 'page': 0}
    l = td.get_funds_list(**params).as_json()
    assert len(l) > 0
    td.get_funds_list(**params).as_csv()
    assert not td.get_funds_list(**params).as_pandas().empty
    td.get_funds_list(**params).as_url()


def test_get_bonds_list():
    td = _init_client()
    l = td.get_bonds_list().as_json()
    assert len(l) > 0
    td.get_bonds_list().as_csv()
    assert not td.get_bonds_list().as_pandas().empty
    td.get_bonds_list().as_url()


def test_get_commodities_list():
    td = _init_client()
    assert '/commodities' in td.get_commodities_list().as_url()
    assert not td.get_commodities_list().as_pandas().empty


def test_get_cryptocurrency_exchanges_list():
    td = _init_client()
    assert '/cryptocurrency_exchanges' in td.get_cryptocurrency_exchanges_list().as_url()
    assert not td.get_cryptocurrency_exchanges_list().as_pandas().empty


def test_get_etf_list():
    td = _init_client()
    assert td.get_etf_list().as_json()
    td.get_etf_list().as_csv()
    assert not td.get_etf_list().as_pandas().empty
    td.get_etf_list().as_url()


def test_get_indices_list():
    td = _init_client()
    assert td.get_indices_list().as_json()
    td.get_indices_list().as_csv()
    assert not td.get_indices_list().as_pandas().empty
    td.get_indices_list().as_url()


def test_get_technical_indicators_list():
    td = _init_client()
    assert td.get_technical_indicators_list().as_json()
    assert not td.get_technical_indicators_list().as_pandas().empty
    td.get_technical_indicators_list().as_url()


def test_get_exchanges_list():
    td = _init_client()
    assert td.get_exchanges_list().as_json()
    td.get_exchanges_list().as_csv()
    assert not td.get_exchanges_list().as_pandas().empty
    td.get_exchanges_list().as_url()


def test_symbol_search():
    td = _init_client()
    assert td.symbol_search().as_json()
    assert not td.symbol_search().as_pandas().empty
    td.symbol_search().as_url()


def test_earliest_timestamp():
    td = _init_client()
    assert td.get_earliest_timestamp(symbol="AAPL", interval="1day").as_json()
    df = td.get_earliest_timestamp(symbol="AAPL", interval="1day").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_earliest_timestamp(symbol="AAPL", interval="1day").as_url()


def test_market_state():
    td = _init_client()
    assert td.get_market_state().as_json()
    assert not td.get_market_state().as_pandas().empty
    td.get_market_state().as_url()


def test_exchange_rate():
    td = _init_client()
    assert td.exchange_rate(symbol="EUR/USD").as_json()
    assert len(td.exchange_rate(symbol="EUR/USD").as_pandas()) >= 1
    td.exchange_rate(symbol="EUR/USD").as_url()


def test_currency_conversion():
    td = _init_client()
    assert td.currency_conversion(symbol="EUR/USD", amount=100).as_json()
    assert len(td.currency_conversion(symbol="EUR/USD", amount=100).as_pandas()) >= 1
    td.currency_conversion(symbol="EUR/USD", amount=100).as_url()


def test_quote():
    td = _init_client()
    assert td.quote(symbol="AAPL").as_json()
    df = td.quote(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.quote(symbol="AAPL").as_url()


def test_price():
    td = _init_client()
    assert td.price(symbol="AAPL").as_json()
    assert len(td.price(symbol="AAPL").as_pandas()) >= 1
    td.price(symbol="AAPL").as_url()


def test_eod():
    td = _init_client()
    assert td.eod(symbol="AAPL").as_json()
    df = td.eod(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.eod(symbol="AAPL").as_url()


def test_api_usage():
    td = _init_client()
    assert td.api_usage().as_json()
    assert len(td.api_usage().as_pandas()) >= 1
    td.api_usage().as_url()


def test_logo():
    td = _init_client()
    assert td.get_logo(symbol="AAPL").as_json()
    assert len(td.get_logo(symbol="AAPL").as_pandas()) >= 1
    td.get_logo(symbol="AAPL").as_url()


def test_profile():
    td = _init_client()
    assert td.get_profile(symbol="AAPL").as_json()
    assert len(td.get_profile(symbol="AAPL").as_pandas()) >= 1
    td.get_profile(symbol="AAPL").as_url()


def test_dividends():
    td = _init_client()
    assert td.get_dividends(symbol="AAPL").as_json()
    df = td.get_dividends(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_dividends(symbol="AAPL").as_url()


def test_dividends_calendar():
    td = _init_client()
    assert td.get_dividends_calendar(symbol="AAPL").as_json()
    df = td.get_dividends_calendar(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_dividends_calendar(symbol="AAPL").as_url()


def test_splits():
    td = _init_client()
    assert td.get_splits(symbol="AAPL").as_json()
    df = td.get_splits(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_splits(symbol="AAPL").as_url()


def test_splits_calendar():
    td = _init_client()
    assert td.get_splits_calendar(symbol="AAPL").as_json()
    df = td.get_splits_calendar(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_splits_calendar(symbol="AAPL").as_url()


def test_get_earnings_calendar():
    td = _init_client()
    assert '/earnings_calendar' in td.get_earnings_calendar().as_url()
    df = td.get_earnings_calendar().as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_ipo_calendar():
    td = _init_client()
    assert '/ipo_calendar' in td.get_ipo_calendar().as_url()
    df = td.get_ipo_calendar().as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_earnings():
    td = _init_client()
    assert td.get_earnings(symbol="AAPL").as_json()
    df = td.get_earnings(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_earnings(symbol="AAPL").as_url()


def test_statistics():
    td = _init_client()
    assert td.get_statistics(symbol="AAPL").as_json()
    assert len(td.get_statistics(symbol="AAPL").as_pandas()) >= 1
    td.get_statistics(symbol="AAPL").as_url()


def test_insider_transactions():
    td = _init_client()
    assert td.get_insider_transactions(symbol="AAPL").as_json()
    df = td.get_insider_transactions(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_insider_transactions(symbol="AAPL").as_url()


def test_income_statement():
    td = _init_client()
    assert td.get_income_statement(symbol="AAPL").as_json()
    df = td.get_income_statement(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_income_statement(symbol="AAPL").as_url()


def test_balance_sheet():
    td = _init_client()
    assert td.get_balance_sheet(symbol="AAPL").as_json()
    df = td.get_balance_sheet(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_balance_sheet(symbol="AAPL").as_url()


def test_cash_flow():
    td = _init_client()
    assert td.get_cash_flow(symbol="AAPL").as_json()
    df = td.get_cash_flow(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_cash_flow(symbol="AAPL").as_url()


def test_key_executives():
    td = _init_client()
    assert td.get_key_executives(symbol="AAPL").as_json()
    assert not td.get_key_executives(symbol="AAPL").as_pandas().empty
    td.get_key_executives(symbol="AAPL").as_url()


def test_institutional_holders():
    td = _init_client()
    assert td.get_institutional_holders(symbol="AAPL").as_json()
    df = td.get_institutional_holders(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_institutional_holders(symbol="AAPL").as_url()


def test_fund_holders():
    td = _init_client()
    assert td.get_fund_holders(symbol="AAPL").as_json()
    df = td.get_fund_holders(symbol="AAPL").as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)
    td.get_fund_holders(symbol="AAPL").as_url()


def test_time_series():
    ts = _init_ts()
    assert ts.as_json()
    ts.as_csv()
    df = ts.as_pandas()
    ts.as_plotly_figure()
    ts.as_plotly_figure(df=df)
    ts.as_url()
    plt.close()


def test_time_series_get_ad():
    ts = _init_ts()
    assert ts.with_ad().as_json()
    ts.with_ad().as_csv()
    df = ts.with_ad().as_pandas()
    ts.with_ad().as_plotly_figure()
    ts.with_ad().as_plotly_figure(df=df)
    ts.with_ad().as_url()
    plt.close()


def test_time_series_get_adosc():
    ts = _init_ts()
    assert ts.with_adosc().as_json()
    ts.with_adosc().as_csv()
    ts.with_adosc().as_pandas()
    ts.with_adosc().as_plotly_figure()
    ts.with_adosc().as_url()
    plt.close()


def test_time_series_get_adx():
    ts = _init_ts()
    assert ts.with_adx().as_json()
    ts.with_adx().as_csv()
    ts.with_adx().as_pandas()
    ts.with_adx().as_plotly_figure()
    ts.with_adx().as_url()
    plt.close()


def test_time_series_get_adxr():
    ts = _init_ts()
    assert ts.with_adxr().as_json()
    ts.with_adxr().as_csv()
    ts.with_adxr().as_pandas()
    ts.with_adxr().as_plotly_figure()
    ts.with_adxr().as_url()
    plt.close()


def test_time_series_get_apo():
    ts = _init_ts()
    assert ts.with_apo().as_json()
    ts.with_apo().as_csv()
    ts.with_apo().as_pandas()
    ts.with_apo().as_plotly_figure()
    ts.with_apo().as_url()
    plt.close()


def test_time_series_get_aroon():
    ts = _init_ts()
    assert ts.with_aroon().as_json()
    ts.with_aroon().as_csv()
    ts.with_aroon().as_pandas()
    ts.with_aroon().as_plotly_figure()
    ts.with_aroon().as_url()
    plt.close()


def test_time_series_get_aroonosc():
    ts = _init_ts()
    assert ts.with_aroonosc().as_json()
    ts.with_aroonosc().as_csv()
    ts.with_aroonosc().as_pandas()
    ts.with_aroonosc().as_plotly_figure()
    ts.with_aroonosc().as_url()
    plt.close()


def test_time_series_get_atr():
    ts = _init_ts()
    assert ts.with_atr().as_json()
    ts.with_atr().as_csv()
    ts.with_atr().as_pandas()
    ts.with_atr().as_plotly_figure()
    ts.with_atr().as_url()
    plt.close()


def test_time_series_get_avgprice():
    ts = _init_ts()
    assert ts.with_avgprice().as_json()
    ts.with_avgprice().as_csv()
    ts.with_avgprice().as_pandas()
    ts.with_avgprice().as_plotly_figure()
    ts.with_avgprice().as_url()
    plt.close()


def test_time_series_get_bbands():
    ts = _init_ts()
    assert ts.with_bbands().as_json()
    ts.with_bbands().as_csv()
    ts.with_bbands().as_pandas()
    ts.with_bbands().as_plotly_figure()
    ts.with_bbands().as_url()
    plt.close()


def test_time_series_get_beta():
    ts = _init_ts()
    assert ts.with_beta().as_json()
    ts.with_beta().as_pandas()
    ts.with_beta().as_plotly_figure()
    ts.with_beta().as_url()
    plt.close()


def test_time_series_get_percent_b():
    ts = _init_ts()
    assert ts.with_percent_b().as_json()
    ts.with_percent_b().as_csv()
    ts.with_percent_b().as_pandas()
    ts.with_percent_b().as_plotly_figure()
    ts.with_percent_b().as_url()
    plt.close()


def test_time_series_get_bop():
    ts = _init_ts()
    assert ts.with_bop().as_json()
    ts.with_bop().as_csv()
    ts.with_bop().as_pandas()
    ts.with_bop().as_plotly_figure()
    ts.with_bop().as_url()
    plt.close()


def test_time_series_get_cci():
    ts = _init_ts()
    assert ts.with_cci().as_json()
    ts.with_cci().as_csv()
    ts.with_cci().as_pandas()
    ts.with_cci().as_plotly_figure()
    ts.with_cci().as_url()
    plt.close()


def test_time_series_get_ceil():
    ts = _init_ts()
    assert ts.with_ceil().as_json()
    ts.with_ceil().as_csv()
    ts.with_ceil().as_pandas()
    ts.with_ceil().as_plotly_figure()
    ts.with_ceil().as_url()
    plt.close()


def test_time_series_get_cmo():
    ts = _init_ts()
    assert ts.with_cmo().as_json()
    ts.with_cmo().as_csv()
    ts.with_cmo().as_pandas()
    ts.with_cmo().as_plotly_figure()
    ts.with_cmo().as_url()
    plt.close()


def test_time_series_get_coppock():
    ts = _init_ts()
    assert ts.with_coppock().as_json()
    ts.with_coppock().as_csv()
    ts.with_coppock().as_pandas()
    ts.with_coppock().as_plotly_figure()
    ts.with_coppock().as_url()
    plt.close()


def test_time_series_get_dema():
    ts = _init_ts()
    assert ts.with_dema().as_json()
    ts.with_dema().as_csv()
    ts.with_dema().as_pandas()
    ts.with_dema().as_plotly_figure()
    ts.with_dema().as_url()
    plt.close()


def test_time_series_get_dx():
    ts = _init_ts()
    assert ts.with_dx().as_json()
    ts.with_dx().as_csv()
    ts.with_dx().as_pandas()
    ts.with_dx().as_plotly_figure()
    ts.with_dx().as_url()
    plt.close()


def test_time_series_get_ema():
    ts = _init_ts()
    assert ts.with_ema().as_json()
    ts.with_ema().as_csv()
    ts.with_ema().as_pandas()
    ts.with_ema().as_plotly_figure()
    ts.with_ema().as_url()
    plt.close()


def test_time_series_get_exp():
    ts = _init_ts()
    assert ts.with_exp().as_json()
    ts.with_exp().as_csv()
    ts.with_exp().as_pandas()
    ts.with_exp().as_plotly_figure()
    ts.with_exp().as_url()
    plt.close()


def test_time_series_get_floor():
    ts = _init_ts()
    assert ts.with_floor().as_json()
    ts.with_floor().as_csv()
    ts.with_floor().as_pandas()
    ts.with_floor().as_plotly_figure()
    ts.with_floor().as_url()
    plt.close()


def test_time_series_get_heikinashicandles():
    ts = _init_ts()
    assert ts.with_heikinashicandles().as_json()
    ts.with_heikinashicandles().as_csv()
    ts.with_heikinashicandles().as_pandas()
    ts.with_heikinashicandles().as_plotly_figure()
    ts.with_heikinashicandles().as_url()
    plt.close()


def test_time_series_get_hlc3():
    ts = _init_ts()
    assert ts.with_hlc3().as_json()
    ts.with_hlc3().as_csv()
    ts.with_hlc3().as_pandas()
    ts.with_hlc3().as_plotly_figure()
    ts.with_hlc3().as_url()
    plt.close()


def test_time_series_get_ht_dcperiod():
    ts = _init_ts()
    assert ts.with_ht_dcperiod().as_json()
    ts.with_ht_dcperiod().as_csv()
    ts.with_ht_dcperiod().as_pandas()
    ts.with_ht_dcperiod().as_plotly_figure()
    ts.with_ht_dcperiod().as_url()
    plt.close()


def test_time_series_get_ht_dcphase():
    ts = _init_ts()
    assert ts.with_ht_dcphase().as_json()
    ts.with_ht_dcphase().as_csv()
    ts.with_ht_dcphase().as_pandas()
    ts.with_ht_dcphase().as_plotly_figure()
    ts.with_ht_dcphase().as_url()
    plt.close()


def test_time_series_get_ht_phasor():
    ts = _init_ts()
    assert ts.with_ht_phasor().as_json()
    ts.with_ht_phasor().as_csv()
    ts.with_ht_phasor().as_pandas()
    ts.with_ht_phasor().as_plotly_figure()
    ts.with_ht_phasor().as_url()
    plt.close()


def test_time_series_get_ht_sine():
    ts = _init_ts()
    assert ts.with_ht_sine().as_json()
    ts.with_ht_sine().as_csv()
    ts.with_ht_sine().as_pandas()
    ts.with_ht_sine().as_plotly_figure()
    ts.with_ht_sine().as_url()
    plt.close()


def test_time_series_get_ht_trendline():
    ts = _init_ts()
    assert ts.with_ht_trendline().as_json()
    ts.with_ht_trendline().as_csv()
    ts.with_ht_trendline().as_pandas()
    ts.with_ht_trendline().as_plotly_figure()
    ts.with_ht_trendline().as_url()
    plt.close()


def test_time_series_get_ht_trendmode():
    ts = _init_ts()
    assert ts.with_ht_trendmode().as_json()
    ts.with_ht_trendmode().as_csv()
    ts.with_ht_trendmode().as_pandas()
    ts.with_ht_trendmode().as_plotly_figure()
    ts.with_ht_trendmode().as_url()
    plt.close()


def test_time_series_get_ichimoku():
    ts = _init_ts()
    assert ts.with_ichimoku().as_json()
    ts.with_ichimoku().as_csv()
    ts.with_ichimoku().as_pandas()
    ts.with_ichimoku().as_plotly_figure()
    ts.with_ichimoku().as_url()
    plt.close()


def test_time_series_get_kama():
    ts = _init_ts()
    assert ts.with_kama().as_json()
    ts.with_kama().as_csv()
    ts.with_kama().as_pandas()
    ts.with_kama().as_plotly_figure()
    ts.with_kama().as_url()
    plt.close()


def test_time_series_get_keltner():
    ts = _init_ts()
    assert ts.with_keltner().as_json()
    ts.with_keltner().as_csv()
    ts.with_keltner().as_pandas()
    ts.with_keltner().as_plotly_figure()
    ts.with_keltner().as_url()
    plt.close()


def test_time_series_get_kst():
    ts = _init_ts()
    assert ts.with_kst().as_json()
    ts.with_kst().as_csv()
    ts.with_kst().as_pandas()
    ts.with_kst().as_plotly_figure()
    ts.with_kst().as_url()
    plt.close()


def test_time_series_get_linearreg():
    ts = _init_ts()
    assert ts.with_linearreg().as_json()
    ts.with_linearreg().as_csv()
    ts.with_linearreg().as_pandas()
    ts.with_linearreg().as_plotly_figure()
    ts.with_linearreg().as_url()
    plt.close()


def test_time_series_get_linearregangle():
    ts = _init_ts()
    assert ts.with_linearregangle().as_json()
    ts.with_linearregangle().as_csv()
    ts.with_linearregangle().as_pandas()
    ts.with_linearregangle().as_plotly_figure()
    ts.with_linearregangle().as_url()
    plt.close()


def test_time_series_get_linearregintercept():
    ts = _init_ts()
    assert ts.with_linearregintercept().as_json()
    ts.with_linearregintercept().as_csv()
    ts.with_linearregintercept().as_pandas()
    ts.with_linearregintercept().as_plotly_figure()
    ts.with_linearregintercept().as_url()
    plt.close()


def test_time_series_get_linearregslope():
    ts = _init_ts()
    assert ts.with_linearregslope().as_json()
    ts.with_linearregslope().as_csv()
    ts.with_linearregslope().as_pandas()
    ts.with_linearregslope().as_plotly_figure()
    ts.with_linearregslope().as_url()
    plt.close()


def test_time_series_get_ln():
    ts = _init_ts()
    assert ts.with_ln().as_json()
    ts.with_ln().as_csv()
    ts.with_ln().as_pandas()
    ts.with_ln().as_plotly_figure()
    ts.with_ln().as_url()
    plt.close()


def test_time_series_get_log10():
    ts = _init_ts()
    assert ts.with_log10().as_json()
    ts.with_log10().as_csv()
    ts.with_log10().as_pandas()
    ts.with_log10().as_plotly_figure()
    ts.with_log10().as_url()
    plt.close()


def test_time_series_get_ma():
    ts = _init_ts()
    assert ts.with_ma().as_json()
    ts.with_ma().as_csv()
    ts.with_ma().as_pandas()
    ts.with_ma().as_plotly_figure()
    ts.with_ma().as_url()
    plt.close()


def test_time_series_get_macd():
    ts = _init_ts()
    assert ts.with_macd().as_json()
    ts.with_macd().as_csv()
    ts.with_macd().as_pandas()
    ts.with_macd().as_plotly_figure()
    ts.with_macd().as_url()
    plt.close()


def test_time_series_get_macdext():
    ts = _init_ts()
    assert ts.with_macdext().as_json()
    ts.with_macdext().as_csv()
    ts.with_macdext().as_pandas()
    ts.with_macdext().as_plotly_figure()
    ts.with_macdext().as_url()
    plt.close()


def test_time_series_get_mama():
    ts = _init_ts()
    assert ts.with_mama().as_json()
    ts.with_mama().as_csv()
    ts.with_mama().as_pandas()
    ts.with_mama().as_plotly_figure()
    ts.with_mama().as_url()
    plt.close()


def test_time_series_get_max():
    ts = _init_ts()
    assert ts.with_max().as_json()
    ts.with_max().as_csv()
    ts.with_max().as_pandas()
    ts.with_max().as_plotly_figure()
    ts.with_max().as_url()
    plt.close()


def test_time_series_get_maxindex():
    ts = _init_ts()
    assert ts.with_maxindex().as_json()
    ts.with_maxindex().as_csv()
    ts.with_maxindex().as_pandas()
    ts.with_maxindex().as_plotly_figure()
    ts.with_maxindex().as_url()
    plt.close()


def test_time_series_get_mcginley_dynamic():
    ts = _init_ts()
    assert ts.with_mcginley_dynamic().as_json()
    ts.with_mcginley_dynamic().as_csv()
    ts.with_mcginley_dynamic().as_pandas()
    ts.with_mcginley_dynamic().as_plotly_figure()
    ts.with_mcginley_dynamic().as_url()
    plt.close()


def test_time_series_get_medprice():
    ts = _init_ts()
    assert ts.with_medprice().as_json()
    ts.with_medprice().as_csv()
    ts.with_medprice().as_pandas()
    ts.with_medprice().as_plotly_figure()
    ts.with_medprice().as_url()
    plt.close()


def test_time_series_get_mfi():
    ts = _init_ts()
    assert ts.with_mfi().as_json()
    ts.with_mfi().as_csv()
    ts.with_mfi().as_pandas()
    ts.with_mfi().as_plotly_figure()
    ts.with_mfi().as_url()
    plt.close()


def test_time_series_get_midpoint():
    ts = _init_ts()
    assert ts.with_midpoint().as_json()
    ts.with_midpoint().as_csv()
    ts.with_midpoint().as_pandas()
    ts.with_midpoint().as_plotly_figure()
    ts.with_midpoint().as_url()
    plt.close()


def test_time_series_get_midprice():
    ts = _init_ts()
    assert ts.with_midprice().as_json()
    ts.with_midprice().as_csv()
    ts.with_midprice().as_pandas()
    ts.with_midprice().as_plotly_figure()
    ts.with_midprice().as_url()
    plt.close()


def test_time_series_get_min():
    ts = _init_ts()
    assert ts.with_min().as_json()
    ts.with_min().as_csv()
    ts.with_min().as_pandas()
    ts.with_min().as_plotly_figure()
    ts.with_min().as_url()
    plt.close()


def test_time_series_get_minindex():
    ts = _init_ts()
    assert ts.with_minindex().as_json()
    ts.with_minindex().as_csv()
    ts.with_minindex().as_pandas()
    ts.with_minindex().as_plotly_figure()
    ts.with_minindex().as_url()
    plt.close()


def test_time_series_get_minmax():
    ts = _init_ts()
    assert ts.with_minmax().as_json()
    ts.with_minmax().as_csv()
    ts.with_minmax().as_pandas()
    ts.with_minmax().as_plotly_figure()
    ts.with_minmax().as_url()
    plt.close()


def test_time_series_get_minmaxindex():
    ts = _init_ts()
    assert ts.with_minmaxindex().as_json()
    ts.with_minmaxindex().as_csv()
    ts.with_minmaxindex().as_pandas()
    ts.with_minmaxindex().as_plotly_figure()
    ts.with_minmaxindex().as_url()
    plt.close()


def test_time_series_get_minus_di():
    ts = _init_ts()
    assert ts.with_minus_di().as_json()
    ts.with_minus_di().as_csv()
    ts.with_minus_di().as_pandas()
    ts.with_minus_di().as_plotly_figure()
    ts.with_minus_di().as_url()
    plt.close()


def test_time_series_get_minus_dm():
    ts = _init_ts()
    assert ts.with_minus_dm().as_json()
    ts.with_minus_dm().as_csv()
    ts.with_minus_dm().as_pandas()
    ts.with_minus_dm().as_plotly_figure()
    ts.with_minus_dm().as_url()
    plt.close()


def test_time_series_get_mom():
    ts = _init_ts()
    assert ts.with_mom().as_json()
    ts.with_mom().as_csv()
    ts.with_mom().as_pandas()
    ts.with_mom().as_plotly_figure()
    ts.with_mom().as_url()
    plt.close()


def test_time_series_get_natr():
    ts = _init_ts()
    assert ts.with_natr().as_json()
    ts.with_natr().as_csv()
    ts.with_natr().as_pandas()
    ts.with_natr().as_plotly_figure()
    ts.with_natr().as_url()
    plt.close()


def test_time_series_get_obv():
    ts = _init_ts()
    assert ts.with_obv().as_json()
    ts.with_obv().as_csv()
    ts.with_obv().as_pandas()
    ts.with_obv().as_plotly_figure()
    ts.with_obv().as_url()
    plt.close()


def test_time_series_get_plus_di():
    ts = _init_ts()
    assert ts.with_plus_di().as_json()
    ts.with_plus_di().as_csv()
    ts.with_plus_di().as_pandas()
    ts.with_plus_di().as_plotly_figure()
    ts.with_plus_di().as_url()
    plt.close()


def test_time_series_get_plus_dm():
    ts = _init_ts()
    assert ts.with_plus_dm().as_json()
    ts.with_plus_dm().as_csv()
    ts.with_plus_dm().as_pandas()
    ts.with_plus_dm().as_plotly_figure()
    ts.with_plus_dm().as_url()
    plt.close()


def test_time_series_get_ppo():
    ts = _init_ts()
    assert ts.with_ppo().as_json()
    ts.with_ppo().as_csv()
    ts.with_ppo().as_pandas()
    ts.with_ppo().as_plotly_figure()
    ts.with_ppo().as_url()
    plt.close()


def test_time_series_get_roc():
    ts = _init_ts()
    assert ts.with_roc().as_json()
    ts.with_roc().as_csv()
    ts.with_roc().as_pandas()
    ts.with_roc().as_plotly_figure()
    ts.with_roc().as_url()
    plt.close()


def test_time_series_get_rocp():
    ts = _init_ts()
    assert ts.with_rocp().as_json()
    ts.with_rocp().as_csv()
    ts.with_rocp().as_pandas()
    ts.with_rocp().as_plotly_figure()
    ts.with_rocp().as_url()
    plt.close()


def test_time_series_get_rocr():
    ts = _init_ts()
    assert ts.with_rocr().as_json()
    ts.with_rocr().as_csv()
    ts.with_rocr().as_pandas()
    ts.with_rocr().as_plotly_figure()
    ts.with_rocr().as_url()
    plt.close()


def test_time_series_get_rocr100():
    ts = _init_ts()
    assert ts.with_rocr100().as_json()
    ts.with_rocr100().as_csv()
    ts.with_rocr100().as_pandas()
    ts.with_rocr100().as_plotly_figure()
    ts.with_rocr100().as_url()
    plt.close()


def test_time_series_get_rsi():
    ts = _init_ts()
    assert ts.with_rsi().as_json()
    ts.with_rsi().as_csv()
    ts.with_rsi().as_pandas()
    ts.with_rsi().as_plotly_figure()
    ts.with_rsi().as_url()
    plt.close()


def test_time_series_get_sar():
    ts = _init_ts()
    assert ts.with_sar().as_json()
    ts.with_sar().as_csv()
    ts.with_sar().as_pandas()
    ts.with_sar().as_plotly_figure()
    ts.with_sar().as_url()
    plt.close()


def test_time_series_get_sma():
    ts = _init_ts()
    assert ts.with_sma().as_json()
    ts.with_sma().as_csv()
    ts.with_sma().as_pandas()
    ts.with_sma().as_plotly_figure()
    ts.with_sma().as_url()
    plt.close()


def test_time_series_get_sqrt():
    ts = _init_ts()
    assert ts.with_sqrt().as_json()
    ts.with_sqrt().as_csv()
    ts.with_sqrt().as_pandas()
    ts.with_sqrt().as_plotly_figure()
    ts.with_sqrt().as_url()
    plt.close()


def test_time_series_get_stddev():
    ts = _init_ts()
    assert ts.with_stddev().as_json()
    ts.with_stddev().as_csv()
    ts.with_stddev().as_pandas()
    ts.with_stddev().as_plotly_figure()
    ts.with_stddev().as_url()
    plt.close()


def test_time_series_get_stoch():
    ts = _init_ts()
    assert ts.with_stoch().as_json()
    ts.with_stoch().as_csv()
    ts.with_stoch().as_pandas()
    ts.with_stoch().as_plotly_figure()
    ts.with_stoch().as_url()
    plt.close()


def test_time_series_get_stochf():
    ts = _init_ts()
    assert ts.with_stochf().as_json()
    ts.with_stochf().as_csv()
    ts.with_stochf().as_pandas()
    ts.with_stochf().as_plotly_figure()
    ts.with_stochf().as_url()
    plt.close()


def test_time_series_get_stochrsi():
    ts = _init_ts()
    assert ts.with_stochrsi().as_json()
    ts.with_stochrsi().as_csv()
    ts.with_stochrsi().as_pandas()
    ts.with_stochrsi().as_plotly_figure()
    ts.with_stochrsi().as_url()
    plt.close()


def test_time_series_get_supertrend():
    ts = _init_ts()
    assert ts.with_supertrend().as_json()
    ts.with_supertrend().as_csv()
    ts.with_supertrend().as_pandas()
    ts.with_supertrend().as_plotly_figure()
    ts.with_supertrend().as_url()
    plt.close()


def test_time_series_get_t3ma():
    ts = _init_ts()
    assert ts.with_t3ma().as_json()
    ts.with_t3ma().as_csv()
    ts.with_t3ma().as_pandas()
    ts.with_t3ma().as_plotly_figure()
    ts.with_t3ma().as_url()
    plt.close()


def test_time_series_get_tema():
    ts = _init_ts()
    assert ts.with_tema().as_json()
    ts.with_tema().as_csv()
    ts.with_tema().as_pandas()
    ts.with_tema().as_plotly_figure()
    ts.with_tema().as_url()
    plt.close()


def test_time_series_get_trange():
    ts = _init_ts()
    assert ts.with_trange().as_json()
    ts.with_trange().as_csv()
    ts.with_trange().as_pandas()
    ts.with_trange().as_plotly_figure()
    ts.with_trange().as_url()
    plt.close()


def test_time_series_get_trima():
    ts = _init_ts()
    assert ts.with_trima().as_json()
    ts.with_trima().as_csv()
    ts.with_trima().as_pandas()
    ts.with_trima().as_plotly_figure()
    ts.with_trima().as_url()
    plt.close()


def test_time_series_get_tsf():
    ts = _init_ts()
    assert ts.with_tsf().as_json()
    ts.with_tsf().as_csv()
    ts.with_tsf().as_pandas()
    ts.with_tsf().as_plotly_figure()
    ts.with_tsf().as_url()
    plt.close()


def test_time_series_get_typprice():
    ts = _init_ts()
    assert ts.with_typprice().as_json()
    ts.with_typprice().as_csv()
    ts.with_typprice().as_pandas()
    ts.with_typprice().as_plotly_figure()
    ts.with_typprice().as_url()
    plt.close()


def test_time_series_get_ultosc():
    ts = _init_ts()
    assert ts.with_ultosc().as_json()
    ts.with_ultosc().as_csv()
    ts.with_ultosc().as_pandas()
    ts.with_ultosc().as_plotly_figure()
    ts.with_ultosc().as_url()
    plt.close()


def test_time_series_get_var():
    ts = _init_ts()
    assert ts.with_var().as_json()
    ts.with_var().as_csv()
    ts.with_var().as_pandas()
    ts.with_var().as_plotly_figure()
    ts.with_var().as_url()
    plt.close()


def test_time_series_get_vwap():
    ts = _init_ts()
    assert ts.with_vwap().as_json()
    ts.with_vwap().as_csv()
    ts.with_vwap().as_pandas()
    ts.with_vwap().as_plotly_figure()
    ts.with_vwap().as_url()
    plt.close()


def test_time_series_get_wclprice():
    ts = _init_ts()
    assert ts.with_wclprice().as_json()
    ts.with_wclprice().as_csv()
    ts.with_wclprice().as_pandas()
    ts.with_wclprice().as_plotly_figure()
    ts.with_wclprice().as_url()
    plt.close()


def test_time_series_get_willr():
    ts = _init_ts()
    assert ts.with_willr().as_json()
    ts.with_willr().as_csv()
    ts.with_willr().as_pandas()
    ts.with_willr().as_plotly_figure()
    ts.with_willr().as_url()
    plt.close()


def test_time_series_get_wma():
    ts = _init_ts()
    assert ts.with_wma().as_json()
    ts.with_wma().as_csv()
    ts.with_wma().as_pandas()
    ts.with_wma().as_plotly_figure()
    ts.with_wma().as_url()
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
        .with_beta()
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
    assert chart.as_json()


def test_chart_csv():
    chart = _init_chart()
    chart.as_csv()


def test_chart_pandas():
    chart = _init_chart()
    chart.as_pandas()


def test_chart_url():
    chart = _init_chart()
    chart.as_url()


# def test_chart_plot():
#     chart = _init_chart()
#     chart.as_plotly_figure()
    # plt.close()


def test_string_batch():
    batch_ts = _init_batch_ts('AAPL,QQQ,EUR/USD,BTC/USD,')
    assert batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()
    batch_ts.with_ema().with_bbands().as_url()


def test_list_batch():
    batch_ts = _init_batch_ts(['AAPL', 'QQQ', 'EUR/USD', 'BTC/USD'])
    assert batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()
    batch_ts.with_ema().with_bbands().as_url()


def test_tuple_batch():
    batch_ts = _init_batch_ts(('AAPL', 'QQQ', 'EUR/USD', 'BTC/USD'))
    assert batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()
    batch_ts.with_ema().with_bbands().as_url()


def test_tuple_batch_one_symbol():
    batch_ts = _init_batch_ts(('AAPL',))
    assert batch_ts.with_macd().with_stoch().as_json()
    batch_ts.with_ema().with_bbands().as_pandas()
    batch_ts.with_ema().with_bbands().as_url()


@patch('twelvedata.http_client.Session.get', return_value=_fake_resp(500))
def test_http_internal_server_error_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InternalServerError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 500, "message": "error message"}')),
)
def test_http_internal_server_error_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InternalServerError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_resp(400))
def test_http_bad_request_error_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(BadRequestError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 400, "message": "error message"}')),
       )
def test_http_bad_request_error_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(BadRequestError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_resp(401))
def test_http_invalid_api_key_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InvalidApiKeyError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 401, "message": "error message"}')),
       )
def test_http_invalid_api_key_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(InvalidApiKeyError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_resp(520))
def test_http_other_invalid_response(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(TwelveDataError):
        http_client.get('/fake_url')
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


@patch('twelvedata.http_client.Session.get', return_value=_fake_json_resp(
    json.loads('{"status": "error", "code": 520, "message": "error message"}')),
       )
def test_http_other_invalid_response_in_json(mock_get):
    http_client = DefaultHttpClient(API_URL)
    with pytest.raises(TwelveDataError) as err:
        http_client.get('/fake_url')
        assert str(err) == 'error message'
    mock_get.assert_called_once_with(API_URL + '/fake_url', timeout=30, params={'source': 'python'})


def test_identifiers_threaded_through_time_series_and_indicators():
    td = _init_client()
    ts = td.time_series(
        symbol='AAPL', interval='1min',
        figi='BBG000B9XRY4', isin='US0378331005', cusip='037833100',
    ).with_macd().with_rsi()
    for url in ts.as_url():
        assert 'figi=BBG000B9XRY4' in url
        assert 'isin=US0378331005' in url
        assert 'cusip=037833100' in url


def test_identifiers_on_individual_indicator_do_not_leak_to_base():
    td = _init_client()
    base_url, rsi_url = td.time_series(
        symbol='AAPL', interval='1min',
    ).with_rsi(figi='OVERRIDE').as_url()
    assert 'figi=' not in base_url
    assert 'figi=OVERRIDE' in rsi_url


def test_get_dividends_threads_identifiers():
    td = _init_client()
    url = td.get_dividends(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


def test_get_splits_threads_identifiers():
    td = _init_client()
    url = td.get_splits(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


def test_get_income_statement_threads_identifiers():
    td = _init_client()
    url = td.get_income_statement(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


def test_get_key_executives_threads_identifiers():
    td = _init_client()
    url = td.get_key_executives(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


def test_quote_threads_identifiers():
    td = _init_client()
    url = td.quote(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


def test_price_threads_identifiers():
    td = _init_client()
    url = td.price(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url


# ---------------------------------------------------------------------------
# Reference data endpoints
# ---------------------------------------------------------------------------

def test_get_exchange_schedule():
    td = _init_client()
    assert '/exchange_schedule' in td.get_exchange_schedule(country='United States').as_url()
    assert not td.get_exchange_schedule(country='United States').as_pandas().empty


def test_get_countries():
    td = _init_client()
    assert '/countries' in td.get_countries().as_url()
    assert td.get_countries().as_json()
    assert not td.get_countries().as_pandas().empty


def test_get_cross_listings():
    td = _init_client()
    assert '/cross_listings?symbol=AAPL' in td.get_cross_listings(symbol='AAPL').as_url()
    assert td.get_cross_listings(symbol='AAPL').as_json()
    assert not td.get_cross_listings(symbol='AAPL').as_pandas().empty


def test_get_intervals():
    td = _init_client()
    assert '/intervals' in td.get_intervals().as_url()
    assert td.get_intervals().as_json()
    assert not td.get_intervals().as_pandas().empty


def test_get_instrument_type():
    td = _init_client()
    assert '/instrument_type' in td.get_instrument_type().as_url()
    assert td.get_instrument_type().as_json()
    assert not td.get_instrument_type().as_pandas().empty


# ---------------------------------------------------------------------------
# Market data endpoints
# ---------------------------------------------------------------------------

def test_time_series_cross():
    td = _init_client()
    url = td.time_series_cross(base='USD', quote='EUR', interval='1day').as_url()
    assert 'base=USD' in url
    assert 'quote=EUR' in url
    assert 'interval=1day' in url
    assert td.time_series_cross(base='USD', quote='EUR', interval='1day').as_json()
    df = td.time_series_cross(base='USD', quote='EUR', interval='1day').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_market_movers():
    td = _init_client()
    url = td.get_market_movers(market='stocks', direction='gainers').as_url()
    assert '/market_movers/stocks' in url
    assert 'direction=gainers' in url
    assert not td.get_market_movers(market='stocks', direction='gainers').as_pandas().empty


# ---------------------------------------------------------------------------
# Fundamentals endpoints
# ---------------------------------------------------------------------------

def test_get_income_statement_consolidated():
    td = _init_client()
    url = td.get_income_statement_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_income_statement_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_income_statement_consolidated(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_balance_sheet_consolidated():
    td = _init_client()
    url = td.get_balance_sheet_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_balance_sheet_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_balance_sheet_consolidated(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_cash_flow_consolidated():
    td = _init_client()
    url = td.get_cash_flow_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_cash_flow_consolidated(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_cash_flow_consolidated(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_market_cap():
    td = _init_client()
    url = td.get_market_cap(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_market_cap(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_market_cap(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_press_releases():
    td = _init_client()
    url = td.get_press_releases(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_press_releases(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_press_releases(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_last_change():
    td = _init_client()
    url = td.get_last_change(endpoint='logo', symbol='AAPL').as_url()
    assert '/last_change/logo' in url
    assert 'symbol=AAPL' in url
    assert td.get_last_change(endpoint='logo', symbol='AAPL').as_json() is not None
    td.get_last_change(endpoint='logo', symbol='AAPL').as_pandas()


# ---------------------------------------------------------------------------
# Analysis endpoints
# ---------------------------------------------------------------------------

def test_get_analyst_ratings_light():
    td = _init_client()
    url = td.get_analyst_ratings_light(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_analyst_ratings_light(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_analyst_ratings_light(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_analyst_ratings_us_equities():
    td = _init_client()
    url = td.get_analyst_ratings_us_equities(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_analyst_ratings_us_equities(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_analyst_ratings_us_equities(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_earnings_estimate():
    td = _init_client()
    url = td.get_earnings_estimate(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_earnings_estimate(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_earnings_estimate(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_revenue_estimate():
    td = _init_client()
    url = td.get_revenue_estimate(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_revenue_estimate(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_revenue_estimate(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_eps_trend():
    td = _init_client()
    url = td.get_eps_trend(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_eps_trend(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_eps_trend(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_eps_revisions():
    td = _init_client()
    url = td.get_eps_revisions(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_eps_revisions(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    df = td.get_eps_revisions(symbol='AAPL').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_growth_estimates():
    td = _init_client()
    url = td.get_growth_estimates(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_growth_estimates(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_growth_estimates(symbol='AAPL').as_pandas()) >= 1


def test_get_price_target():
    td = _init_client()
    url = td.get_price_target(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_price_target(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_price_target(symbol='AAPL').as_pandas()) >= 1


def test_get_recommendations():
    td = _init_client()
    url = td.get_recommendations(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_recommendations(symbol='AAPL', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_recommendations(symbol='AAPL').as_pandas()) >= 1


# ---------------------------------------------------------------------------
# Regulatory endpoints
# ---------------------------------------------------------------------------

def test_get_direct_holders():
    td = _init_client()
    url = td.get_direct_holders(symbol='AAPL', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_direct_holders(symbol='AAPL', figi='F', isin='I', cusip='C').as_json() is not None
    td.get_direct_holders(symbol='AAPL').as_pandas()


def test_get_edgar_filings_archive():
    td = _init_client()
    url = td.get_edgar_filings_archive(symbol='AAPL', form_type='10-K').as_url()
    assert '/edgar_filings/archive' in url
    assert 'form_type=10-K' in url
    assert td.get_edgar_filings_archive(symbol='AAPL', form_type='10-K').as_json()
    df = td.get_edgar_filings_archive(symbol='AAPL', form_type='10-K').as_pandas()
    assert isinstance(df.index, pd.DatetimeIndex)


def test_get_sanctions():
    td = _init_client()
    assert '/sanctions/ofac' in td.get_sanctions(source='ofac').as_url()
    assert not td.get_sanctions(source='ofac').as_pandas().empty


def test_get_tax_info():
    td = _init_client()
    assert '/tax_info' in td.get_tax_info(symbol='AAPL').as_url()
    assert td.get_tax_info(symbol='AAPL').as_json()
    assert len(td.get_tax_info(symbol='AAPL').as_pandas()) >= 1


# ---------------------------------------------------------------------------
# Options endpoints (deprecated)
# ---------------------------------------------------------------------------

def test_get_options_expiration():
    td = _init_client()
    with pytest.warns(FutureWarning):
        ep = td.get_options_expiration(symbol='AAPL')
    assert '/options/expiration' in ep.as_url()


def test_get_options_chain():
    td = _init_client()
    with pytest.warns(FutureWarning):
        ep = td.get_options_chain(symbol='AAPL')
    assert '/options/chain' in ep.as_url()


# ---------------------------------------------------------------------------
# ETFs endpoints
# ---------------------------------------------------------------------------

def test_get_etfs_world():
    td = _init_client()
    url = td.get_etfs_world(symbol='VOO', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_etfs_world(symbol='VOO', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_etfs_world(symbol='VOO').as_pandas()) >= 1


def test_get_etfs_world_summary():
    td = _init_client()
    url = td.get_etfs_world_summary(symbol='VOO', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_etfs_world_summary(symbol='VOO', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_etfs_world_summary(symbol='VOO').as_pandas()) >= 1


def test_get_etfs_world_composition():
    td = _init_client()
    url = td.get_etfs_world_composition(symbol='VOO', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_etfs_world_composition(symbol='VOO', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_etfs_world_composition(symbol='VOO').as_pandas()) >= 1


def test_get_etfs_world_performance():
    td = _init_client()
    url = td.get_etfs_world_performance(symbol='VOO', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_etfs_world_performance(symbol='VOO', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_etfs_world_performance(symbol='VOO').as_pandas()) >= 1


def test_get_etfs_world_risk():
    td = _init_client()
    url = td.get_etfs_world_risk(symbol='VOO', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_etfs_world_risk(symbol='VOO', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_etfs_world_risk(symbol='VOO').as_pandas()) >= 1


def test_get_etfs_list():
    td = _init_client()
    assert '/etfs/list' in td.get_etfs_list(symbol='VOO').as_url()
    assert td.get_etfs_list(symbol='VOO').as_json()
    assert not td.get_etfs_list(symbol='VOO').as_pandas().empty


def test_get_etfs_type():
    td = _init_client()
    assert '/etfs/type' in td.get_etfs_type(country='US').as_url()
    assert td.get_etfs_type(country='US').as_json()
    assert not td.get_etfs_type(country='US').as_pandas().empty


def test_get_etfs_family():
    td = _init_client()
    assert '/etfs/family' in td.get_etfs_family(country='US').as_url()
    assert td.get_etfs_family(country='US').as_json()
    assert not td.get_etfs_family(country='US').as_pandas().empty


# ---------------------------------------------------------------------------
# Mutual funds endpoints
# ---------------------------------------------------------------------------

def test_get_mutual_funds_world():
    td = _init_client()
    url = td.get_mutual_funds_world(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_summary():
    td = _init_client()
    url = td.get_mutual_funds_world_summary(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_summary(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_summary(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_composition():
    td = _init_client()
    url = td.get_mutual_funds_world_composition(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_composition(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_composition(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_purchase_info():
    td = _init_client()
    url = td.get_mutual_funds_world_purchase_info(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_purchase_info(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_purchase_info(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_performance():
    td = _init_client()
    url = td.get_mutual_funds_world_performance(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_performance(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_performance(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_risk():
    td = _init_client()
    url = td.get_mutual_funds_world_risk(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_risk(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_risk(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_ratings():
    td = _init_client()
    url = td.get_mutual_funds_world_ratings(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_ratings(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_ratings(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_world_sustainability():
    td = _init_client()
    url = td.get_mutual_funds_world_sustainability(symbol='VFIAX', figi='F', isin='I', cusip='C').as_url()
    assert 'figi=F' in url and 'isin=I' in url and 'cusip=C' in url
    assert td.get_mutual_funds_world_sustainability(symbol='VFIAX', figi='F', isin='I', cusip='C').as_json()
    assert len(td.get_mutual_funds_world_sustainability(symbol='VFIAX').as_pandas()) >= 1


def test_get_mutual_funds_list():
    td = _init_client()
    assert '/mutual_funds/list' in td.get_mutual_funds_list(symbol='VFIAX').as_url()
    assert td.get_mutual_funds_list(symbol='VFIAX').as_json()
    assert not td.get_mutual_funds_list(symbol='VFIAX').as_pandas().empty


def test_get_mutual_funds_type():
    td = _init_client()
    assert '/mutual_funds/type' in td.get_mutual_funds_type(country='US').as_url()
    assert td.get_mutual_funds_type(country='US').as_json()
    assert not td.get_mutual_funds_type(country='US').as_pandas().empty


def test_get_mutual_funds_family():
    td = _init_client()
    assert '/mutual_funds/family' in td.get_mutual_funds_family(country='US').as_url()
    assert td.get_mutual_funds_family(country='US').as_json()
    assert not td.get_mutual_funds_family(country='US').as_pandas().empty


# ---------------------------------------------------------------------------
# Technical indicators: one test per with_* method.
# ---------------------------------------------------------------------------

def _indicator_url(td, method_name, **kwargs):
    ts = td.time_series(symbol='AAPL', interval='1min')
    ts = getattr(ts, method_name)(**kwargs)
    _, indicator_url = ts.as_url()
    return indicator_url


def test_with_add():
    td = _init_client()
    url = _indicator_url(td, 'with_add', series_type_1='high', series_type_2='low')
    assert '/add' in url
    assert 'series_type_1=high' in url
    assert 'series_type_2=low' in url


def test_with_sub():
    td = _init_client()
    url = _indicator_url(td, 'with_sub', series_type_1='high', series_type_2='low')
    assert '/sub' in url
    assert 'series_type_1=high' in url
    assert 'series_type_2=low' in url

def test_with_mult():
    td = _init_client()
    url = _indicator_url(td, 'with_mult', series_type_1='high', series_type_2='low')
    assert '/mult' in url
    assert 'series_type_1=high' in url
    assert 'series_type_2=low' in url


def test_with_div():
    td = _init_client()
    url = _indicator_url(td, 'with_div', series_type_1='high', series_type_2='low')
    assert '/div' in url
    assert 'series_type_1=high' in url
    assert 'series_type_2=low' in url


def test_with_sum():
    td = _init_client()
    url = _indicator_url(td, 'with_sum', time_period=20, series_type='open')
    assert '/sum' in url
    assert 'time_period=20' in url
    assert 'series_type=open' in url


def test_with_avg():
    td = _init_client()
    url = _indicator_url(td, 'with_avg', time_period=20, series_type='open')
    assert '/avg' in url
    assert 'time_period=20' in url
    assert 'series_type=open' in url


def test_with_crsi():
    td = _init_client()
    url = _indicator_url(
        td, 'with_crsi',
        rsi_period=5, up_down_length=3, percent_rank_period=50,
    )
    assert '/crsi' in url
    assert 'rsi_period=5' in url
    assert 'up_down_length=3' in url
    assert 'percent_rank_period=50' in url


def test_with_correl():
    td = _init_client()
    url = _indicator_url(
        td, 'with_correl',
        series_type_1='high', series_type_2='low', time_period=20,
    )
    assert '/correl' in url
    assert 'series_type_1=high' in url
    assert 'series_type_2=low' in url
    assert 'time_period=20' in url


def test_with_dpo():
    td = _init_client()
    url = _indicator_url(td, 'with_dpo', time_period=20, centered='true')
    assert '/dpo' in url
    assert 'time_period=20' in url
    assert 'centered=true' in url


def test_with_sarext():
    td = _init_client()
    url = _indicator_url(
        td, 'with_sarext',
        start_value=0.01, offset_on_reverse=0.02,
        acceleration_limit_long=0.03, acceleration_long=0.04,
        acceleration_max_long=0.5, acceleration_limit_short=0.06,
        acceleration_short=0.07, acceleration_max_short=0.6,
    )
    assert '/sarext' in url
    for key in (
        'start_value=0.01', 'offset_on_reverse=0.02',
        'acceleration_limit_long=0.03', 'acceleration_long=0.04',
        'acceleration_max_long=0.5', 'acceleration_limit_short=0.06',
        'acceleration_short=0.07', 'acceleration_max_short=0.6',
    ):
        assert key in url, f'missing {key} in {url}'


def test_with_supertrend_heikinashicandles():
    td = _init_client()
    url = _indicator_url(
        td, 'with_supertrend_heikinashicandles', period=14, multiplier=2,
    )
    assert '/supertrend_heikinashicandles' in url
    assert 'period=14' in url
    assert 'multiplier=2' in url


def test_with_macd_slope():
    td = _init_client()
    url = _indicator_url(td, 'with_macd_slope')
    assert '/macd_slope' in url


def test_with_pivot_points_hl():
    td = _init_client()
    url = _indicator_url(td, 'with_pivot_points_hl')
    assert '/pivot_points_hl' in url


def test_with_rvol():
    td = _init_client()
    url = _indicator_url(td, 'with_rvol')
    assert '/rvol' in url


# ---------------------------------------------------------------------------
# Error response handling: API returns {"status": "error", ...} with HTTP 200.
# DefaultHttpClient.get raises before reaching as_json/as_pandas, but we want
# the exception to propagate cleanly through both serializers.
# ---------------------------------------------------------------------------

class _PatcherGroup:
    def __init__(self, patchers):
        self._patchers = patchers

    def stop(self):
        for p in self._patchers:
            p.stop()


def _error_client(error_code, message='error message'):
    # Skip the metadata fetch on TDClient construction so the Session.get patch
    # below isn't intercepted by it. Patch the binding in twelvedata.client
    # (where it's imported), not twelvedata.utils, and stop both patchers in the
    # caller's finally so module-global state isn't mutated.
    body = {'status': 'error', 'code': error_code, 'message': message}
    fake_resp = _fake_json_resp(body)
    session_patcher = patch('twelvedata.http_client.Session.get', return_value=fake_resp)
    meta_patcher = patch('twelvedata.client.patch_endpoints_meta', lambda ctx: None)
    session_patcher.start()
    meta_patcher.start()
    td = TDClient('demo', http_client=DefaultHttpClient(API_URL))
    return _PatcherGroup([session_patcher, meta_patcher]), td


def test_as_json_propagates_invalid_api_key_error():
    patcher, td = _error_client(401)
    try:
        with pytest.raises(InvalidApiKeyError):
            td.get_splits(symbol='AAPL').as_json()
    finally:
        patcher.stop()


def test_as_pandas_propagates_invalid_api_key_error():
    patcher, td = _error_client(401)
    try:
        with pytest.raises(InvalidApiKeyError):
            td.get_splits(symbol='AAPL').as_pandas()
    finally:
        patcher.stop()


def test_as_json_propagates_bad_request_error():
    patcher, td = _error_client(400)
    try:
        with pytest.raises(BadRequestError):
            td.get_dividends(symbol='AAPL').as_json()
    finally:
        patcher.stop()


def test_as_pandas_propagates_bad_request_error():
    patcher, td = _error_client(400)
    try:
        with pytest.raises(BadRequestError):
            td.get_balance_sheet(symbol='AAPL').as_pandas()
    finally:
        patcher.stop()


def test_as_json_propagates_internal_server_error():
    patcher, td = _error_client(500)
    try:
        with pytest.raises(InternalServerError):
            td.time_series(symbol='AAPL', interval='1day').as_json()
    finally:
        patcher.stop()


def test_as_pandas_propagates_generic_error():
    patcher, td = _error_client(429, message='rate limit exceeded')
    try:
        with pytest.raises(TwelveDataError):
            td.quote(symbol='AAPL').as_pandas()
    finally:
        patcher.stop()


def test_as_json_returns_error_dict_when_http_client_does_not_raise():
    # Custom http_client that does not raise on JSON-level errors — exercises the
    # `if json.get("status") == "error": return json` branch in AsJsonMixin.
    error_payload = {'status': 'error', 'code': 400, 'message': 'bad symbol'}
    fake_resp = _fake_json_resp(error_payload)

    class PassthroughHttpClient(DefaultHttpClient):
        def get(self, *args, **kwargs):
            return fake_resp

    td = TDClient('demo', http_client=PassthroughHttpClient(API_URL))
    assert td.get_splits(symbol='AAPL').as_json() == error_payload
