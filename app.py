import dash
app = dash.Dash(__name__, assets_ignore='.*bootstrap-journal.css.*')
server = app.server
app.config.suppress_callback_exceptions = True