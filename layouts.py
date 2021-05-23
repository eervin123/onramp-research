import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from dash_app import dash_app
import datetime
import pytz

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    "onramp-dark": "#131c4f",
    "dark-blue-grey": "#424972",
    "medium-blue-grey": "#424972",
    "superdark-green": "#424972",
    "dark-green": "#424972",
    "medium-green": "#b8bbca",
    "light-green": "#b8bbca",
    "pink-red": "#00eead",
    "dark-pink-red": "#00eead",
    "white": "rgb(251, 251, 252)",
    "light-grey": "#b0b6bd",
}

externalgraph_rowstyling = {"margin-left": "15px", "margin-right": "15px"}

externalgraph_colstyling = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": corporate_colors["light-grey"],
    "background-color": corporate_colors["onramp-dark"],
    "box-shadow": "0px 0px 17px 0px rgba(186, 218, 212, .5)",
    "padding-top": "10px",
}

filterdiv_borderstyling = {
    "border-radius": "0px 0px 10px 10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": "#424972",
    "background-color": "#424972",
    "box-shadow": "2px 5px 5px 1px rgba(255, 101, 131, .5)",
}

navbarcurrentpage = {
    "text-decoration": "underline",
    "text-decoration-color": corporate_colors["pink-red"],
    "text-shadow": "0px 0px 1px rgb(251, 251, 252)",
    "font-family": "Circular STD",
}

recapdiv = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": "#424972",
    "margin-left": "15px",
    "margin-right": "15px",
    "margin-top": "15px",
    "margin-bottom": "15px",
    "padding-top": "5px",
    "padding-bottom": "5px",
    "background-color": "rgb(251, 251, 252, 0.1)",  # behind slider
}

recapdiv_text = {
    "text-align": "left",
    "font-weight": "350",
    "color": corporate_colors["white"],
    "font-size": "1.5rem",
    "letter-spacing": "0.04em",
}

####################### Corporate chart formatting

corporate_title = {"font": {"size": 16, "color": corporate_colors["white"]}}

corporate_xaxis = {
    "showgrid": False,
    "linecolor": corporate_colors["light-grey"],
    "color": corporate_colors["light-grey"],
    "tickangle": 315,
    "titlefont": {"size": 12, "color": corporate_colors["light-grey"]},
    "tickfont": {"size": 11, "color": corporate_colors["light-grey"]},
    "zeroline": False,
}

corporate_yaxis = {
    "showgrid": True,
    "color": corporate_colors["light-grey"],
    "gridwidth": 0.5,
    "gridcolor": corporate_colors["dark-green"],
    "linecolor": corporate_colors["light-grey"],
    "titlefont": {"size": 12, "color": corporate_colors["light-grey"]},
    "tickfont": {"size": 11, "color": corporate_colors["light-grey"]},
    "zeroline": False,
}

corporate_font_family = "Circular STD"

corporate_legend = {
    "orientation": "h",
    "yanchor": "bottom",
    "y": 1.01,
    "xanchor": "right",
    "x": 1.05,
    "font": {"size": 9, "color": corporate_colors["light-grey"]},
}  # Legend will be on the top right, above the graph, horizontally

corporate_margins = {
    "l": 5,
    "r": 5,
    "t": 45,
    "b": 15,
}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font={"family": corporate_font_family},
    title=corporate_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=corporate_xaxis,
    yaxis=corporate_yaxis,
    height=270,
    legend=corporate_legend,
    margin=corporate_margins,
)


####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

df = pd.read_csv(
    "datafiles/Slider_data.csv",
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
    ],
)
df["Date"] = pd.to_datetime(df["Date"], unit="ms")
df = df.set_index("Date")

# Stats Data
df_stats = pd.read_csv(
    "datafiles/Slider_data.csv",
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
)
df_stats = df_stats.dropna()


####################################################################################################
# 000 - DATA AND FUNCTIONS FOR NON DYNAMIC STUFF
####################################################################################################
pairs = [
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

pairs_new = [
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

price_data = {}

# ----------------------------------------Volitility ----------------------------------------------------------
def get_coin_data(symbol, db, coindata_day):
    df = pd.read_csv(f"datafiles/{symbol}_data.csv")
    res = df[
        ["timestamp", "price_open", "price_high", "price_low", "price_close", "volume"]
    ].to_dict(orient="list")
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

    if data_interval not in ["1T", "30T", "1D"]:
        raise ValueError

    if data_interval == "1T":
        trading_periods = 60 * 24
    elif data_interval == "30T":
        trading_periods = 2 * 24
    else:
        trading_periods = 1

    percent_change = price.pct_change() * 100
    standard_deviation = percent_change.rolling(period_value * trading_periods).std()
    # formula sqrt(to_hour * daily_hours * days)
    volatility = standard_deviation * ((trading_periods * 365) ** 0.5)
    return volatility


def calc_volatility(pairs, db, coindata_day):
    """
    Get Graph For Each Coin You Want
    """
    # create visuals

    df_all = dict()
    for sp in pairs:
        # calculate vol for each coin and graph
        tmp = pd.DataFrame(get_coin_data(sp, db, coindata_day))
        tmp = tmp[["price_close", "timestamp"]]
        tmp.timestamp = pd.to_datetime(tmp.timestamp, unit="s")
        tmp.set_index("timestamp", inplace=True)
        for t in [14, 30, 90]:
            df_all[f'{sp.split("-",1)[0]}_vol_{t}'] = volatility(
                tmp.price_close, t, data_interval="1D"
            )

    return pd.DataFrame(df_all).dropna(how="all")


df = calc_volatility(pairs, "Nothing", "Nothing")

today = datetime.datetime.now(tz=pytz.utc).date()
xd = today - datetime.timedelta(days=30)


def graph_volatility(df, coins, xd):
    source = "Binance"
    yaxis_dict = dict(
        title="Rolling 30-Day Volatility",
        hoverformat=".2f",
        ticks="outside",
        tickcolor="#53585f",
        ticklen=8,
        tickwidth=3,
        tick0=0,
        tickprefix="                 ",
    )
    vols = [14, 30, 90]
    colors = 3 * [
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
                x=-0.12,
                y=1.09,
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
        images=[
            dict(
                source="/static/onramp-logo.png",
                xref="paper",
                yref="paper",
                x=1.05,
                y=1.05,
                sizex=0.21,
                sizey=0.21,
                xanchor="right",
                yanchor="bottom",
            )
        ],
        height=700,
        width=1000,
        dragmode="zoom",
        xaxis=dict(
            title="Date",
            ticks="inside",
            ticklen=6,
            tickwidth=3,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=6, label="6m", step="month", stepmode="backward"),
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
        font=dict(size=14),
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

    return fig


c = xd.strftime("%Y-%m-%d")
vol_fig = graph_volatility(df, pairs, c)


# -----------------------------------------------------------Heatmap------------------------------------------
custom_scale = [
    # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
    [0, "#00eead"],
    [0.1, "#00eead"],
    # Let values between 10-20% of the min and max of z
    # have color rgb(20, 20, 20)
    [0.1, "#00d8b7"],
    [0.2, "#00d8b7"],
    # Values between 20-30% of the min and max of z
    # have color rgb(40, 40, 40)
    [0.2, "#00c0bd"],
    [0.3, "#00c0bd"],
    [0.3, "#00a9be"],
    [0.4, "#00a9be"],
    [0.4, "#0090b9"],
    [0.5, "#0090b9"],
    [0.5, "#0078ad"],
    [0.6, "#0078ad"],
    [0.6, "#00609c"],
    [0.7, "#00609c"],
    [0.7, "#004986"],
    [0.8, "#004986"],
    [0.8, "#00326b"],
    [0.9, "#00326b"],
    [0.9, "#131c4f"],
    [1.0, "#131c4f"],
]


def get_coin_data_new(symbol):
    df = pd.read_csv("datafiles/Multi_Asset_data.csv", usecols=["Timestamp", symbol])
    res = df.to_dict(orient="list")
    return res


def create_corr(pairs, db, coindata_day):
    vals = dict()
    for sp in pairs:
        data = get_coin_data(sp, db, coindata_day)
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


def create_corr_new(pairs, db, coindata_day):
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
        images=[
            dict(
                source="/static/onramp-logo.png",
                xref="paper",
                yref="paper",
                x=1.12,
                y=1.08,
                sizex=0.25,
                sizey=0.25,
                xanchor="right",
                yanchor="bottom",
            )
        ],
        title=f"Return Correlation - Close {date}",
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
                font=dict(size=10),
            )
        ],
        autosize=False,
        width=700,
        height=700,
        xaxis=dict(ticklen=1, tickcolor="#fff"),
        yaxis=dict(ticklen=1, tickcolor="#fff"),
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
                colorscale=[[0.0, "#00eead"], [1, "#131c4f"]],
            )
        ],
        layout=layout,
    )

    return fig


corr_df = create_corr(pairs, "Nothing", "Nothing")

corr_df_new = create_corr_new(pairs_new, "Nothing", "Nothing")

heatmap_fig = graph_heatmap(corr_df, c)

heatmap_fig_new = graph_heatmap(corr_df_new, c)

# ---------------------------------------------------------Timeline--------------------------------------------


def graph_timeline(corr_df, xd):
    _font = dict(family="Raleway, Bold")
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
    updatemenus = list([dict(type="dropdown", active=0, y=1.5, x=0, buttons=buttons,)])

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
                y=-0.25,
                xref="paper",
                yref="paper",
                showarrow=False,
                text=f"*Source: {source}; Correlation data quoted here represents data as of {xd}.",
                font=dict(size=9),
            )
        ],
        title=dict(
            text="Crypto-Return Correlation", font=dict(_font, size=20, color="#000")
        ),
        xaxis=dict(
            title="Date",
            ticks="inside",
            ticklen=6,
            tickwidth=2,
            tickfont=_font,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            autorange=True,
            type="date",
            tickcolor="#53585f",
        ),
        yaxis=dict(
            axis_dict, title=f"{start_title} 6-Month Rolling Return Correlation"
        ),
        margin=dict(pad=5, b=125),
        legend=dict(orientation="h"),
        updatemenus=updatemenus,
    )

    fig = go.Figure(data=data, layout=layout)
    # fig.update_layout({
    #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    #     })

    return fig


heatmap_timeline_fig = graph_timeline(corr_df, c)

heatmap_timeline_fig_new = graph_timeline(corr_df_new, c)


#####################
# Header with logo
def get_header():

    header = html.Div(
        [
            html.Div(
                [], className="col-2"
            ),  # Same as img width, allowing to have the title centrally aligned
            html.Div(
                [
                    html.H1(
                        children="Onramp Academy Tools",
                        style={"textAlign": "center", "font": "Roboto"},
                    ),
                    html.H4(
                        children="Interactive Market Data and Tools to Explore the Cryptoasset Economy",
                        style={
                            "textAlign": "center",
                            "font": "Roboto",
                            "color": "#b0b6bd",
                        },
                    ),
                ],
                className="col-8",
                style={"padding-top": "1%"},
            ),
            html.Div(
                [
                    html.Img(
                        src=dash_app.get_asset_url("onramp-logo-small.png"),
                        height="43 px",
                        width="auto",
                    )
                ],
                className="col-2",
                style={"align-items": "center", "padding-top": "1%", "height": "auto"},
            ),
        ],
        className="row",
        style={"height": "4%", "background-color": corporate_colors["onramp-dark"]},
    )

    return header


#####################
# Nav bar
def get_navbar(p="dashboard"):

    navbar_dashboard = html.Div(
        [
            html.Div([], className="col-2"),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Dashboard", style=navbarcurrentpage),
                        href="/apps/dashboard",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Volatility Chart"),
                        href="/apps/volatility-chart",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [dcc.Link(html.H4(children="Heatmap"), href="/apps/heatmap")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Heatmap Timeline"),
                        href="/apps/heatmap-timeline",
                    )
                ],
                className="col-2",
            ),
            html.Div([], className="col-3"),
        ],
        className="row",
        style={
            "background-color": corporate_colors["dark-green"],  # behind nav
            "box-shadow": "2px 5px 5px 1px #00eead",
        },
    )

    navbar_vol = html.Div(
        [
            html.Div([], className="col-2"),
            html.Div(
                [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Volatility Chart", style=navbarcurrentpage),
                        href="/apps/volatility-chart",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [dcc.Link(html.H4(children="Heatmap"), href="/apps/heatmap")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Heatmap Timeline"),
                        href="/apps/heatmap-timeline",
                    )
                ],
                className="col-2",
            ),
            html.Div([], className="col-3"),
        ],
        className="row",
        style={
            "background-color": corporate_colors["dark-green"],  # behind nav
            "box-shadow": "2px 5px 5px 1px #00eead",
        },
    )

    navbar_heatmap = html.Div(
        [
            html.Div([], className="col-2"),
            html.Div(
                [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Volatility Chart"),
                        href="/apps/volatility-chart",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Heatmap", style=navbarcurrentpage),
                        href="/apps/heatmap",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Heatmap Timeline"),
                        href="/apps/heatmap-timeline",
                    )
                ],
                className="col-2",
            ),
            html.Div([], className="col-3"),
        ],
        className="row",
        style={
            "background-color": corporate_colors["dark-green"],  # behind nav
            "box-shadow": "2px 5px 5px 1px #00eead",
        },
    )

    navbar_timeline = html.Div(
        [
            html.Div([], className="col-2"),
            html.Div(
                [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Volatility Chart"),
                        href="/apps/volatility-chart",
                    )
                ],
                className="col-2",
            ),
            html.Div(
                [dcc.Link(html.H4(children="Heatmap"), href="/apps/heatmap")],
                className="col-2",
            ),
            html.Div(
                [
                    dcc.Link(
                        html.H4(children="Heatmap Timeline", style=navbarcurrentpage),
                        href="/apps/heatmap-timeline",
                    )
                ],
                className="col-2",
            ),
            html.Div([], className="col-3"),
        ],
        className="row",
        style={
            "background-color": corporate_colors["dark-green"],  # behind nav
            "box-shadow": "2px 5px 5px 1px #00eead",
        },
    )

    if p == "dashboard":
        return navbar_dashboard
    elif p == "volatility":
        return navbar_vol
    elif p == "heatmap":
        return navbar_heatmap
    elif p == "timeline":
        return navbar_timeline
    else:
        return navbar_dashboard


#####################
# Empty row


def get_emptyrow(h="45px"):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div(
        [html.Div([html.Br()], className="col-12")],
        className="row",
        style={"height": h},
    )

    return emptyrow


####################################################################################################
# 001 - Portfilio Modeling
####################################################################################################

dashboard_page = html.Div(
    [
        #####################
        # Row 1 : Header
        get_header(),
        #####################
        # Row 2 : Nav bar
        get_navbar("dashboard"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Impact of Adding BTC to a 60/40 Portfolio",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Br(),
                        html.H4(
                            children="Cryptoassets such as Bitcoin (BTC) and Ether (ETH) have emerged as an asset class that clients are interested in holding long term. Cryptoassets are usually held away from advisors. As a trusted confidante and risk manager, Advisors should have access to tools and insights that help them manage portfolios holistically. Use the slider to show the performance change of adding 1-5% BTC to a typical 60/40 portfolio. ",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        # $html.Br(),
                                        html.H3(
                                            children="100% 60/40",
                                            style={"color": corporate_colors["white"]},
                                        ),
                                    ],
                                    className="col-2 slider-text",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        dcc.Slider(
                                            id="slider_num",
                                            min=0,
                                            max=10,
                                            value=0,
                                            step=0.5,
                                            marks={
                                                0: {'label':'0% BTC', 'style':{'color':'white'}},
                                                2.5 : {'label':'2.5% BTC', 'style':{'color':'white'}},
                                                5: {'label':'5% BTC', 'style':{'color':'white'}},
                                                7.5: {'label':'7.5% BTC', 'style':{'color':'white'}},
                                                10: {'label':'10% BTC', 'style':{'color':'white'}},
                                            }
                                        ),
                                    ],
                                    className="col-8",
                                ),
                                html.Div(
                                    [
                                        # html.Br(),
                                        html.H3(
                                            children="10% Bitcoin",
                                            style={"color": corporate_colors["white"]},
                                        ),
                                    ],
                                    className="col-2 slider-text",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAPS
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="pie_chart")], className="col-3"
                                ),
                                # Chart Column
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="line_chart", style={"responsive": True}
                                        )
                                    ],
                                    style={"margin": "auto"},
                                    className="col-5",
                                ),
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="scatter_plot")], className="col-4"
                                ),
                            ],
                            className="row",
                        ),  # Internal row
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="bar_chart_rr")], className="col-6"
                                ),
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="bar_chart_ss")], className="col-6"
                                ),
                                # Chart Column
                                html.Div([], className="col-4"),
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-10",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)


vol_page = html.Div(
    [
        #####################
        # Row 1 : Header
        get_header(),
        #####################
        # Row 2 : Nav bar
        get_navbar("volatility"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Rolling Volatility Charts",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Br(),
                        html.H4(
                            children="Advisors will now have remote access to held-away client cryptoasset accounts via Read-Only or direct access to allocate on clients’ behalf via the Onramp platform, allowing Advisors to comprehensively manage clients’ assets and risk. Here we show how dynamic volatility can be in the cryptoasset ecosystem creating multiple opportunities to reach out to clients and discuss their risk tolerance and ability to withstand this volatility. ",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        # $html.Br(),
                                        # html.H3(children= "100% 60/40",
                                        # style = {'color' : corporate_colors['white']}),
                                    ],
                                    className="col-2",
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : corporate_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-3'),
                                # Chart Column
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="vol_chart",
                                            figure=vol_fig,
                                            style={"responsive": True},
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-10",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)


heatmap_page = html.Div(
    [
        #####################
        # Row 1 : Header
        get_header(),
        #####################
        # Row 2 : Nav bar
        get_navbar("heatmap"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Correlation Matrix",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Br(),
                        html.H4(
                            children="Advisors can now manage the overall expected return, risk, Sharpe ratio, et cetera, of clients’ total mix of financial assets, including cryptocurrencies and decentralized finance. This heatmap, updated daily, shows current intra-asset correlations for: BTC, ETH, S&P500, All World Equities, High Yield, Global Hedge Funds, Gold, Emerging Market Indices, Russell 2000, Oil, Frontier Markets, and Biotech. Historical correlations are presented in the next tab.",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {
                                                    "label": "Crypto Correlation",
                                                    "value": "CC",
                                                },
                                                {
                                                    "label": "Asset Class Correlation",
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                #TODO: #1 style the dropdown to accommodate the text
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : corporate_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4'),
                                # Chart Column
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap",
                                            # figure = heatmap_fig_new,
                                            style={"responsive": True},
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-10",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)


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
            images=[
                dict(
                    source="/static/onramp-logo.png",
                    xref="paper",
                    yref="paper",
                    x=1.12,
                    y=1.08,
                    sizex=0.25,
                    sizey=0.25,
                    xanchor="right",
                    yanchor="bottom",
                )
            ],
            title=dict(
                text="Correlation Matrix",
                font=dict(size=30),
                x=.5,
            ),
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
                    font=dict(size=10),
                )
            ],
            autosize=False,
            width=700,
            height=700,
            xaxis=dict(ticklen=1, tickcolor="#fff"),
            yaxis=dict(ticklen=1, tickcolor="#fff"),
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
                    colorscale=[[0.0, "#00eead"], [1, "#131c4f"]],
                )
            ],
            layout=layout,
        )

        return fig

    if value == "CC":
        return graph_heatmap(corr_df, c)
    if value == "AC":
        return graph_heatmap(corr_df_new, c)


heatmap_timeline_page = html.Div(
    [
        #####################
        # Row 1 : Header
        get_header(),
        #####################
        # Row 2 : Nav bar
        get_navbar("timeline"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Onramp Heatmap Timeline",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Br(),
                        html.H4(
                            children="Advisors may have or receive questions about the value of adding cryptoassets, particularly BTC and ETH, to a traditional portfolio. Price returns speak for themselves but the history of their correlation to traditional assets is meaningful to holistic portfolio construction and client discussions. For example, the May 2021 drawdown in cryptoassets had very little correlation to the broader markets, illustrating its value as a minimally-correlated asset in a broader portfolio.",
                            style={"color": corporate_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {
                                                    "label": "Crypto Correlation",
                                                    "value": "CC",
                                                },
                                                {
                                                    "label": "Asset Class Correlation",
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : corporate_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4'),
                                # Chart Column
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap_timeline",
                                            # figure = heatmap_timeline_fig_new,
                                            style={"responsive": True},
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-10",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)


@dash_app.callback(
    dash.dependencies.Output("heatmap_timeline", "figure"),
    [dash.dependencies.Input("dropdown", "value")],
)
def update_timeline(value):
    def graph_timeline(corr_df, xd):
        _font = dict(family="Raleway, Bold")
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
            [dict(type="dropdown", active=0, y=1.07, x=0.2, buttons=buttons,),]
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
                    y=-0.25,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    text=f"*Source: {source}; Correlation data quoted here represents data as of {xd}.",
                    font=dict(size=9),
                )
            ],
            title=dict(
                text="Relative Correlation Over Time",
                font=dict(_font, size=40, color="#000"),
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
                    buttons=list(
                        [
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
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
            margin=dict(pad=5, b=15),
            legend=dict(orientation="h"),
            updatemenus=updatemenus,
        )

        fig = go.Figure(data=data, layout=layout)
        # fig.update_layout({
        #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        #     })

        return fig

    if value == "CC":
        return graph_timeline(corr_df, c)
    if value == "AC":
        return graph_timeline(corr_df_new, c)
