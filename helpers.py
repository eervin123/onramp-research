import pandas as pd 
import bt
import plotly.express as px
import plotly.graph_objects as go
from formatting import onramp_colors, onramp_template, onramp_template_dashboard

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

def get_data():
  s_data = bt.get('spy,agg', start = '2017-01-01') #took out gold for now because of error
  #cry_data = bt.get('btc-usd,eth-usd', start = '2017-01-01')
  btc = bt.get('btc-usd', start = '2017-01-01') #had to implement this seperatly because eth data got cut out one day on yahoo finance 
  data_cache = btc.join(s_data, how='outer')
  data_cache = data_cache.dropna()
  return data_cache #TODO: #5 @cyrus something is messed up with this. AGG is reading in as zero

def calculate_controls(data):
    # TODO @cyrus It looks like you were using VWO not AGG for the bond portion I made the change but please confirm you agree.
  stock_dic_control = {'spy': float(60)/100, 'agg': float(40)/100}
  stock_dic_spy = {'spy': float(100)/100}
  stock_dic_agg = {'agg': float(100)/100}
                            
  strategy_control = bt.Strategy('60-40 Portfolio', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_control),
                          bt.algos.Rebalance()]) #Creating strategy
  strategy_spy = bt.Strategy('SPY', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_spy),
                          bt.algos.Rebalance()]) #Creating strategy
  strategy_agg = bt.Strategy('AGG', 
                          [bt.algos.RunMonthly(), 
                          bt.algos.SelectAll(), 
                          bt.algos.WeighSpecified(**stock_dic_agg),
                          bt.algos.Rebalance()]) #Creating strategy
  test_control = bt.Backtest(strategy_control, data)
  results_control = bt.run(test_control)
  
  test_spy = bt.Backtest(strategy_spy, data)
  results_spy = bt.run(test_spy)
  
  test_agg = bt.Backtest(strategy_agg, data)
  results_agg = bt.run(test_agg)

  results_return = [results_control, results_spy, results_agg]

  return results_return 

def line_chart(results_list):
    result_final = pd.DataFrame()
    for i in range(len(results_list)):

        temp = results_list[i]._get_series(None).rebase()
        result_final = pd.concat([result_final, temp], axis = 1) #result dataframe
        #color_dict[result_final.columns[i]] = colors[i] #colors

    fig = px.line(result_final, labels=dict(index="<b>Click Legend Icons to Toggle Viewing<b>", value="", variable=""),
                    title="",
                    template= onramp_template
                    #height = 350
                    )
    
    fig.update_yaxes( # the y-axis is in dollars
        tickprefix="$",
        type = 'log',
        dtick = 1,
        nticks = 20

    )
    # fig.update_layout(
    #     legend = {
    #         "xanchor": "left",
    #         "x": .2,
    #     }  
    # )
    return fig

def plotly_pie(stock_list, percent_list):
    for i in range(len(stock_list)):
        stock_list[i] = stock_list[i].upper()
    fig = px.pie( values = percent_list, names = stock_list, color = stock_list, template = onramp_template, hole = .3)
    
    fig.update_traces(textfont_size=17, marker=dict( line=dict(color='white', width=1)))
    fig.update_layout(font = dict(color = "white"))
    

    return fig
    
def results_to_df(results_list):
    df_list = [] #list of completed dataframes
    
    for x in results_list:
        string_res = x.to_csv(sep=',') #This creates string of results stats 
        df = pd.DataFrame([x.split(',') for x in string_res.split('\n')]) # Takes the string and creates a dataframe 
        nan_value = float("NaN") 
        df.replace("", nan_value, inplace=True) #lot of empty collumns in dataframe, this makes the empty go to null("NaN")
        df.dropna(how='all', axis=1, inplace=True) #delete null collumns
        df = df.dropna()

        df_list.append(df)
    
    return df_list

def display_stats_combined(results_list): #works for list of two results df 
    
    df_list = results_to_df(results_list) #The results arent dataframes, so need to make them dataframes
    
    stats_combined = pd.concat([df_list[0], df_list[1]], axis=1) #this combines them 
    stats_combined.columns = ['Stats', 'Strategy 1', 'Drop', "Strategy 2"]
    stats_combined = stats_combined.drop(['Drop'], axis =1 )

    return stats_combined

def scatter_plot(results_list):
    results_df = results_to_df(results_list)
    xaxis_vol = []
    yaxis_return = []
    for x in results_df: #fill in two lists with the vol and return %s 
        xaxis_vol.append(float(x.iloc[30][1].replace('%', '')))
        yaxis_return.append(float(x.iloc[29][1].replace('%', '')))
    
    size_list =[]
    for i in range(len(xaxis_vol)): #getting errors on the number of sizes
        size_list.append(4)
    
    labels = []
    for i in results_df:
        labels.append(i.iloc[0][1])
    
    fig = px.scatter( x= xaxis_vol, y= yaxis_return, size = size_list, color = labels,
                            labels={
                            "x": "<b>Monthly Vol (ann.) %<b>",
                            "y": "<b>Monthly Mean (ann.) %<b>",
                            "color" : ""
                            },
                            title="", 
                            template= onramp_template,
                            #width = 530, height = 350
                            )
    #fig.update_layout(legend = {"y": -.38})
    
    return fig

def balance_table(results, results_con):
    labels = ['<b>Strategy<b>', '<b>Initial Investment<b>', '<b>Final Balance<b>']
    series_res = results._get_series(None).rebase()
    series_con = results_con._get_series(None).rebase()
    final_res = round(series_res.iloc[-1])
    final_con = round(series_con.iloc[-1])
    final_res = '$' + str(int(final_res)) #this line gets the $, but the initial final_res is a dataframe object type so this line is neccesary for the $
    final_con = '$' + str(int(final_con))

    name = series_res.columns[0]
    text_color = ['white', onramp_colors['btc']]

    fig = go.Figure(data=[go.Table(
                                header=dict(values= labels,
                                            line_color= 'rgba(100, 100, 100, 0.36)',
                                            fill_color= onramp_colors['cyan'],
                                            align=['center','center'],
                                            font=dict(color='black', size=12)),
                                cells=dict(values=[['60-40 Portfolio', series_res.columns[0]], ["$100", "$100"], [final_con, final_res]],
                                            line_color = 'rgba(100, 100, 100, 0.36)',
                                            font = dict(color = [text_color*3], size = 12),
                                            height = 26,
                                            fill_color = onramp_colors["dark_blue"] )) ])
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
    fig.update_layout(margin = dict(l=1, r=1, t=0, b=0))
    
    return fig

def short_stats_table(results_list):
    stats_0 = results_list[0].display_lookback_returns() #these objects are the dataframes we want, just need to combine them and-
    stats_1 = results_list[1].display_lookback_returns()   #make them into a nice table


    labels= ["<b>Stats<b>", '<b>'+ stats_0.columns[0] + '<b>', "<b>60-40 Portfolio<b>", "<b>Difference<b>"]

    #combining 
    stats_combined = pd.concat([stats_0, stats_1], axis=1)
    stats_combined.columns = ['Your_Strategy', "Portfolio6040"]
    stats_combined = stats_combined.dropna()
    
    #adding new row of differences
    stats_combined['Difference'] = stats_combined.apply(lambda row: 
                                        str(round(float(row.Your_Strategy.replace('%', ''))- float(row.Portfolio6040.replace('%', '')), 2)) + '%', axis = 1)  

    text_color = []
    n = len(stats_combined)
    for col in stats_combined:
        if col!='Portfolio6040':
            text_color.append(["white"] * n)
        else:
            text_color.append(onramp_colors['btc'])
    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'rgba(100, 100, 100, 0.36)',
                                        fill_color= onramp_colors['cyan'],
                                        align=['center','center'],
                                        font=dict(color='black', size=12)),
                            cells=dict(values=[stats_combined.index, stats_combined.Your_Strategy, stats_combined.Portfolio6040, stats_combined.Difference],
                                        line_color = 'rgba(100, 100, 100, 0.36)',
                                        height = 26,
                                        font = dict(color = text_color),
                                        fill_color = onramp_colors["dark_blue"] )) ])
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
    fig.update_layout(margin = dict(l=2, r=1, t=0, b=0))
    
    return fig

def monthly_table(results_list):

    

    key = results_list[0]._get_backtest(0) #syntax for getting the monthly returns data frame 
    res_mon = results_list[0][key].return_table
    df_r = pd.DataFrame(res_mon)

    keyc = results_list[1]._get_backtest(0)  
    res_con = results_list[1][keyc].return_table
    df_c = pd.DataFrame(res_con)

    keys = results_list[2]._get_backtest(0) #syntax for getting the monthly returns data frame 
    res_spy = results_list[2][keys].return_table
    df_s = pd.DataFrame(res_spy)

    keya = results_list[3]._get_backtest(0)  
    res_agg = results_list[3][keya].return_table
    df_a = pd.DataFrame(res_agg)

    strategy_color = '#A90BFE'
    P6040_color = '#FF7052'
    spy_color = '#66F3EC'
    agg_color = '#67F9AF'
    label_color = onramp_colors['cyan']
    bg_color = onramp_colors["dark_blue"]

    #hard part of this is combining
    index = res_mon.index
    index = index.tolist()
    
    
    year_rows =[] #create a list of the rows of year month month YTD
    for i in range(len(res_mon.index)):
        temp = []
        temp.append(index[i])
        temp.append("Jan")
        temp.append("Feb")
        temp.append("Mar")
        temp.append("Apr")
        temp.append("May")
        temp.append("Jun")
        temp.append("Jul")
        temp.append("Aug")
        temp.append("Sep")
        temp.append("Oct")
        temp.append("Nov")
        temp.append("Dec")
        temp.append("YTD")
        year_rows.append(temp)


    df_results = results_to_df(results_list) #doing this because we need to get the correct name of the strategy
    res_rows = [] #this creates the list of the "Your Strategy" then all the numbers
    for i in range(len(res_mon.index)):
        temp = []
        temp += [df_results[0].iloc[0][1]]
        for j in range(len(res_mon.columns)):
            temp += [str(round(df_r.iloc[i][j]*100, 2)) + '%']
        res_rows.append(temp)
    
    con_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_con.index)):
        temp = []
        temp += [df_results[1].iloc[0][1]]
        for j in range(len(res_con.columns)):
            temp += [str((round(df_c.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        con_rows.append(temp)

    spy_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_spy.index)):
        temp = []
        temp += ["SPY"]
        for j in range(len(res_spy.columns)):
            temp += [str((round(df_s.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        spy_rows.append(temp)
    
    agg_rows = [] #this creates the list of the "60-40 Portfolio " then all the numbers
    for i in range(len(res_agg.index)):
        temp = []
        temp += ["AGG"]
        for j in range(len(res_agg.columns)):
            temp += [str((round(df_a.iloc[i][j] *100, 2))) + '%'] #this takes the value in, round to 2 decimal places, and adds the percent sign
        agg_rows.append(temp)

    length = len(year_rows)

    
    list_4_df = [] #appends the rows in the correct order
    for i in range(length):
        list_4_df.append(year_rows[(length-1)-i])
        list_4_df.append(res_rows[(length-1)-i])
        list_4_df.append(con_rows[(length-1)-i])
        list_4_df.append(spy_rows[(length-1)-i])
        list_4_df.append(agg_rows[(length-1)-i])
    
    label_row = year_rows[length-1] #grabs the label row
    for i in range (len(year_rows)): # this loop is to make all the labels bold
        for j in range(len(year_rows[0])):
            label_row[j] = str(label_row[j])
            label_row[j] = '<b>' + label_row[j] + '<b>'

            year_rows[i][j] = str(year_rows[i][j])
            year_rows[i][j] = '<b>' + year_rows[i][j] + '<b>'

    for i in range (len(res_rows)): # this loop is to make all the strategy titles bold 

        res_rows[i][0] = str(res_rows[i][0])
        res_rows[i][0] = '<b>' + res_rows[i][0] + '<b>'  

        con_rows[i][0] = str(con_rows[i][0])
        con_rows[i][0] = '<b>' + con_rows[i][0] + '<b>'   

        spy_rows[i][0] = str(spy_rows[i][0])
        spy_rows[i][0] = '<b>' + spy_rows[i][0] + '<b>'

        agg_rows[i][0] = str(agg_rows[i][0])
        agg_rows[i][0] = '<b>' + agg_rows[i][0] + '<b>'

    df = pd.DataFrame(list_4_df) #creates a dataframe of the lists
    df = df.drop(df.index[0]) #drops the label row, this is for creating a plotly table better 
    
    color_list = []
    font_color_list = []
    color_list += [bg_color]
    color_list += [bg_color]
    color_list += [bg_color]
    color_list += [bg_color]
    color_list += [label_color]
    font_color_list += [onramp_colors['btc']]
    font_color_list += ['white']
    font_color_list += ['white']
    font_color_list += ['white']
    font_color_list += ['black']
    for i in range(length-1):
        color_list += [bg_color]
        color_list += [bg_color]
        color_list += [bg_color]
        color_list += [bg_color]
        color_list += [label_color]
        font_color_list += [onramp_colors['btc']]
        font_color_list += ['white']
        font_color_list += ['white']
        font_color_list += ['white']
        font_color_list += ['black']
    
    color_list2 = []
    for i in range(length):
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += ['#f7f7f7']
        color_list2 += [label_color]

    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
    #making the table 
    date_color = '#131c4f'
    fig = go.Figure(data=[go.Table(
                            #columnorder = [1,2,1,1,1,1,1,1,1,1,1,1,1,1],
                            columnwidth = [200, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                            header=dict(values= label_row,
                                        line_color= 'rgba(100, 100, 100, 0.36)',
                                        height = 30,
                                        fill_color= label_color,
                                        align=['center','center'],
                                        font=dict(color='black', size=14)),
                            cells=dict(values=[df.a, df.b, df.c, df.d, df.e, df.f, df.g, df.h, df.i, df.j, df.k, df.l, df.m, df.n],
                                        line_color = 'rgba(100, 100, 100, 0.36)',
                                        height = 30,
                                        font = dict(color = [font_color_list*14], size = 14),
                                        fill_color = [color_list] )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=1, b=0))
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )

    return fig
    #['#A90BFE', '#FF7052', date_color, '#A90BFE','#FF7052', date_color, '#A90BFE', '#FF7052', date_color, '#A90BFE', '#FF7052', date_color, '#A90BFE', '#FF7052']
    #['black', 'black', 'white', 'black','black', 'white', 'black', 'black', 'white', 'black', 'black', 'white', 'black', 'black']

def optomize_table(df):
    df = pd.DataFrame(df)
    
    #combining 
    labels = ['<b>Tickers<b>', '<b>Allocation<b>']

    df.columns = ["Allocation"]
    df = df.dropna()
    df.index = df.index.map(str.upper)
    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'rgba(100, 100, 100, 0.36)',
                                        fill_color= onramp_colors["cyan"],
                                        align=['center','center'],
                                        font=dict(color='black', size=12)),
                            cells=dict(values=[df.index, df.Allocation],
                                        line_color = 'rgba(100, 100, 100, 0.36)',
                                        height = 30,
                                        font = dict(color = 'white'),
                                        fill_color = onramp_colors["dark_blue"] )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=0, b=0))
    
    fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
    return fig

def optomize_table_combine(df):
    
    #combining 
    labels = ['<b>Tickers<b>', '<b>Daily<b>', '<b>Monthly<b>', '<b>Quarterly<b>', '<b>Yearly<b>']

    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'black',
                                        fill_color= '#131c4f',
                                        align=['center','center'],
                                        font=dict(color='white', size=10)),
                            cells=dict(values=[df.index, df.Daily, df.Monthly, df.Quarterly, df.Yearly],
                                        line_color = 'black',
                                        height = 30,
                                        font = dict(color = 'black'),
                                        fill_color = '#f7f7f7' )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=0, b=0))
    return fig

def stats_table(results_list):

    df_list = results_to_df(results_list) #The results arent dataframes, so need to make them dataframes

    stats_combined = pd.concat([df_list[0], df_list[1]], axis=1) #this combines them 
    stats_combined.columns = ['Stats', 'Your Strategy', 'Drop', "60-40 Portfolio"]
    stats_combined = stats_combined.drop(['Drop'], axis =1 )

    stats_col = []
    stats_col.append(stats_combined.iloc[1][0])
    stats_col.append(stats_combined.iloc[2][0])
    stats_col.append(stats_combined.iloc[4][0])
    stats_col.append(stats_combined.iloc[8][0])
    stats_col.append(stats_combined.iloc[27][0])
    stats_col.append(stats_combined.iloc[28][0])
    stats_col.append(stats_combined.iloc[29][0])
    stats_col.append(stats_combined.iloc[30][0])
    stats_col.append(stats_combined.iloc[33][0])
    stats_col.append(stats_combined.iloc[34][0])
    
    strat1_col = []
    strat1_col.append(stats_combined.iloc[1][1])
    strat1_col.append(stats_combined.iloc[2][1])
    strat1_col.append(stats_combined.iloc[4][1])
    strat1_col.append(stats_combined.iloc[8][1])
    strat1_col.append(stats_combined.iloc[27][1])
    strat1_col.append(stats_combined.iloc[28][1])
    strat1_col.append(stats_combined.iloc[29][1])
    strat1_col.append(stats_combined.iloc[30][1])
    strat1_col.append(stats_combined.iloc[33][1])
    strat1_col.append(stats_combined.iloc[34][1])

    strat2_col = []
    strat2_col.append(stats_combined.iloc[1][2])
    strat2_col.append(stats_combined.iloc[2][2])
    strat2_col.append(stats_combined.iloc[4][2])
    strat2_col.append(stats_combined.iloc[8][2])
    strat2_col.append(stats_combined.iloc[27][2])
    strat2_col.append(stats_combined.iloc[28][2])
    strat2_col.append(stats_combined.iloc[29][2])
    strat2_col.append(stats_combined.iloc[30][2])
    strat2_col.append(stats_combined.iloc[33][2])
    strat2_col.append(stats_combined.iloc[34][2])

    #creates a datframe with exactly what we need
    df = pd.DataFrame(list(zip(stats_col, strat1_col, strat2_col)), 
               columns =['Stats', 'Your_Strategy', 'Portfolio6040'])
    labels = ['<b>Stats<b>', '<b>' +stats_combined.iloc[0][1] + '<b>', '<b>' +stats_combined.iloc[0][2] + '<b>',]
    
    text_color = []
    n = len(df)
    for col in df:
        if col!='Your_Strategy':
            text_color.append(["white"] * n)
        else:
            text_color.append(onramp_colors['btc'])
    fig = go.Figure(data=[go.Table(
                            header=dict(values= labels,
                                        line_color= 'rgba(100, 100, 100, 0.36)',
                                        fill_color= onramp_colors["cyan"],
                                        align=['center','center'],
                                        font=dict(color='black', size=12)),
                            cells=dict(values=[df.Stats, df.Your_Strategy, df.Portfolio6040],
                                        line_color = 'rgba(100, 100, 100, 0.36)',
                                        height = 26,
                                        font = dict(color = text_color, size = 12),
                                        fill_color =  onramp_colors["dark_blue"])) ])
    fig.update_layout(margin = dict(l=2, r=1, t=0, b=10), 
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",)

    return fig



