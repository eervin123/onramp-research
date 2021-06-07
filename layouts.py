import dash_core_components as dcc
import dash_html_components as html
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Row import Row
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash_app import dash_app
from formatting import onramp_colors, externalgraph_rowstyling, externalgraph_colstyling, recapdiv
from helpers import get_coin_data, get_coin_data_new, volatility, calc_volatility, calc_volatility_btc_vol, calc_volatility_new, create_corr, create_corr_new


####################################################################################################
# 000 - BITCOIN VOLATILITY (NOT DYNAMIC YET)
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

df = calc_volatility_btc_vol(pairs) #Used for Crypto Vol Chart 

df_btc = df[['BTC_vol_30', 'BTC_vol_60', 'BTC_vol_7']] #Annualized bitcoin vol chart

df_btc.columns = ['Ann. 30D Volatility', 'Ann. 60D Volatility', 'Ann. 7D Volatility']

for col in df_btc.columns:
    df_btc[col] = df_btc[col].map(lambda element: element/100)

avg_7 = df_btc["Ann. 7D Volatility"].mean()
avg_30 = df_btc["Ann. 30D Volatility"].mean()
avg_60 = df_btc["Ann. 60D Volatility"].mean()
df_btc["Avg. 30D Volatility"] = avg_30

def graph_btc_vol(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter( x = df.index, y = df['Ann. 30D Volatility'], name = 'Ann. 30D Volatility', line = dict(color = "#00EEAD", width = 2, dash = 'solid')))
    fig.add_trace(go.Scatter( x = df.index, y = df['Ann. 60D Volatility'], name = 'Ann. 60D Volatility', line = dict(color = "white", width = 2, dash = 'solid')))
    fig.add_trace(go.Scatter( x = df.index, y = df['Ann. 7D Volatility'], name = 'Ann. 7D Volatility', line = dict(color = "#B0B6BD", width = 2, dash = 'dot')))
    fig.add_trace(go.Scatter( x = df.index, y = df['Avg. 30D Volatility'], name = 'Avg. 30D Volatility', line = dict(color = "white", width = 2, dash = 'dash')))
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid=False) 
    fig.update_layout(yaxis_tickformat="%")
    fig.update_layout(
        legend=dict(
            orientation="h", yanchor="top", xanchor="center", y = 1.1, x = .5, font = {"size": 17}
            
        ),
        font=dict(family="Roboto", color="white"),
        title={
            "text": "<b>Annualized 30D & 60D Volatility - Bitcoin<b>",
            "y": 1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis=dict(
                title="Date",
                ticks="inside",
                ticklen=6,
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
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    #fig.update_xaxes(ticks = 'outside', tickwidth=2, tickcolor='white', ticklen=10)
    fig.update_xaxes(tickfont = {'size': 14})
    fig.update_yaxes(tickfont = {'size': 14})
    fig.update_yaxes(side="left", nticks=8)
    fig.update_layout(titlefont=dict(size=30, color="white", family="Roboto"))

    return fig

def btc_vol_table(a7, a30, a60, df_btc):
    labels = ['<b>Volatility<b>', '<b>Average<b>', '<b>Current<b>']
    fig = go.Figure(data=[go.Table(
                                header=dict(values= labels,
                                            line_color= 'white',
                                            fill_color= '#b0b6bd',
                                            align=['left','center', 'center'],
                                            height = 50,
                                            font=dict(color='black', size=30, family = "roboto")),
                                cells=dict(values=[['Ann. 7D Volatility', 'Ann. 30D Volatility', 'Ann. 60D Volatility'], [str(round(a7*100, 2))+'%', str(round(a30*100, 2))+'%', str(round(a60*100, 2))+'%'], [str(round(df_btc['Ann. 7D Volatility'].iloc[-1]*100, 2))+'%', str(round(df_btc['Ann. 30D Volatility'].iloc[-1]*100, 2))+'%', str(round(df_btc['Ann. 60D Volatility'].iloc[-1]*100, 2))+'%']],
                                            line_color = 'white',
                                            height = 40,
                                            font = dict(color = 'white', size = 20, family = "roboto"),
                                            fill_color = '#131c4f' )) ])
    fig.update_layout(margin = dict(l=1, r=0, t=0, b=0))
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    return fig

btc_vol_table = btc_vol_table(avg_7, avg_30, avg_60, df_btc)
btc_vol_fig = graph_btc_vol(df_btc)




####################################################################################################
# 000 - LAYOUTS
####################################################################################################


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
        style={"height": "4%", "background-color": onramp_colors["dark_blue"]},
    )

    return header

#####################
# Nav bar
def get_navbar(p="dashboard"):

    navbar_dashboard = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard", active=True, href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility", href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    navbar_vol = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart",active=True, href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility", href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    navbar_heatmap = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix",active=True, href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility", href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    navbar_timeline = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", active=True, href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility",  href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    btc_vol = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility", active=True, href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    navbar_custom = dbc.Row([
        dbc.Col( width = {"size" : 0}, className = "mr-3" ),
        dbc.Col([
        dbc.Nav(
        [
        dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Bitcoin Volatility", href="/apps/bitcoin-volatility", style = {"color": "black"})),
        dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", active=True, href="/apps/custom-dashboard", style = {"color": "black"})),
        ],
        pills=True, 
        )
        ])
    ], className = "bg-white")

    # navbar_dashboard = html.Div(
    #     [
    #         html.Div([], className="col-1"),
    #         html.Div(
    #             [   html.Div(
    #                      [
    #                  dbc.Tabs(
    #                     [
    #                         dbc.Tab(label="Tab 1", tab_id="tab-1"),
    #                         dbc.Tab(label="Tab 2", tab_id="tab-2"),
    #                     ],
    #                     id="tabs",
    #                     active_tab="tab-1",
    #                 ),
    #                 html.Div(id="content"),
    #                         ]
    #                     ),


    #                 dcc.Link(
    #                     html.H4(children="Dashboard", style=navbarcurrentpage),
    #                     href="/apps/dashboard",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Volatility Chart"),
    #                     href="/apps/volatility-chart",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Matrix"),
    #                     href="/apps/correlation-matrix",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Over Time"),
    #                     href="/apps/correlation-timeline",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
            
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Bitcoin Rolling Volatility"),
    #                     href="/apps/bitcoin-volatility",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div([], className="col-3"),
    #     ],
    #     className="row",
    #     style={
    #         "background-color": onramp_colors["dark-green"],  # behind nav
    #         "box-shadow": "2px 5px 5px 1px #00eead",
    #     },
    # )

    # navbar_vol = html.Div(
    #     [
    #         html.Div([], className="col-1"),
    #         html.Div(
    #             [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Volatility Chart", style=navbarcurrentpage),
    #                     href="/apps/volatility-chart",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Matrix"),
    #                     href="/apps/correlation-matrix",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Over Time"),
    #                     href="/apps/correlation-timeline",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #         [
    #             dcc.Link(
    #                 html.H4(children="Bitcoin Rolling Volatility"),
    #                 href="/apps/bitcoin-volatility",
    #             )
    #         ],
    #         className="col-2",
    #         ),
            
    #         html.Div([], className="col-3"),
    #     ],
    #     className="row",
    #     style={
    #         "background-color": onramp_colors["dark-green"],  # behind nav
    #         "box-shadow": "2px 5px 5px 1px #00eead",
    #     },
    # )

    # navbar_heatmap = html.Div(
    #     [
    #         html.Div([], className="col-1"), #Empty Col
            
            
    #         html.Div(
    #             [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Volatility Chart"),
    #                     href="/apps/volatility-chart",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Matrix", style=navbarcurrentpage),
    #                     href="/apps/correlation-matrix",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Over Time"),
    #                     href="/apps/correlation-timeline",
    #                 )
    #             ],
    #             className="col-2",
    #         ),

    #         html.Div(
    #         [
    #             dcc.Link(
    #                 html.H4(children="Bitcoin Rolling Volatility"),
    #                 href="/apps/bitcoin-volatility",
    #             )
    #         ],
    #         className="col-2",
    #         ),
    #         html.Div([], className="col-3"),
    #     ],
    #     className="row",
    #     style={
    #         "background-color": onramp_colors["dark-green"],  # behind nav
    #         "box-shadow": "2px 5px 5px 1px #00eead",
    #     },
    # )

    # navbar_timeline = html.Div(
    #     [
    #         html.Div([], className="col-1"),
    #         html.Div(
    #             [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Volatility Chart"),
    #                     href="/apps/volatility-chart",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Matrix"),
    #                     href="/apps/correlation-matrix",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(
    #                         children="Correlation Over Time", style=navbarcurrentpage
    #                     ),
    #                     href="/apps/correlation-timeline",
    #                 )
    #             ],
    #             className="col-2",
    #         ),

    #         html.Div(
    #         [
    #             dcc.Link(
    #                 html.H4(children="Bitcoin Rolling Volatility"),
    #                 href="/apps/bitcoin-volatility",
    #             )
    #         ],
    #         className="col-2",
    #         ),

    #         html.Div([], className="col-3"),
    #     ],
    #     className="row",
    #     style={
    #         "background-color": onramp_colors["dark-green"],  # behind nav
    #         "box-shadow": "2px 5px 5px 1px #00eead",
    #     },
    # )

    # btc_vol = html.Div(
    #     [
    #         html.Div([], className="col-1"),
    #         html.Div(
    #             [dcc.Link(html.H4(children="Dashboard"), href="/apps/dashboard")],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Volatility Chart"),
    #                     href="/apps/volatility-chart",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(children="Correlation Matrix"),
    #                     href="/apps/correlation-matrix",
    #                 )
    #             ],
    #             className="col-2",
    #         ),
    #         html.Div(
    #             [
    #                 dcc.Link(
    #                     html.H4(
    #                         children="Correlation Over Time"
    #                     ),
    #                     href="/apps/correlation-timeline",
    #                 )
    #             ],
    #             className="col-2",
    #         ),

    #         html.Div(
    #         [
    #             dcc.Link(
    #                 html.H4(children="Bitcoin Rolling Volatility", style = navbarcurrentpage),
    #                 href="/apps/bitcoin-volatility",
    #             )
    #         ],
    #         className="col-2",
    #         ),

    #         html.Div([], className="col-3"),
    #     ],
    #     className="row",
    #     style={
    #         "background-color": onramp_colors["dark-green"],  # behind nav
    #         "box-shadow": "2px 5px 5px 1px #00eead",
    #     },
    # )

    if p == "dashboard":
        return navbar_dashboard
    elif p == "volatility":
        return navbar_vol
    elif p == "heatmap":
        return navbar_heatmap
    elif p == "timeline":
        return navbar_timeline
    elif p == "btc_vol":
        return btc_vol
    elif p == "custom":
        return navbar_custom
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
        # ##################### commented out for Nutech to place in iframe ########################
        # # Row 1 : Header
        # get_header(),
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
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Impact of Adding BTC to a 60/40 Portfolio",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Cryptoassets such as Bitcoin (BTC) and Ether (ETH) have emerged as an asset class that clients are interested in holding long term. Cryptoassets are usually held away from advisors. As a trusted confidante and risk manager, Advisors should have access to tools and insights that help them manage portfolios holistically. Use the slider to show the performance change of adding 1-5% BTC to a typical 60/40 portfolio. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        # $html.Br(),
                                        html.H3(
                                            children="100% 60/40",
                                            style={"color": onramp_colors["white"]},
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
                                                0: {
                                                    "label": "0% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                2.5: {
                                                    "label": "2.5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                5: {
                                                    "label": "5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                7.5: {
                                                    "label": "7.5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                10: {
                                                    "label": "10% BTC",
                                                    "style": {"color": "white"},
                                                },
                                            },
                                        ),
                                        html.Br()
                                    ],
                                    className="col-8",
                                ),
                                html.Div(
                                    [
                                        # html.Br(),
                                        html.H3(
                                            children="10% Bitcoin",
                                            style={"color": onramp_colors["white"]},
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
                                dbc.Col(
                                    [   
                                        html.Br(),
                                        #dcc.Graph(id="pie_chart"),
                                        dcc.Loading(id = "loading-icon1", 
                                                children=[html.Div(dcc.Graph(id='pie_chart'))], type="default")
                                        
                                        ], className="col-3", xs = 12, sm = 12, md = 12, lg = 3, xl = 3),
                                html.Div(

                                ),
                                # Chart Column
                                dbc.Col(
                                    [
                                        # dcc.Graph(
                                        #     id="line_chart", style={"responsive": True}
                                        # )
                                        html.Br(),
                                        dcc.Loading(id = "loading-icon2", 
                                                children=[html.Div(dcc.Graph(id='line_chart'))], type="default")

                                    ],
                                    style={"margin": "auto"},
                                    className="col-5", xs = 12, sm = 12, md = 12, lg = 5, xl = 5
                                ),
                                # Chart Column
                                dbc.Col(
                                    [
                                        #dcc.Graph(id="scatter_plot")
                                        html.Br(),
                                        dcc.Loading(id = "loading-icon3", 
                                                children=[html.Div(dcc.Graph(id='scatter_plot'))], type="default")
                                        
                                    
                                    ], className="col-4", xs = 12, sm = 12, md = 12, lg = 4, xl = 4

                                ),
                            ],
                            className="row",
                        ),  # Internal row
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                dbc.Col(
                                    [   #html.Br(),
                                        #dcc.Graph(id="bar_chart_rr")
                                        dcc.Loading(id = "loading-icon4", 
                                                children=[html.Div(dcc.Graph(id='bar_chart_rr'))], type="default")
                                    
                                    
                                    ], className="col-6", xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                                ),
                                # Chart Column
                                dbc.Col(
                                    [   
                                        #html.Br(),
                                        #dcc.Graph(id="bar_chart_ss")
                                        dcc.Loading(id = "loading-icon5", 
                                                children=[html.Div(dcc.Graph(id='bar_chart_ss'))], type="default")
                                    ], className="col-6", xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
                                html.Div(

                                ),
                                # Chart Column
                                html.Div([], className="col-4"),
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 002 - Volatility over Time Page
####################################################################################################
vol_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
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
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Rolling Volatility Charts",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors will now have remote access to held-away client cryptoasset accounts via Read-Only or direct access to allocate on clients’ behalf via the Onramp platform, allowing Advisors to comprehensively manage clients’ assets and risk. Here we show how dynamic volatility can be in the cryptoasset ecosystem creating multiple opportunities to reach out to clients and discuss their risk tolerance and ability to withstand this volatility. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",  # TODO @cyrus let's use these names going forward.
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
                                        # style = {'color' : onramp_colors['white']}),
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
                                        # dcc.Graph(
                                        #     id="vol_chart", style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_vol",
                                            children=[
                                                
                                                    dcc.Graph(
                                                        id="vol_chart",
                                                        style={"responsive": True},
                                                    )
                                                
                                            ],
                                            type="default",
                                            
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
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 003 - Bitcoin Volatility Page
####################################################################################################
btc_vol_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
        # Row 2 : Nav bar
        get_navbar("btc_vol"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Annualized Bitcoin Volatility",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors will now have remote access to held-away client cryptoasset accounts via Read-Only or direct access to allocate on clients’ behalf via the Onramp platform, allowing Advisors to comprehensively manage clients’ assets and risk. Here we show how dynamic volatility can be in the cryptoasset ecosystem creating multiple opportunities to reach out to clients and discuss their risk tolerance and ability to withstand this volatility. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                # html.Div(
                                #     [
                                #         dcc.Dropdown(
                                #             id="dropdown",
                                #             options=[
                                #                 {"label": "Crypto", "value": "CC",},
                                #                 {
                                #                     "label": "Mixed Asset Classes",  # TODO @cyrus let's use these names going forward.
                                #                     "value": "AC",
                                #                 },
                                #             ],
                                #             value="AC",
                                #         ),
                                #     ],
                                #     className="col-3",
                                # ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
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
                                        # dcc.Graph(
                                        #     id="vol_chart", style={"responsive": True},
                                        # )
                                        dcc.Loading(id = "loading-icon_btc_vol", 
                                                children=[html.Div(dcc.Graph(id='btc_vol_chart', figure = btc_vol_fig, style = {"responsive": True, "width": "100%", "height": "70vh"}))], type="default"),
                                        
                                        dcc.Loading(id = "loading-icon_btc_vol_table", 
                                                children=[html.Div(dcc.Graph(id='btc_vol_chart_t', figure = btc_vol_table, style = {"responsive": True, "width": "95%", "height": "70vh"}))], type="default")
                                        
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-8",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 004 - Correlation Matrix Heatmap Page
####################################################################################################
heatmap_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
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
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Correlation Matrix",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors can now manage the overall expected return, risk, Sharpe ratio, et cetera, of clients’ total mix of financial assets, including cryptocurrencies and decentralized finance. This heatmap, updated daily, shows current intra-asset correlations for: BTC, ETH, S&P500, All World Equities, High Yield, Global Hedge Funds, Gold, Emerging Market Indices, Russell 2000, Oil, Frontier Markets, and Biotech. Historical correlations are presented in the next tab.",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                    # TODO: #1 style the dropdown to accommodate the text
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
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
                                        # dcc.Graph(
                                        #     id="heatmap",
                                        #     # figure = heatmap_fig_new,
                                        #     style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_heat",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="heatmap",
                                                        style={"responsive": True},
                                                    )
                                                )
                                            ],
                                            type="default",
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
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 005 - Correlation over time (Heatmap over time) Page
####################################################################################################
heatmap_timeline_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
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
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Correlation Over Time",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors may have or receive questions about the value of adding cryptoassets, particularly BTC and ETH, to a traditional portfolio. Price returns speak for themselves but the history of their correlation to traditional assets is meaningful to holistic portfolio construction and client discussions. For example, the May 2021 drawdown in cryptoassets had very little correlation to the broader markets, illustrating its value as a minimally-correlated asset in a broader portfolio.",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",
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
                                        # style = {'color' : onramp_colors['white']}),
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
                                        # dcc.Graph(
                                        #     id="heatmap_timeline",
                                        #     # figure = heatmap_timeline_fig_new,
                                        #     style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_time",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="heatmap_timeline",
                                                        style={"responsive": True},
                                                    )
                                                )
                                            ],
                                            type="default",
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
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 005 - Custom Strategy Page
####################################################################################################

def Inputs():

    inputs_ = dbc.Card([
            dbc.CardHeader(children= html.H3("Inputs"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
            dbc.CardBody([
                #Inputs 1 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker1",
                            type= 'text',
                            value = "spy",
                            placeholder= "Enter Ticker",
                            debounce = True,
                            style = {"width" : "100%"}

                        ),
                    width={'size':4}, className= " mb-4", 
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation1",
                            value = "40",
                            type= 'text',
                            placeholder= "Enter Allocation %",
                            style = {"width" : "100%"}

                        ), width={'size': 6, 'offset':1},
                    ),
                ]),

                #Inputs 2 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker2",
                            type= 'text',
                            value = 'agg',
                            placeholder= "Enter Ticker",
                            style = {"width" : "100%"}

                        ),
                    width={'size':4}, className= "mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation2",
                            type= 'text',
                            value = "20",
                            placeholder= "Enter Allocation %",
                            style = {"width" : "100%"}

                        ), width={'size':6, 'offset':1},
                    ),
                ]),

                #Inputs 3 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker3",
                            type= 'text',
                            value = 'btc-usd',
                            placeholder= "Enter Ticker",
                            style = {"width" : "100%"}

                        ),
                    width={'size':4}, className= "mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation3",
                            type= 'text',
                            value = '20',
                            placeholder= "Enter Allocation %",
                            style = {"width" : "100%"}

                        ), width={'size':6, 'offset':1},
                    ),
                ]),

                #Inputs 4 
                dbc.Row([
                    dbc.Col(
                        dcc.Input(
                            id = "Ticker4",
                            type= 'text',
                            value = 'tsla',
                            placeholder= "Enter Ticker",
                            style = {"width" : "100%"}

                        ),
                    width={'size':4}, className= "mb-4"
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Allocation4",
                            type= 'text',
                            value = "20",
                            placeholder= "Enter Allocation %",
                            style = {"width" : "100%"}

                        ), width={'size':6, 'offset':1},
                    ),
                ]),

                #Inputs 5 
                dbc.Row([
                    dbc.Col(
                    width={'size':4}, className= "mb-4" #Empty Col for Rebalance 
                    ), 

                    dbc.Col(
                        dcc.Input(
                            id = "Rebalance",
                            type= 'text',
                            placeholder= "Rebalance Threshold %",
                            style = {"width" : "100%"}

                        ), width={'size':6, 'offset':1}, className= "mb-4"
                    ),
                ]),

                #Submit Button
                dbc.Row([
                    
                    dbc.Col(
                        html.Button(
                            id = "submit_button",
                            children= "Create Strategy",
                            n_clicks=0,
                            style= {"width": "100%"}

                        ), width={'size':12, 'offset':0},
                    ),
                ]),
                
            ]), 
    ], className= "text-center mb-2 mr-2", style= {"height": "31rem"}, color= onramp_colors["dark_blue"], inverse= True,)

    return inputs_

def Description():

    descript = dbc.Card(
                dbc.CardBody([
                   
                            html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes.", 
                            style = {"fontSize": "vmin" }),
                            
                            html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes.",
                            style = {"fontSize": "vmin" })
                            
                
                ]), className= "text-center", style= {"height": "22rem"}, color= onramp_colors["dark_blue"], inverse= True
    )

    return descript

def DisplayPie():
    pie = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            
            dcc.Loading( id = "loading_pie", children=
            dcc.Graph(
                id = "pie_chart_c"
            )
            )
        ]),
    ],  className= "text-center mb-2 mr-2", style= {"height": "31rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return pie
           
def DisplayLineChart():
    line = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Performance"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_line", children=
            dcc.Graph(
                id = "line_chart_c",
                style= {"responsive": True}
            ))
        ]), 
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "31rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return line        

def DisplayScatter():
    scat = dbc.Card([
        dbc.CardHeader(children= html.H3("Risk vs. Return"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading-scatter", children=
            dcc.Graph(
                id = "scatter_plot_c",
                style= {"responsive": True}
            )
            )
        ]),  
    ], className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "31rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return scat        

def DisplayStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Performance Statistics"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_stats", children=
            dcc.Graph(
                id = "stats_table",
                style= {"responsive": True}
            )
            )
        ]),  
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "31rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

def DisplayReturnStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Recap"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_return1", children= 
                dcc.Graph(
                id = "balance_table",
                style= {"responsive": True}
                )
            ),
            dcc.Loading(id = "loading_returns2", children=
                dcc.Graph(
                id = "return_stats",
                style= {"responsive": True}
                )
            )
            
                            
        ])
    ],  className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "31rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats      

def DisplayMonthTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Breakdown"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading( id = "loading_month", children=
            dcc.Graph(
                id = "month_table",
                style= {"responsive": True}
            )
            )
        ])
    ],  className= "text-center", style= {"max-width" : "100%", "margin": "auto", "height": "59rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

custom_page = dbc.Container([
    
    get_navbar('custom'),
    #Title 
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H1(children="Custom Strategy Dashboard", style = {"color": onramp_colors["gray"]}), 
                    
                    html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes.", 
                            style = {"fontSize": "vmin", "color": onramp_colors["gray"]}),
                            
                    html.P(children= "Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. While the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannotavoid mediating disputes.",
                            style = {"fontSize": "vmin", "color": onramp_colors["gray"] })
                ]),
            className="text-center mb-2", color= onramp_colors["dark_blue"], inverse= True,), 
        width = 12)
    ),

    
    # Inputs | Pie Chart | Line Chart
    dbc.Row([
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    Inputs()
                ],  ),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 3, xl = 3),

        dbc.Col([
            
            dbc.Row([
                dbc.Col([
                    DisplayPie()
                ],  ),
            ]),
        ], xs = 12, sm = 12, md = 12, lg = 3, xl = 3),
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayLineChart()
                ]),
            )
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6 )
    ],no_gutters = True),

    # Stats | Scatter Plot | Return Recap
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayScatter()
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 4, xl = 4),


        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayReturnStats()
                    
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 4, xl = 4),
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayStats()
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 4, xl = 4)
    ], no_gutters = True),

    
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayMonthTable(),
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 12),
    ]),
], fluid=True)

