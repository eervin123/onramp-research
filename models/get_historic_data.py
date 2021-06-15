#!/usr/bin/env python3

import requests
import pandas as pd
from dateutil.parser import parse
from sqlalchemy.orm import Session
import datetime
from cryptocurrency_pair_ohlcv import CryptocurrencyPairOHLCV
from session_context import db_session
from datetime import datetime, timedelta

TICKER_MAPPING = {
    'ETH': 'ethereum',
    'EOS': 'eos',
    'USDT': 'tether',
    'TRX': 'tron',
    'IOTA': 'iota',
    'XLM': 'stellar',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'NEO': 'neo',
    'BCHABC': 'bitcoin-cash',
    'BNB': 'binance-coin',
    'BTC': 'bitcoin'
}


def get_and_insert_historical_data(symbol: str, ts_start: float, session: Session):
    base, quote = symbol.split('-')

    baseId = TICKER_MAPPING[base]
    quoteId = TICKER_MAPPING[quote]

    historical_data = list(CryptocurrencyPairOHLCV.get_all_history_for_pair(quoteId, baseId, session))
    start_time = ts_start
    if historical_data:
        historical_data.sort(key=lambda x: x.datetime)
        start_time = historical_data[-1].datetime
        # Add another day to our last datetime found
        start_time = datetime.timestamp(start_time + timedelta(days=1))

    if datetime.fromtimestamp(start_time) > datetime.now():
        return historical_data

    url = "https://api.coincap.io/v2/candles?exchange=binance&interval=d1" \
          f"&baseId={baseId}&quoteId={quoteId}" \
          f"&start={int(start_time) * 1000}" \
          f"&end={datetime.timestamp(datetime.now()) * 1000}"

    response = requests.get(url)
    if response.status_code > 300:
        raise Exception("Invalid response code returned: " + str(response.status_code))
    res = response.json()
    if not res['data']:
        raise Exception("No response body returned for: " + symbol)
    items = [
        CryptocurrencyPairOHLCV(asset_1=quoteId, asset_2=baseId, price_close=item['close'], price_high=item['high'],
                                price_low=item['low'], price_open=item['open'], volume=item['volume'],
                                datetime=datetime.fromtimestamp(item['period'] / 1000))
        for item in res['data']]
    session.bulk_save_objects(items)
    session.commit()
    total_data = historical_data + items
    df = pd.DataFrame(
        [{'open': item.price_open,
          'close': item.price_close,
          'low': item.price_low,
          'high': item.price_high,
          'period': item.datetime
          } for item in total_data]
    )
    df.to_csv(f'{symbol}_data.csv', index=False, header=True)

API_LIMIT = 700
ts_start = datetime.timestamp(datetime.now() - timedelta(days=API_LIMIT))
pairs = ['BTC-USDT', 'BCHABC-USDT', 'TRX-USDT', 'IOTA-USDT', 'XLM-USDT', 'EOS-USDT', 'XRP-USDT', 'ADA-USDT', 'LTC-USDT',
         'NEO-USDT', 'BNB-USDT', 'ETH-USDT']
for pair in pairs:
    with db_session() as db:
        try:
            get_and_insert_historical_data(pair, ts_start, db)
        except Exception as err:
            print(err)
