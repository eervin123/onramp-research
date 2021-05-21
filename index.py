import dash_core_components as dcc
import dash_html_components as html
import dash

from dash_app import dash_app
from dash_app import server
from layouts import dashboard_page, vol_page, heatmap_page, heatmap_timeline_page
import callbacks


dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dashboard':
         return dashboard_page
    elif pathname == '/apps/volatility-chart':
         return vol_page
    elif pathname == '/apps/heatmap':
         return heatmap_page
    elif pathname == '/apps/heatmap-timeline':
         return heatmap_timeline_page
    else:
        return dashboard_page # This is the "home page"

if __name__ == '__main__':
    dash_app.run_server(debug=True)
