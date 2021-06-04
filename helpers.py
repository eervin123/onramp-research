import pandas as pd 

def get_coin_data(symbol):
    df = pd.read_csv(f"datafiles/{symbol}_data.csv")
    res = df[
        ["timestamp", "price_open", "price_high", "price_low", "price_close", "volume"]
    ].to_dict(orient="list")
    return res

def get_coin_data_new(symbol):
    df = pd.read_csv("datafiles/Multi_Asset_data.csv", usecols=["Timestamp", symbol])
    res = df.to_dict(orient="list")
    return res

def volatility(price, period_value, data_interval):
    """
    This function is used to calculate the annualized volatility for a given set of prices.
    Inputs:
       price: a pandas series/column of prices
       period_value: Number of days volatility is measured over (int). e.g 1,5,10,14,30
    returns:
       a pandas series of volatility measures
    """

    if data_interval not in ["1T", "30T", "1D", "30D", "60D", "7D"]:
        raise ValueError

    if data_interval == "1T":
        trading_periods = 60 * 24
    elif data_interval == "30T":
        trading_periods = 2 * 24
    elif data_interval == "1D":
        trading_periods = 1
    elif data_interval == "30D":
        trading_periods = 30
    elif data_interval == "60D":
        trading_periods = 60
    elif data_interval == "7D":
        trading_periods = 60

    percent_change = price.pct_change() * 100
    standard_deviation = percent_change.rolling(period_value * trading_periods).std()
    # formula sqrt(to_hour * daily_hours * days)
    volatility = standard_deviation * ((trading_periods * 365) ** 0.5)
    return volatility

def calc_volatility(pairs):
    """
    Get Graph For Each Coin You Want
    """
    # create visuals

    df_all = dict()
    for sp in pairs:
        # calculate vol for each coin and graph
        tmp = pd.DataFrame(get_coin_data(sp))
        tmp = tmp[["price_close", "timestamp"]]
        tmp.timestamp = pd.to_datetime(tmp.timestamp, unit="s")
        tmp.set_index("timestamp", inplace=True)
        for t in [14, 30, 90]:
            df_all[f'{sp.split("-",1)[0]}_vol_{t}'] = volatility(
                tmp.price_close, t, data_interval= "1D"
            )

    return pd.DataFrame(df_all).dropna(how="all")

def calc_volatility_btc_vol(pairs):
    """
    Get Graph For Each Coin You Want
    """
    # create visuals

    df_all = dict()
    for sp in pairs:
        # calculate vol for each coin and graph
        tmp = pd.DataFrame(get_coin_data(sp))
        tmp = tmp[["price_close", "timestamp"]]
        tmp.timestamp = pd.to_datetime(tmp.timestamp, unit="s")
        tmp.set_index("timestamp", inplace=True)
        for t in [14, 30, 90, 7, 60]:
            df_all[f'{sp.split("-",1)[0]}_vol_{t}'] = volatility(
                tmp.price_close, t, data_interval= "1D"
            )

    return pd.DataFrame(df_all).dropna(how="all")

def calc_volatility_new(pairs):
    """
    Get Graph For Each Coin You Want
    """
    # create visuals

    df_all = dict()
    for sp in pairs:
        # calculate vol for each coin and graph
        tmp = pd.DataFrame(get_coin_data_new(sp))
        tmp = tmp[[sp, "Timestamp"]]
        tmp.set_index("Timestamp", inplace=True)
        tmp.index = pd.to_datetime(tmp.index, unit="s")
        for t in [14, 30, 90]:
            df_all[f'{sp.split("-",1)[0]}_vol_{t}'] = volatility(
                tmp.iloc[:, 0], t, data_interval="1D"
            )

    return pd.DataFrame(df_all).dropna(how="all")

def create_corr(pairs):
    vals = dict()
    for sp in pairs:
        data = get_coin_data(sp)
        if len(data) < 6:  # bad data
            print(sp, " ", len(data))
            continue
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        vals[sp] = df.price_close

    df_ = pd.DataFrame(vals)
    df_.index = pd.to_datetime(df_.index, unit="s")
    df_ = df_.pct_change(1).fillna(0)
    df_.columns = [col.split("-", 1)[0] for col in df_.columns]
    df_ = df_.round(3).rolling(180).corr().dropna(how="all")

    return df_

def create_corr_new(pairs):
    vals = dict()
    for sp in pairs:
        data = get_coin_data_new(sp)
        # if(len(data)<6): #bad data
        #     print(sp, " ", len(data))
        #     continue
        df = pd.DataFrame(data)
        df.set_index("Timestamp", inplace=True)
        vals[sp] = df[sp]

    df_ = pd.DataFrame(vals)
    df_.index = pd.to_datetime(df_.index, unit="s")
    df_ = df_.pct_change(1).fillna(0)
    df_.columns = [col.split("-", 1)[0] for col in df_.columns]
    df_ = df_.round(3).rolling(180).corr().dropna(how="all")

    return df_
