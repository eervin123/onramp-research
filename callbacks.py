import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash_app import dash_app
from dash.dependencies import Output, Input, State
import datetime
from datetime import timedelta
import time 
import pytz
import bt
import redis
from direct_redis import DirectRedis
import pyarrow as pa
import urllib.parse as urlparse
from formatting import onramp_colors, onramp_template, onramp_template_dashboard, custom_scale
from helpers import *
from bt_algos import RebalanceAssetThreshold
#get_coin_data, get_coin_data_new, volatility, calc_volatility, calc_volatility_new, create_corr, create_corr_new, get_data, calculate_controls, pl

#redis-16351.c263.us-east-1-2.ec2.cloud.redislabs.com:16351

url = urlparse.urlparse('redis://default:mUtpOEwJc2F8tHYOGxF9JGvnIwHY3unu@redis-16351.c263.us-east-1-2.ec2.cloud.redislabs.com:16351')
r = DirectRedis(host=url.hostname, port=url.port, password=url.password)

#r = redis.Redis(host='localhost', port=6379)

####################################################################################################
# 000 - IMPORT DATA SLIDER DASHBOARD
####################################################################################################

df = pd.read_csv(
    "datafiles/Slider_data20.csv",
    usecols=[
        "Date",
        "TraditionalOnly",
        "SP500Only",
        "d1",
        "d2",
        "d3",
        "d4",
        "d5",
        "d6",
        "d7",
        "d8",
        "d9",
        "d10",
        "d11",
        "d12",
        "d13",
        "d14",
        "d15",
        "d16",
        "d17",
        "d18",
        "d19",
        "d20",
        "d21",
    ],
    encoding="latin-1",
)
df["Date"] = pd.to_datetime(df["Date"], unit="ms")
df = df.set_index("Date")
# Stats Data
df_stats = pd.read_csv(
    "datafiles/Slider_data20.csv",
    usecols=[
        "AnnReturn",
        "AnnRisk",
        "SharpeRatio",
        "SortinoRatio",
        "ReturnTraditional",
        "ReturnSP500",
        "RiskTraditional",
        "RiskSP500",
        "SharpeTraditional",
        "SharpeSP500",
        "SortinoTraditional",
        "SortinoSP500",
    ],
    encoding="latin-1",
)
df_stats = df_stats.dropna()

colors = [onramp_colors["dark_blue"], "#3fb6dc", "#f2a900"]
####################################################################################################
# 001 - LARGE CHARTS DATA
####################################################################################################
pairs_crypto = [
    "BTC-USDT",
    "BCHABC-USDT",
    "TRX-USDT",
    "IOTA-USDT",
    "XLM-USDT",
    "EOS-USDT",
    "ADA-USDT",
    "LTC-USDT",
    "NEO-USDT",
    "BNB-USDT",
    "ETH-USDT",
]

pairs_mixed = [
    "S&P 500",
    "All World Index",
    "High Yield",
    "HFRXGL Index",
    "Gold",
    "Emerging Markets",
    "Russell 2000",
    "Oil",
    "Frontier Markets",
    "Biotech",
    "Bitcoin",
    "Ethereum",
]


############################################## VOLATILITTY ##########################################

df_mixed = calc_volatility_new(pairs_mixed) #Used for Mixed Asset Class Vol Chart

df_mixed = df_mixed[
    df_mixed.index > datetime.datetime(2020, 1, 15)
]  # make it so we only have 2020 data

df_vol = calc_volatility(pairs_crypto) #Used for Crypto Vol Chart 

today = datetime.datetime.now(tz=pytz.utc).date()
xd = today - datetime.timedelta(days=30) 

c = xd.strftime("%Y-%m-%d")


############################################## HEATMAP/TIMELINE ##########################################

corr_df = create_corr(pairs_crypto)

corr_df_new = create_corr_new(pairs_mixed)

####################################################################################################
# 000 - CUSTOM PAGE DATA
####################################################################################################

data = get_data()
returns = calculate_controls(data)

results_control = returns[0]
results_spy = returns[1]
results_agg = returns[2]


####################################################################################################
# DASHBOARD PAGE
####################################################################################################
@dash_app.callback(
    [
        dash.dependencies.Output("pie_chart", "figure"),
        dash.dependencies.Output("line_chart", "figure"),
        dash.dependencies.Output("scatter_plot", "figure"),
        dash.dependencies.Output("bar_chart_rr", "figure"),
        dash.dependencies.Output("bar_chart_ss", "figure"),
    ],
    [dash.dependencies.Input("slider_num", "drag_value")],
)
def update_graphs(value):
    # print(value)
    # ------------------------------------------------------------------------------Pie Chart ---------------------------------------------------------------------------
    value_dict = {
        0: 1,
        0.5: 2,
        1: 3,
        1.5: 4,
        2: 5,
        2.5: 6,
        3: 7,
        3.5: 8,
        4: 9,
        4.5: 10,
        5: 11,
        5.5: 12,
        6: 13,
        6.5: 14,
        7: 15,
        7.5: 16,
        8: 17,
        8.5: 18,
        9: 19,
        9.5: 20,
        10: 21,
    }

    percent_dict = {"Traditional 60/40": float(1 - float(value)) / 100, "Bitcoin": float(float(value) / 100)}

    # print(value)
    def graph_pie(percent_dictionary):

        colors_pie = [onramp_colors['dark_blue'], "#f2a900"]  # BTC Orange
        assets = list(percent_dictionary.keys())

        percents = list(percent_dictionary.values())
        # print(percents)

        fig = px.pie(
            values=percents,
            names=assets,
            color=assets,
            color_discrete_sequence=colors_pie,
            title="Portfolio Allocation",
            # width = 400, height = 400
            template=onramp_template,
            height=500,
            hole = .2
        )
        fig.update_traces(hovertemplate="%{value:.0%}")
        # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_layout(
            font=dict(family="Roboto", color= onramp_colors["gray"]),
            title={
                "text": "<b>Portfolio Allocation<b>",
                "y": 1,
                "x": 0.49,
                "xanchor": "center",
                "yanchor": "top",
            },
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.2, xanchor="left", x=0.30
            ),
        )
        fig.update_layout(
            {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)",}
        )
        fig.update_traces(textfont_size=17, marker=dict( line=dict(color='white', width=1)))
        fig.update_layout(titlefont=dict(size=24, color= onramp_colors["gray"]))
        fig.update_layout(margin=dict(l=10, r=20, t=40, b=0))

        return fig

    # print(percent_dict)
    value = value_dict[value]
    # print(value)
    # ------------------------------------------------------------------------------Line Chart ---------------------------------------------------------------------------

    choice = "d" + str(value)

    def graph_line_chart(df, choice):
        #colors = ["#a90bfe", "#7540ee", "#3fb6dc"]
        colors = ['white', "#3fb6dc", "#f2a900"]
        df = df[["TraditionalOnly", "SP500Only", choice]]
        df.columns = ["Traditional 60/40", "S&P 500", "Combined Portfolio"]
        color_dict = {}
        color_dict["Traditional 60/40"] = colors[0]
        color_dict["S&P 500"] = colors[1]
        color_dict["Combined Portfolio"] = colors[2]

        fig = px.line(
            df,
            labels={"value": "", "Date": "", "color": "", "variable": ""},
            title="Portfolio Performance",
            color_discrete_map=color_dict,
            template=onramp_template,
            height = 500
            # width = 450
        )

        fig.update_yaxes(tickprefix="$", showgrid=False)  # the y-axis is in dollars
        x = 0.82
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.80
            ),
            font=dict(family="Roboto", color= onramp_colors["gray"]),
            title={
                "text": "<b>Portfolio Performance<b>",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
        )
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
        fig.update_yaxes(side="left", nticks=8)
        fig.update_layout(titlefont=dict(size=24, color= onramp_colors["gray"]))
        fig.update_layout(margin=dict(l=70, r=30, t=0, b=0))
        return fig

    # ------------------------------------------------------------------------------Scatter Plot ---------------------------------------------------------------------------
    risk_dic = {
        "Traditional 60/40": float(df_stats.iloc[0][6]) / 100,
        "S&P 500": float(df_stats.iloc[0][7]) / 100,
        "Combined Portfolio": float(df_stats.iloc[value - 1][1]) / 100,
    }
    # print(risk_dic)
    return_dic = {
        "Traditional 60/40": float(df_stats.iloc[0][4]) / 100,
        "S&P 500": float(df_stats.iloc[0][5]) / 100,
        "Combined Portfolio": float(df_stats.iloc[value - 1][0]) / 100,
    }

    def graph_scatter_plot(risk_dic, return_dic):
        colors = [onramp_colors['dark_blue'], "#3fb6dc", "#f2a900"]
        labels = list(risk_dic.keys())

        xaxis_vol = list(risk_dic.values())
        yaxis_return = list(return_dic.values())

        size_list = [3, 3, 3]
        symbols = [1, 2, 0]  # this makes the symbols square diamond and circle in order
        fig = px.scatter(
            x=xaxis_vol,
            y=yaxis_return,
            size=size_list,
            color=labels,
            # color_discrete_sequence=['#A90BFE','#FF7052','#66F3EC', '#67F9AF'],
            color_discrete_sequence=colors,
            opacity=1,
            template=onramp_template,
            labels={
                "x": "",
                "y": "Annual Return",
                "color": "",
                "symbol": "",
            },
            title="Risk vs. Return",
            height = 500
        )
        # width = 450, height = 450)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_traces(
            hovertemplate="Annual Risk = %{x:.0%}<br>Annual Return = %{y:.0%}"
        )

        fig.update_layout(
            title={
                "text": "<b>Risk vs. Return<b>",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(family="Circular STD", color="black"),
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.35, xanchor="left", x=0.1
            ),
        )
        fig.update_yaxes(side="left")
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(255, 255, 255, 0)",
                "paper_bgcolor": "rgba(255, 255, 255, 0)",
            }
        )
        fig.add_annotation(text="Annual Risk", 
                  xref="paper", yref="paper",
                  x=0.5, y=-.2, showarrow=False, font=dict(family="Roboto", color= onramp_colors["gray"], size = 20))
        fig.update_layout(yaxis_tickformat="%")
        fig.update_layout(xaxis_tickformat="%")
        fig.update_layout(titlefont=dict(size=24, color= onramp_colors["gray"]))
        fig.update_xaxes(title_font={"size": 20})
        fig.update_yaxes(title_font={"size": 20})
        fig.update_layout(margin=dict(l=50, r=30, t=20, b=0))

        return fig

    # ------------------------------------------------------------------------------Bar Chart ---------------------------------------------------------------------------

    x_axis_rr = ["Ann. Return", "Ann. Risk"]
    x_axis_ss = ["Sharpe Ratio", "Sortino Ratio"]

    y_combined_rr = [
        float(df_stats.iloc[value - 1][0]) / 100,
        float(df_stats.iloc[value - 1][1]) / 100,
    ]
    y_6040_rr = [float(df_stats.iloc[0][4]) / 100, float(df_stats.iloc[0][6]) / 100]
    y_spy_rr = [float(df_stats.iloc[0][5]) / 100, float(df_stats.iloc[0][7]) / 100]

    y_combined_ss = [
        float(df_stats.iloc[value - 1][2]) / 100,
        float(df_stats.iloc[value - 1][3]) / 100,
    ]
    y_6040_ss = [float(df_stats.iloc[0][8]) / 100, float(df_stats.iloc[0][10]) / 100]
    y_spy_ss = [float(df_stats.iloc[0][9]) / 100, float(df_stats.iloc[0][11]) / 100]

    def graph_barchart(x_axis_rr_ss, y_combined, y_6040, y_spy):

        colors = [onramp_colors['dark_blue'], "#3fb6dc", "#f2a900"]
        if x_axis_rr_ss[0] == "Ann. Return":
            title = "<b>Ann. Return & Risk<b>"
            max_range = 0.4
        else:
            title = "<b>Sharpe & Sortino Ratio<b>"
            for i in range(len(y_combined)):
                y_combined[i] = y_combined[i]*100
                y_6040[i] = round(y_6040[i]*100, 2)
                y_spy[i] = round(y_spy[i]*100, 2)
            max_range = 4

        x_axis_rr_ss *= 3
        y_vals = []
        y_vals += y_6040
        y_vals += y_spy
        y_vals += y_combined

        strat = [
            "Traditional 60/40",
            "Traditional 60/40",
            "S&P 500",
            "S&P 500",
            "Combined Portfolio",
            "Combined Portfolio",
        ]

        df = pd.DataFrame(
            list(zip(x_axis_rr_ss, y_vals, strat)),
            columns=["Type", "Values", "Strategy"],
        )
        # print(df)

        fig = px.bar(
            df,
            x="Type",
            y="Values",
            color="Strategy",
            barmode="group",
            color_discrete_sequence=colors,
            template=onramp_template,
            labels={"Type": "", "Values": "", "Strategy": ""},
            height = 490
        )
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker_line_color='white', marker_line_width=1.5)


        if x_axis_rr_ss[0] == "Ann. Return":
            fig.update_traces(texttemplate="<b>%{y:.2%}<b>", textposition="outside")
            fig.update_traces(hovertemplate="%{y:.0%}")
        else:
            fig.update_traces(texttemplate="<b>%{y:.9}<b>", textposition="outside")
            fig.update_traces(hovertemplate="%{y:.3}")
        fig.update_layout(uniformtext_minsize=21, uniformtext_mode="hide")
        fig.update_yaxes(showticklabels=False)
        fig.update_yaxes(range=[0, max_range])
        fig.update_layout(
            title={
                "text": "",
                "y": 0.0,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(family="Circular STD", color="white"),
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0.31
            ),
            barmode="group",
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
        )
        # fig.update_layout(
        #     {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)",}
        # )
        fig.update_layout(xaxis_tickfont_size=19)
        fig.update_layout(titlefont=dict(size=24, color="white"))
        fig.update_layout(margin = dict(l=10, r=0, t=0, b=0))

        return fig

    pie_fig = graph_pie(percent_dict)
    line_fig = graph_line_chart(df, choice)
    scatter_fig = graph_scatter_plot(risk_dic, return_dic)
    bar_rr_fig = graph_barchart(x_axis_rr, y_combined_rr, y_6040_rr, y_spy_rr)
    bar_ss_fig = graph_barchart(x_axis_ss, y_combined_ss, y_6040_ss, y_spy_ss)
    return pie_fig, line_fig, scatter_fig, bar_rr_fig, bar_ss_fig

####################################################################################################
# VOLATILITY CHART PAGE
####################################################################################################

@dash_app.callback(
    dash.dependencies.Output("vol_chart", "figure"),
    [dash.dependencies.Input("dropdown", "value")],
)
def update_vol(value):
    
    def graph_volatility(df, coins, xd):
        source = "Binance"
        yaxis_dict = dict(
            title="Rolling 30-Day Volatility",
            hoverformat=".2f",
            ticks="outside",
            tickcolor="#53585f",
            ticklen=0,
            tickwidth=3,
            tick0=0,
            tickprefix="                 ",
        )
        vols = [14, 30, 90]
        colors = 6 * [
            "grey",
            "#033F63",
            "#28666E",
            "#7C9885",
            "#B5B682",
            "#FEDC97",
            "#F6AE2D",
            "#F26419",
            "#5F0F40",
            "#9A031E",
            "#CB793A",
        ]

        index = 0
        data = []
        for i in df.columns:
            data.append(
                go.Scatter(
                    x=list(df.index),
                    y=list(df[i]),
                    name=i.split("_", 1)[0],
                    visible=False,
                    line_color=colors[index],
                )
            )
            index += 1

        num_coins = len(coins)

        vis_init = [False] * len(vols)
        vis_vol = dict()
        for i, v in enumerate(list(vols)):
            tmp = vis_init.copy()
            tmp[i] = True
            vis_vol[v] = tmp.copy()

        updatemenus = list(
            [
                dict(
                    type="dropdown",
                    active=1,
                    x=-0,
                    y=1.2,
                    bgcolor = 'white',
                    font = dict(color = 'black'),
                    buttons=[
                        dict(
                            label=f"{v}-Day",
                            method="update",
                            args=[
                                {"visible": vis_vol[v] * num_coins},
                                {
                                    "yaxis": dict(
                                        yaxis_dict, title=f"Rolling {v}-Day Volatility"
                                    )
                                },
                            ],
                        )
                        for v in list(vols)
                    ],
                )
            ]
        )

        # set initial to 0
        for i, b in enumerate(vis_vol[30] * num_coins):
            if b == True:
                data[i].visible = b

        layout = dict(
            title=dict(
                text="Changing Volatility Over Time",
                font=dict(size=30, color="white"),
                x=0.5,
            ),
            height=700,
            width=1000,
            dragmode="zoom",
            xaxis=dict(
                title="Date",
                ticks="inside",
                ticklen=0,
                tickwidth=3,
                rangeselector=dict(
                    font = dict(color = 'black'),
                    buttons=list(
                        [
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                type="date",
                tickcolor="#53585f",
            ),
            yaxis=yaxis_dict,
            margin=dict(pad=0, b=125),
            updatemenus=updatemenus,
            font=dict(size=14, color = 'white'),
            annotations=[
                dict(
                    x=-0.18,
                    y=-0.25,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    text=f"*Source: {source}; Volatility data quoted here represents data as of {xd}.",
                    font=dict(size=10),
                )
            ],
        )

        fig = go.Figure(data=data, layout=layout)
        
        fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
        )
        fig.update_xaxes(showgrid = False)
        fig.update_yaxes(gridcolor = '#C3C3C3')
        return fig

    if value == "CC":
        return graph_volatility(df_vol, pairs_crypto, c)
    if value == "AC":
        return graph_volatility(df_mixed, pairs_mixed, c)

####################################################################################################
# HEATMAP CHART PAGE
####################################################################################################
@dash_app.callback(
    dash.dependencies.Output("heatmap", "figure"),
    [dash.dependencies.Input("dropdown", "value")],
)
def update_heatmap(value):
    def graph_heatmap(df, date):
        corr_mtx = df.loc[date].values
        text_info = np.round(corr_mtx, decimals=5).astype(str)

        x = 0
        for i in range(len(text_info)):
            for j in range(len(text_info[0])):
                if text_info[i, j] == "1.0":
                    text_info[i, j] = ""
                    corr_mtx[i, j] = np.nan

        labels = df.columns
        layout = go.Layout(
            font = dict(color = 'white'),
            title=dict(text="Correlation Matrix", font=dict(size=30, color = 'white'), x=0.5,),
            annotations=[
                dict(
                    x=0.5,
                    y=-0.25,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    text=(
                        f"*6-Month Rolling Correlation of Daily Returns; Source: Binance; Correlation data quoted here represents data as of {date}."
                    ),
                    font=dict(size=10, color = 'white'),
                )
            ],
            autosize=False,
            width=700,
            height=700,
            xaxis=dict(ticklen=1),
            yaxis=dict(ticklen=1,),
            margin=dict(pad=0, b=125),
        )

        fig = go.Figure(
            data=[
                go.Heatmap(
                    z=corr_mtx,
                    x=labels,
                    y=labels,
                    text=text_info,
                    hoverinfo="text",
                    colorscale=[[0.0, "#3fb6dc"], [1, "#420DBB"]],
                )
            ],
            layout=layout,
        )
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(255, 255, 255, 0)",
                "paper_bgcolor": "rgba(255, 255, 255, 0)",
            }
        )
        fig.update_xaxes(showgrid=False, color = 'white')
        fig.update_yaxes(showgrid=False, color = 'white')
        fig.update_layout(legend_font = dict(color = 'white'))
        return fig

    if value == "CC":
        return graph_heatmap(corr_df, c)
    if value == "AC":
        return graph_heatmap(corr_df_new, c)

####################################################################################################
# TIMELINE CHART PAGE
####################################################################################################
@dash_app.callback(
    dash.dependencies.Output("heatmap_timeline", "figure"),
    [dash.dependencies.Input("dropdown", "value")],
)
def update_timeline(value):
    def graph_timeline(corr_df, xd):
        _font = dict(family="Roboto", color = 'white')
        source = "Binance"
        axis_dict = dict(
            ticks="outside",
            tickfont=_font,
            tickcolor="#53585f",
            ticklen=0,
            tickwidth=2,
            automargin=True,
            fixedrange=True,
            tickprefix="        ",
        )

        unique_coins = corr_df.columns
        coin_set = set(unique_coins)
        num_buttons = np.arange(1, len(unique_coins), 1).sum()
        data, buttons = [], []
        x = 0

        if "USDT" in corr_df.columns[0]:
            label_tag = "-USDT"
        else:
            label_tag = "-USD"

        for i in unique_coins:
            labels = []

            info_ = i.replace(label_tag, "")
            # z:vals, x:dates, y:coin names
            cross_section = corr_df.xs(i, level=1).drop(i, axis=1)
            labels = [x.replace(label_tag, "") for x in cross_section.columns]
            data.append(
                go.Heatmap(
                    z=cross_section.T.values,
                    x=cross_section.index,
                    y=labels,
                    name=info_,
                    visible=False,
                    colorscale=custom_scale,
                )
            )
            buttons.append(
                dict(
                    label=info_,
                    method="update",
                    args=[
                        {"visible": list(np.insert([False] * num_buttons, x, True))},
                        {
                            "yaxis": dict(
                                axis_dict,
                                title=f"{info_} 6-Month Rolling Return Correlation",
                            )
                        },
                    ],
                )
            )
            x += 1

        data[0].visible = True
        start_title = buttons[0]["label"]
        updatemenus = list(
            [dict(type="dropdown", active=0, y=1.09, x=-.01, buttons=buttons, font = dict(color = 'black'), bgcolor = 'white'),]
        )

        layout = dict(
            font=_font,
            images=[
                dict(
                    source="/static/onramp-logo.png",
                    xref="paper",
                    yref="paper",
                    x=1.08,
                    y=1.1,
                    sizex=0.25,
                    sizey=0.25,
                    xanchor="right",
                    yanchor="bottom",
                )
            ],
            height=700,
            width=800,
            dragmode="zoom",
            annotations=[
                dict(
                    x=-0.15,
                    y=-0.20,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    text=f"*Source: {source}; Correlation data quoted here represents data as of {xd}.",
                    font=dict(size=9),
                )
            ],
            title=dict(
                text="Relative Correlation Over Time",
                font=dict(_font, size=40, color="white"),
                x=0.5,
            ),
            xaxis=dict(
                title=dict(text="Date", font=dict(_font, size=20)),
                ticks="inside",
                ticklen=6,
                tickwidth=2,
                tickfont=_font,
                rangeselector=dict(
                    x=0.75,
                    font = dict(color = 'black'),
                    buttons=list(
                        [
                            dict(
                                count=3, label="3m", step="month", stepmode="backward",
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                ),
                autorange=True,
                type="date",
                tickcolor="#53585f",
            ),
            yaxis=dict(
                axis_dict,
                title=dict(
                    font=dict(_font, size=20),
                    text=f"{start_title} 6-Month Rolling Return Correlation",
                ),
            ),
            margin=dict(pad=5, b=105),
            legend=dict(orientation="h"),
            updatemenus=updatemenus,
        )

        fig = go.Figure(data=data, layout=layout)
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })

        return fig

    if value == "CC":
        return graph_timeline(corr_df, c)
    if value == "AC":
        return graph_timeline(corr_df_new, c)

####################################################################################################
# CUSTOM STRATEGY PAGE
####################################################################################################
@dash_app.callback(
    [Output('pie_chart_c', 'figure'),
    Output('line_chart_c', 'figure'),
    Output('scatter_plot_c', 'figure'),
    Output("stats_table", "figure"),
    Output("month_table", "figure"),
    Output("balance_table", "figure"),
    Output("return_stats", "figure")
    ],
    
    Input("submit_button", "n_clicks"),
    State('Ticker1', 'value'),
    State('Allocation1', 'value'),
    State('Ticker2', 'value'),
    State('Allocation2', 'value'),
    State('Ticker3', 'value'),
    State('Allocation3', 'value'),
    State('Ticker4', 'value'),
    State('Allocation4', 'value'),
    State('Rebalance', 'value')
    
)
def update_graph(num_click, stock_choice_1, alloc1, stock_choice_2, alloc2, stock_choice_3, alloc3, stock_choice_4, alloc4, rebalance = 1.2):
    start = time.time()
    ####################################################### PIE CHART ##########################################################################################
    stock_list_pie = [stock_choice_1, stock_choice_2, stock_choice_3, stock_choice_4]
    percent_list = [float(alloc1)/100, float(alloc2)/100, float(alloc3)/100, float(alloc4)/100]

    fig = plotly_pie(stock_list_pie, percent_list)
    #px.pie( values = percent_list, names = stock_list_pie, color = stock_list_pie, title="", template= onramp_template, hole = .3, height = 300)
    
    ##################################################### SETTING UP DATA #############################################################################################
    stock_choice_1 = stock_choice_1.lower()
    stock_choice_2 = stock_choice_2.lower()
    stock_choice_3 = stock_choice_3.lower()
    stock_choice_4 = stock_choice_4.lower()
    stock_list_pie = [stock_choice_1, stock_choice_2, stock_choice_3, stock_choice_4]
    
    #stock_list = stock_choice_1 +',' + stock_choice_2 + ',' + stock_choice_3 + ',' + stock_choice_4
    
    data_s = time.time()
    #data = bt.get(stock_list, start = '2017-01-01')
    data = pd.DataFrame()
    #context = pa.default_serialization_context()
    for ticker in stock_list_pie:
        data_x = r.get(ticker)
        if data_x is None:
            print("Could not find", ticker, "in the cache.")
            data_x = bt.get(ticker, start = '2017-01-01')
            r.set(ticker, data_x)
            r.expire(ticker, timedelta(seconds = 86400))

        data = data.join(data_x, how = 'outer')
    




    # data1 = r.get(stock_choice_1)
    # context = pa.default_serialization_context()
    # if data1 is None:
    #     print("Could not find", stock_choice_1, "in the cache.")
    #     data1 = bt.get(stock_choice_1, start = '2017-01-01')
    #     r.set(stock_choice_1, context.serialize(data1).to_buffer().to_pybytes())

    # data1 = bt.get(stock_choice_1, start = '2017-01-01')
    # data2 = bt.get(stock_choice_2, start = '2017-01-01')
    # data3 = bt.get(stock_choice_3, start = '2017-01-01')
    # data4 = bt.get(stock_choice_4, start = '2017-01-01')
    # data_2 = pd.DataFrame()
    # data_2 = data_2.join(data1, how = 'outer')
    # print(data_2)
    # data = data1.join(data2, how='outer')
    # data = data.join(data3, how='outer')
    # data = data.join(data4, how='outer')
    data = data.dropna()
    #print(data)
    data_e = time.time()
    print("Finished Data", stock_choice_1, ":", data_e - data_s)

    #need the '-' in cryptos to get the data, but bt needs it gone to work
    data_st = time.time()
    stock_choice_1 = stock_choice_1.replace('-', '')
    stock_choice_2 = stock_choice_2.replace('-', '')
    stock_choice_3 = stock_choice_3.replace('-', '')
    stock_choice_4 = stock_choice_4.replace('-', '')

    
    stock_dic = {stock_choice_1: float(alloc1)/100, stock_choice_2: float(alloc2)/100, stock_choice_3: float(alloc3)/100, stock_choice_4: float(alloc4)/100} #dictonary for strat
    
    if(rebalance == None or rebalance == ""):
        rebalance = 120
    rebalance = float(rebalance)/100
    strategy_ = bt.Strategy("Custom Strategy", 
                              [ 
                              bt.algos.RunDaily(),
                              bt.algos.SelectAll(), 
                              bt.algos.WeighSpecified(**stock_dic),
                              RebalanceAssetThreshold(threshold = rebalance),
                              bt.algos.RunMonthly(),
                              bt.algos.Rebalance()]) #Creating strategy

    test = bt.Backtest(strategy_, data)
    results = bt.run(test)
    
    results_list = [results, results_control, results_spy, results_agg]
    
    data_et = time.time()
    print("Finished Strategy", stock_choice_1, ":", data_et - data_st)
    ################################################### LINE CHART ########################################################################################################
    fig_line = line_chart(results_list)
    fig_line.update_layout(template = onramp_template_dashboard) #legend in top left

    fig_scat = scatter_plot(results_list)
    fig_scat.update_layout(template = onramp_template_dashboard) #legend in top left

    fig_stats = stats_table(results_list)

    fig_month_table = monthly_table(results_list)

    fig_month_table.update_layout(height = 830)

    fig_balance_table = balance_table(results, results_control)

    fig_balance_table.update_layout(height = 100)

    fig_returns_stats = short_stats_table(results_list)

    fig_returns_stats.update_layout(height = 320)

    end = time.time()
    print("Finished Everything", stock_choice_1, ":", end - start)
    return fig, fig_line, fig_scat, fig_stats, fig_month_table, fig_balance_table, fig_returns_stats


####################################################################################################
# PORTFOLIO OPTIMIZER PAGE
####################################################################################################
@dash_app.callback(
    [Output('pie_chart_o', 'figure'),
    Output('line_chart_o', 'figure'),
    Output('opto_table', 'figure'),
    Output('scatter_plot_o', 'figure'),
    Output('stats_table_o', 'figure'),
    Output('month_table_o', 'figure'),
    ],
    
    Input("submit_button_o", "n_clicks"),
    State('Ticker_o', 'value'),
    State('cTicker_o', 'value'),
    State('opti_sel', 'value'),
    State('Frequency_sel', 'value'),
    State('crypto_alloc', 'value'),
)
def update_graph(num_click, tickers, crypto_tickers, opti_sel, freq_sel, crypto_max = 1.2):
    
    tickers = tickers.replace(" ", '') #remove any extra spaces
    tickers_list = tickers.split(',')

    c_tickers = crypto_tickers.replace(" ", '') #remove any extra spaces
    c_tickers_list = c_tickers.split(',')

    full_asset_list = tickers_list + c_tickers_list
    
    ####################################################################################################################################################
    ############### GET DATA
    ####################################################################################################################################################
    data = pd.DataFrame()
    for ticker in full_asset_list:
        data_x = r.get(ticker)
        if data_x is None:
            print("Could not find", ticker, "in the cache.")
            data_x = bt.get(ticker, start = '2017-01-01')
            r.set(ticker, data_x)
            r.expire(ticker, timedelta(seconds = 86400))

        data = data.join(data_x, how = 'outer')
    
    data = data.dropna()
    if(crypto_max == None or crypto_max == ""): #In order to make crypto allocation optional
        crypto_max = 120
    crypto_max = float(crypto_max)/100

    
    ####################################################################################################################################################
    ############### PREPARE DATA
    ####################################################################################################################################################
    
    #Figure out which Frequency 
    if (freq_sel == 'Daily'):
        returns = data.to_log_returns().dropna()
        name = 'Portfolio Optomized Daily'

    if (freq_sel == 'Month'):
        returns = data.asfreq("M",method='ffill').to_log_returns().dropna()
        name = 'Portfolio Optomized Monthly'

    if (freq_sel == 'Quart'):
        returns = data.asfreq("Q",method='ffill').to_log_returns().dropna()
        name = 'Portfolio Optomized Quarterly'

    if (freq_sel == 'Year'):
        returns = data.asfreq("Y",method='ffill').to_log_returns().dropna()
        name = 'Portfolio Optomized Yearly'

    #Pick the right optimization type
    if(opti_sel == 'ef'):
        daily_opt = returns.calc_mean_var_weights().as_format(".2%")
    if(opti_sel == "er"):
        daily_opt = returns.calc_erc_weights().as_format(".2%")
    if(opti_sel == "iv"):
        daily_opt = returns.calc_inv_vol_weights().as_format(".2%")
    
    #preparing data for charts
    stock_dic = daily_opt.to_dict()

    for key in stock_dic: #makes percents numbers 
        stock_dic[key] = float(stock_dic[key].replace('%', ''))
        stock_dic[key] = stock_dic[key]/100
        
    stock_list = list(stock_dic.keys()) #convert the dictionary into lists for plotting
    percent_list = list(stock_dic.values())

    temp = []
    temp_stock = []
    for i in range(len(percent_list)): #Takes out values of 0 
        if (percent_list[i] != 0):
            temp.append(percent_list[i])
            temp_stock.append(stock_list[i])

    stock_list = temp_stock
    percent_list= temp

    
    ####################################################################################################################################################
    ############### CALCULATE MAXIMUM CRYPTO ALLOCATION
    ####################################################################################################################################################

    crypto_tickers = crypto_tickers.replace('-', '')
    crypto_list = crypto_tickers.split(',')
    only_stock_list = tickers_list
    crypto_sum = 0
    stock_sum = 0

    for i in crypto_list: #checking if we need to adjust because too much crypto
        crypto_sum += stock_dic[i] * 100

    for i in only_stock_list: #total stock allocation for later
        stock_sum += stock_dic[i] * 100
        
    if(crypto_sum  > crypto_max*100):

        adjusted_dict = {} #this will be the new allocation dictionary 

        crypto_relative_percent = {} #gets the right crypto allocations after the maximum is in place
        
        for i in crypto_list: 
            crypto_relative_percent[i] = ((stock_dic[i] * 100)/ crypto_sum)
            adjusted_dict[i] = (crypto_relative_percent[i]*(crypto_max*100))/100
        
        
        
        
        stock_relative_percent = {} #gets the right stock allocations after maximum
        for i in only_stock_list: 
            stock_relative_percent[i] = ((stock_dic[i] * 100)/ stock_sum)
            adjusted_dict[i] = (stock_relative_percent[i]* (100-(crypto_max*100)))/100


        daily_opt = pd.Series(adjusted_dict).as_format(".2%") #make a series like the origonal
        
        #preparing the data again but with the new series 
        stock_dic = daily_opt.to_dict()

        for key in stock_dic: #makes percents numbers 
            stock_dic[key] = float(stock_dic[key].replace('%', ''))
            stock_dic[key] = stock_dic[key]/100
        
        stock_list = list(stock_dic.keys()) #convert the dictionary into lists for plotting
        percent_list = list(stock_dic.values())

        temp = []
        temp_stock = []
        for i in range(len(percent_list)): #Takes out values of 0 
            if (percent_list[i] != 0):
                temp.append(percent_list[i])
                temp_stock.append(stock_list[i])

        stock_list = temp_stock
        percent_list= temp

   
    ####################################################################################################################################################
    ############### CREATE STRATEGY AND GRAPH
    ####################################################################################################################################################

    strategy_op = bt.Strategy(name, 
                                [bt.algos.RunMonthly(), 
                                bt.algos.SelectAll(), 
                                bt.algos.WeighSpecified(**stock_dic),
                                bt.algos.Rebalance()]) #Creating strategy

    strategy_port = bt.Strategy('Equally Weighted Portfolio', 
                                [bt.algos.RunMonthly(), 
                                bt.algos.SelectAll(), 
                                bt.algos.WeighEqually(),
                                bt.algos.Rebalance()]) #Creating strategy

    test_op = bt.Backtest(strategy_op, data)
    results_op_d = bt.run(test_op)

    test_port = bt.Backtest(strategy_port, data)
    results_port = bt.run(test_port)

    #table
    fig_opt_table = optomize_table(daily_opt)
    
    #pie_colors = [strategy_color, P6040_color, spy_color, agg_color, '#7496F3', '#B7FA59', 'brown', '#EE4444', 'gold']
    fig_pie = plotly_pie(stock_list, percent_list)

    results_list = [results_op_d, results_port, results_spy, results_agg]
    fig_line = line_chart(results_list)
    fig_line.update_layout(template = onramp_template_dashboard)

    
    fig_scat = scatter_plot(results_list) #scatter function in functions
    fig_scat.update_layout(template = onramp_template_dashboard)

    fig_stats = stats_table(results_list)

    fig_month = monthly_table(results_list)
    fig_month.update_layout(height = 950)

    return fig_pie, fig_line, fig_opt_table, fig_scat, fig_stats, fig_month

##############################################################################################################################################################