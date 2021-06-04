import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash_app import dash_app
import datetime
import pytz
from formatting import corporate_colors, externalgraph_rowstyling, externalgraph_colstyling, filterdiv_borderstyling, recapdiv, recapdiv_text, my_template, custom_scale
from helpers import get_coin_data, get_coin_data_new, volatility, calc_volatility, calc_volatility_btc_vol, calc_volatility_new, create_corr, create_corr_new


####################################################################################################
# 000 - IMPORT DATA DASHBOARD
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

colors = [corporate_colors["onramp-dark"], "#3fb6dc", "#f2a900"]
##################################################################################################################################################


####################################################################################################
# 000 - IMPORT DATA OTHER CHARTS
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


# ----------------------------------------Volitility ----------------------------------------------------------

df_mixed = calc_volatility_new(pairs_mixed) #Used for Mixed Asset Class Vol Chart

df_mixed = df_mixed[
    df_mixed.index > datetime.datetime(2020, 1, 15)
]  # make it so we only have 2020 data

df_vol = calc_volatility(pairs_crypto) #Used for Crypto Vol Chart 

today = datetime.datetime.now(tz=pytz.utc).date()
xd = today - datetime.timedelta(days=30) 

c = xd.strftime("%Y-%m-%d")


# -----------------------------------------------------------Heatmap------------------------------------------


corr_df = create_corr(pairs_crypto)

corr_df_new = create_corr_new(pairs_mixed)



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

    percent_dict = {"Traditional 60/40": 1 - float(value) / 100, "Bitcoin": float(value) / 100}

    # print(value)
    def graph_pie(percent_dictionary):

        colors_pie = [corporate_colors['onramp-dark'], "#f2a900"]  # BTC Orange
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
            template=my_template,
            height=500,
            hole = .2
        )
        fig.update_traces(hovertemplate="%{value:.0%}")
        # print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_layout(
            font=dict(family="Roboto", color="white"),
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
        fig.update_layout(titlefont=dict(size=24, color="white"))
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
            template=my_template,
            height = 500
            # width = 450
        )

        fig.update_yaxes(tickprefix="$", showgrid=False)  # the y-axis is in dollars
        x = 0.82
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.80
            ),
            font=dict(family="Roboto", color="white"),
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
        fig.update_layout(titlefont=dict(size=24, color="white", family="Circular STD"))
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
        colors = [corporate_colors['onramp-dark'], "#3fb6dc", "#f2a900"]
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
            template=my_template,
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
                  x=0.5, y=-.2, showarrow=False, font=dict(family="Roboto", color="white", size = 20))
        fig.update_layout(yaxis_tickformat="%")
        fig.update_layout(xaxis_tickformat="%")
        fig.update_layout(titlefont=dict(size=24, color="white"))
        fig.update_xaxes(title_font={"size": 20})
        fig.update_yaxes(title_font={"size": 20})
        fig.update_layout(margin=dict(l=100, r=50, t=20, b=0))

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

        colors = [corporate_colors['onramp-dark'], "#3fb6dc", "#f2a900"]
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
            template=my_template,
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
            "black",
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

