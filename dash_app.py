import dash
dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = dash_app.server
