import pandas as pd

from models.session_context import db_session
from datetime import datetime
from models.cryptocurrency_pair_ohlcv import CryptocurrencyPairOHLCV
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