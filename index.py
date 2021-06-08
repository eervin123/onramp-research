import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dash_app import dash_app

# from dash_app import server #Eric modified to move in code for gunicorn
from layouts import dashboard_page, vol_page, heatmap_page, heatmap_timeline_page, btc_vol_page, custom_page, optimizer_page
import callbacks

server = dash_app.server  # Eric moved this here after struggling with gunicorn

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

dash_app.title = "Onramp Academy Tools"


@dash_app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/apps/dashboard":
        return dashboard_page
    elif pathname == "/apps/volatility-chart":
        return vol_page
    elif pathname == "/apps/correlation-matrix":
        return heatmap_page
    elif pathname == "/apps/correlation-timeline":
        return heatmap_timeline_page
    elif pathname == "/apps/bitcoin-volatility":
        return btc_vol_page
    elif pathname == "/apps/custom-dashboard":
        return custom_page
    elif pathname == "/apps/portfolio-optimizer":
        return optimizer_page
    else:
        return dashboard_page  # This is the "home page"


if __name__ == "__main__":
    dash_app.run_server(debug=True)
