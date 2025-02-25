import dash
from dash import dcc, html

# Initialize the app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Test Website"),
    html.P("This is a test version of the Dash app."),
    dcc.Graph(
        figure={
            "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "line", "name": "Test Data"}],
            "layout": {"title": "Sample Graph"}
        }
    )
])

# Run server
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
