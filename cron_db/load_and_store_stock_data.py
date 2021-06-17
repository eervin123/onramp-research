from datetime import timedelta
from typing import List
import itertools
import bt
import pandas as pd
from sqlalchemy.orm import Session
from tqdm import tqdm
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from models.close_data import CloseData
from models.session_context import db_session

TICKER_LIST = '../datafiles/tickerlist.csv'


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def create_close_data_objects(row):
    date = row['date']
    return [CloseData(symbol=index, close=value, date=date) for index, value in row.items() if index != 'date']


def get_and_insert_historical_data(tickers: List[str], db: Session):
    chunked_fetch = chunks(tickers, 10)
    for chunk in tqdm(chunked_fetch):
        multihistories = CloseData.get_multiple_histories(chunk, db)
        start = '2017-01-01'
        if multihistories:
            multihistories.sort(key=lambda x: x.date)
            start = multihistories[-1].date + timedelta(days=1)
            start = start.strftime("%Y-%m-%d")
        fetched_tickers = bt.get(chunk, start=start)
        fetched_tickers['date'] = fetched_tickers.index
        close_data = fetched_tickers.apply(create_close_data_objects, axis=1)
        close_data = list(itertools.chain(*close_data))
        db.bulk_save_objects(close_data)
        db.commit()


with db_session() as db:
    tickers = pd.read_csv(TICKER_LIST)['Ticker']
    tickers.dropna(inplace=True)
    get_and_insert_historical_data(tickers.tolist(), db)
