import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])

# Radiation exposure data (in millisieverts, mSv)
radiation_sources = {
    "Background Radiation (Annual Avg)": 3.0,
    "Chest X-ray": 0.1,
    "Dental X-ray": 0.005,
    "Mammogram": 0.4,
    "CT Scan (Abdomen)": 8.0,
    "Flight (NYC to LA)": 0.04,
    "Smoking (1 pack/day, Annual)": 70.0,
    "Fukushima Evacuation Zone (Annual)": 12.0,
}

df = pd.DataFrame(list(radiation_sources.items()), columns=["Source", "Dose (mSv)"])

# LNT Model (only)
dose_values = np.linspace(0, 100, 100)
lnt_risk = dose_values * 0.01

# App layout
app.layout = html.Div(style={"backgroundColor": "white", "minHeight": "100vh", "padding": "30px"}, children=[

    html.H1("Understanding Radiation Exposure and Risk", style={"textAlign": "center"}),

    html.Div(className="nav-links", style={"textAlign": "center", "marginBottom": "20px"}, children=[
        html.A("Exposure Sources | ", href="#exposure"),
        html.A("Dose-Response Models | ", href="#models"),
        html.A("Calculator | ", href="#calculator"),
        html.A("FAQ | ", href="#faq"),
        html.A("Video | ", href="#video"),
    ]),

    # Radiation Exposure Section
    html.Div(id="exposure", className="graph-container", children=[
        html.H3("Radiation Exposure from Common Sources", style={"textAlign": "center"}),
        dcc.Graph(figure={
            "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker=dict(color='blue'))],
            "layout": go.Layout(
                title=dict(text="Radiation Dose Comparison (mSv)", font=dict(color="black")),
                xaxis=dict(title=dict(text="Source", font=dict(color="black")), tickfont=dict(color="black"), tickangle=-20, automargin=True),
                yaxis=dict(title=dict(text="Dose (mSv)", font=dict(color="black")), tickfont=dict(color="black")),
                width=1200, height=500,
                plot_bgcolor="rgba(255,255,255,1)", paper_bgcolor="rgba(255,255,255,1)", font=dict(color="black")
            )
        }),
        html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels.", style={"textAlign": "center"})
    ]),

    # Dose-Response Models Section
    html.Div(id='models', children=[
        html.H3("Dose-Response Models: LNT", style={"textAlign": "center"}),
        dcc.Graph(figure={
            "data": [go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)', line=dict(color='red'))],
            "layout": go.Layout(
                title=dict(text="Radiation Dose-Response Models", font=dict(color="black")),
                xaxis=dict(title=dict(text="Radiation Dose (mSv)", font=dict(color="black")), tickfont=dict(color="black")),
                yaxis=dict(title=dict(text="Relative Risk", font=dict(color="black")), tickfont=dict(color="black")),
                plot_bgcolor="rgba(255,255,255,1)", paper_bgcolor="rgba(255,255,255,1)", font=dict(color="black")
            )
        }),
        html.P("The Linear No-Threshold (LNT) model assumes all radiation exposure carries some risk, no matter how small.", style={"textAlign": "center"})
    ]),

    # Calculator Section
    html.Div(id='calculator', children=[
        html.H3("Personal Radiation Exposure Calculator", style={"textAlign": "center"}),
        html.Label("Number of flights per year (NYC to LA equivalent):"),
        dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider'),
        html.Label("Number of chest X-rays per year:"),
        dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider'),
        html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20, "textAlign": "center"}),
    ]),

    # FAQ Section
    html.Div(id='faq', children=[
        html.H3("Frequently Asked Questions (FAQ)", style={"textAlign": "center"}),

        html.Details([
            html.Summary("What are Sv and mSv?"),
            html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international system unit for dose equivalent. "
                   "mSv = millisievert, which is 1/1000 of a Sv."),
        ]),

        html.Details([
            html.Summary("Is radiation from medical imaging safe?"),
            html.P("Medical imaging, such as CT scans and X-rays, delivers beams in the form of ionizing radiation to a specific part of the body "
                   "to visualize internal structures."),
            html.P("Although these involve low radiation doses, the benefits outweigh the potential risks."),
        ])
    ]),

    # Video Section
    html.Div(id='video', children=[
        html.H3("Radiation Exposure Explained - Video Resource", style={"textAlign": "center"}),
        html.Iframe(
            src="https://www.youtube.com/embed/uzqsnxZBLNE",
            width="700",
            height="400",
            style={"border": "none", "display": "block", "margin": "auto"}
        )
    ])
])

# Callback for radiation dose calculator
@app.callback(
    Output("total-dose-output", "children"),
    [Input("flight-slider", "value"), Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

# Run the app
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
