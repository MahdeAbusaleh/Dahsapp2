import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

# Initialize the Dash app
app = dash.Dash(__name__)

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

# LNT vs. Threshold vs. Hormesis Models
dose_values = np.linspace(0, 100, 100)
lnt_risk = dose_values * 0.01
threshold_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10], [0, lambda x: (x - 10) * 0.01])
hormesis_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10],
                             [lambda x: -0.005 * x + 0.05, lambda x: (x - 10) * 0.01])

# Layout for the app
app.layout = html.Div([
    html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),
    html.H5("Created by Low Dose Radiation Explanation 1 Group 2025", style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

    # Navigation Bar
    html.Div([
        html.A('Exposure Sources | ', href='#exposure', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Dose-Response Models | ', href='#models', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Calculator | ', href='#calculator', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('FAQ | ', href='#faq', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Conclusion', href='#conclusion', style={'cursor': 'pointer', 'textDecoration': 'none'})
    ], style={'textAlign': 'center', 'marginBottom': 20}),

    # Radiation Exposure Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source",
                                    yaxis_title="Dose (mSv)")
            }
        ),
    ]),

    # Dose-Response Models Section
    html.Div(id='models', children=[
        html.H3("Dose-Response Models: LNT vs. Threshold vs. Hormesis"),
        dcc.Graph(
            figure={
                "data": [
                    go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)',
                               line=dict(color='red')),
                    go.Scatter(x=dose_values, y=threshold_risk, mode='lines', name='Threshold Model',
                               line=dict(color='blue', dash='dash')),
                    go.Scatter(x=dose_values, y=hormesis_risk, mode='lines', name='Hormesis Model',
                               line=dict(color='green', dash='dot')),
                ],
                "layout": go.Layout(title="Radiation Dose-Response Models", xaxis_title="Radiation Dose (mSv)",
                                    yaxis_title="Relative Risk")
            }
        ),
    ]),

    # Calculator Section
    html.Div(id='calculator', children=[
        html.H3("Personal Radiation Exposure Calculator"),
        html.Label("Number of flights per year (NYC to LA equivalent):"),
        dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider'),
        html.Label("Number of chest X-rays per year:"),
        dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider'),
        html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20}),
    ]),

    # FAQ Section
    html.Div(id='faq', children=[
        html.H3("Frequently Asked Questions (FAQ)"),
        html.Details([
            html.Summary("What are Sv and mSv?"),
            html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international unit for dose equivalent. "
                   "mSv = millisievert, which is 1/1000 of a Sv.")
        ]),
        html.Details([
            html.Summary("What is background radiation?"),
            html.P("Background radiation is natural radiation present in the environment, originating from cosmic rays, the Earth's crust, and internal sources.")
        ]),
        html.Details([
            html.Summary("How does radiation affect air travel?"),
            html.P("Radiation exposure increases slightly at higher altitudes. A typical flight from NYC to LA results in approximately 0.04 mSv exposure.")
        ]),
        html.Details([
            html.Summary("Is radiation from medical imaging safe?"),
            html.P("Medical imaging uses ionizing radiation to diagnose conditions. At low doses, the benefits outweigh the risks.")
        ]),
        html.Details([
            html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
            html.P("Ionizing radiation (X-rays, gamma rays) can remove electrons from atoms, potentially causing harm. Non-ionizing radiation (radio waves, microwaves) lacks this ability and is generally safer.")
        ]),
    ]),

    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("""
            Understanding radiation exposure and risk is important for making informed decisions about health and safety. 
            This website provides insight into different radiation exposure models, helping individuals evaluate risks 
            associated with medical procedures, air travel, and environmental radiation.

            Radiation exposure is a part of modern life. While excessive exposure can be harmful, scientific models suggest that 
            small doses may not be as dangerous as commonly believed. By presenting different perspectives—including the 
            LNT, Threshold, and Hormesis models—this website offers a balanced view of radiation safety.

            We encourage visitors to explore reliable resources, stay informed, and adopt a data-driven approach when evaluating radiation risks.
        """),
    ]),

    # Callback for radiation dose calculator
    html.Div([
        html.Label("Estimated Annual Radiation Dose:"),
        html.Div(id="total-dose-output", style={'fontSize': 20, 'marginTop': 20})
    ])
])

# Callback for calculator
@app.callback(
    dash.Output("total-dose-output", "children"),
    [dash.Input("flight-slider", "value"), dash.Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

# Server Setup for Deployment on Render
if __name__ == "__main__":
    from waitress import serve
    serve(app.server, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
