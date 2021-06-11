from direct_redis import DirectRedis
import urllib.parse as urlparse
from datetime import timedelta
import pandas as pd
import bt
import numpy as np

url = urlparse.urlparse('redis://default:mUtpOEwJc2F8tHYOGxF9JGvnIwHY3unu@redis-16351.c263.us-east-1-2.ec2.cloud.redislabs.com:16351')
r = DirectRedis(host=url.hostname, port=url.port, password=url.password)


r.flushdb()
print(r.keys())

stock_df = pd.read_csv('datafiles/tickerlist.csv')
stock_df = stock_df.dropna(how = "all")


for ticker in stock_df["Ticker"]:
    try:
        data_x = bt.get(ticker.lower(), start = '2017-01-01')
        r.set(ticker.lower(), data_x)
        r.expire(ticker.lower(), timedelta(seconds = 86400))
        print(ticker, "     set in cache")
    except:
        print(ticker, "ERRORRRRRRR")


for crypto in stock_df["Cryptos"]:
    if crypto is not np.nan:
        try:
            data_x = bt.get(crypto, start = '2017-01-01')
            r.set(crypto, data_x)
            r.expire(crypto, timedelta(seconds = 86400))
            print(crypto, "    set in cache")
        except:
            (crypto, "ERORRRRRRR")
