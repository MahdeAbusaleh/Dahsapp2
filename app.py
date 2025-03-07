import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
        dcc.Link('Exposure Sources | ', href='#exposure'),
        dcc.Link('Dose-Response Models | ', href='#models'),
        dcc.Link('Calculator | ', href='#calculator'),
        dcc.Link('FAQ | ', href='#faq'),
        dcc.Link('Conclusion', href='#conclusion')
    ], style={'textAlign': 'center', 'marginBottom': 20}),

    # Radiation Exposure Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source", yaxis_title="Dose (mSv)")
            }
        ),
    ]),

    # Dose-Response Models Section
    html.Div(id='models', children=[
        html.H3("Dose-Response Models: LNT vs. Threshold vs. Hormesis"),
        dcc.Graph(
            figure={
                "data": [
                    go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)', line=dict(color='red')),
                    go.Scatter(x=dose_values, y=threshold_risk, mode='lines', name='Threshold Model', line=dict(color='blue', dash='dash')),
                    go.Scatter(x=dose_values, y=hormesis_risk, mode='lines', name='Hormesis Model', line=dict(color='green', dash='dot')),
                ],
                "layout": go.Layout(title="Radiation Dose-Response Models", xaxis_title="Radiation Dose (mSv)", yaxis_title="Relative Risk")
            }
        ),
    ]),

    # Calculator Section
    html.Div(id='calculator', children=[
        html.H3("Personal Radiation Exposure Calculator"),
        dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider'),
        dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider'),
        html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20}),
    ]),

    # Video Section
    html.Div(id='video', children=[
        html.H3("Radiation Exposure Explained - Video Resource"),
        html.Iframe(
            src="https://www.youtube.com/embed/uzqsnxZBLNE",
            width="700",
            height="400",
            style={"border": "none", "display": "block", "margin": "auto"}
        ),
        html.P("This video provides a clear explanation of radiation exposure, different sources of radiation, and its effects on health."),
    ]),

    # Conclusion Section (Fixed Syntax Error)
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("""
            Understanding radiation exposure and risk is important in making informed decisions about health and safety.
            While radiation often has a stigma attached to it, it is an essential part of modern life, from medical diagnostics
            to energy production. By breaking down exposure sources, dose-response models, and personal risk factors, 
            this website aims to provide clarity on this complex subject.
            
            Different models of radiation risk such as the Linear No-Threshold (LNT), Threshold, and Hormesis reflect 
            the ongoing debate among scientists and regulators. The LNT model assumes all exposure carries some risk, 
            while the Threshold model suggests a safe limit, and the Hormesis model argues that low doses may be beneficial.
            
            In conclusion, radiation is a part of everyday life, and complete avoidance is neither necessary nor possible. 
            Instead, the key is risk awareness and responsible decision-making. Whether considering medical procedures, 
            occupational hazards, or lifestyle choices, having a solid understanding of radiation principles allows individuals 
            to take the correct precautions without unnecessary anxiety. This site serves as a foundation for further exploration 
            and encourages users to continue learning about radiation safety from reliable sources.
        """),
    ]),
])

# Callback for radiation dose calculator
@app.callback(
    dash.Output("total-dose-output", "children"),
    [dash.Input("flight-slider", "value"), dash.Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
