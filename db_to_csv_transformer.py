from collections import defaultdict

import pandas as pd

from models.session_context import db_session
from datetime import datetime
from models.cryptocurrency_pair_ohlcv import CryptocurrencyPairOHLCV
from models.close_data import CloseData
import pandas as pd


def eager_fetch_all_crypto_data():
    all_assets = []
    with db_session() as session:
        all_assets = session.query(CryptocurrencyPairOHLCV).all()

    def get_coin(coin):
        # Quick fix to convert it back to a timestamp to work with existing codepaths without complaining
        return pd.DataFrame([{**item.__dict__, **{'timestamp': datetime.timestamp(item.datetime)}} for item in all_assets if item.asset_1 == coin])[
            ["timestamp", "price_open", "price_high", "price_low", "price_close", "volume"]
        ].to_dict(orient="list")

    return get_coin

def eager_fetch_all_stock_data():
    all_assets = []
    with db_session() as session:
        all_assets = session.query(CloseData).all()

    dict_of_tickers = defaultdict(list)
    for item in all_assets:
        dict_of_tickers[item.symbol].append(item.__dict__)
    dict_of_frames = {}
    for key in dict_of_tickers.keys():
        dict_of_frames[key] = pd.DataFrame(dict_of_tickers[key])

    def get_stock(stock):
        return dict_of_frames[stock]

    return get_stock
