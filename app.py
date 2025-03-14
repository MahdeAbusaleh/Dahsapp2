import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import os  # Required for Render deployment

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

# Define dose values
dose_values = np.linspace(0, 100, 100)

# LNT Model: Risk increases linearly with dose
lnt_risk = dose_values * 0.01

# Threshold Model: No risk below a certain dose, then linear increase
threshold_dose = 10  # Assume risk starts at 10 mSv
threshold_risk = np.where(dose_values < threshold_dose, 0, (dose_values - threshold_dose) * 0.01)

# Hormesis Model: Beneficial at low doses, harmful at higher doses
hormesis_risk = -0.005 * np.exp(-dose_values / 20) + dose_values * 0.005

# Layout for the app
app.layout = html.Div(
    style={'backgroundColor': 'white', 'padding': '20px'},  # Ensuring a plain white background
    children=[
        html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),
        html.H5("Created by Mahde Abusaleh", style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

        # Navigation Bar
        html.Div([
            html.A('Exposure Sources | ', href='#exposure', style={'cursor': 'pointer', 'textDecoration': 'none'}),
            html.A('Dose-Response Models | ', href='#models', style={'cursor': 'pointer', 'textDecoration': 'none'}),
            html.A('Calculator | ', href='#calculator', style={'cursor': 'pointer', 'textDecoration': 'none'}),
            html.A('FAQ | ', href='#faq', style={'cursor': 'pointer', 'textDecoration': 'none'}),
            html.A('Conclusion', href='#conclusion', style={'cursor': 'pointer', 'textDecoration': 'none'})
        ], style={'textAlign': 'center', 'marginBottom': 20}),

        # Introduction Section
        html.Div(id='introduction', children=[
            html.H3("Introduction"),
            html.P("Radiation – the word sounds scary. But what is it really? Would it surprise you to know that you experience radiation every day?"),
            html.P("Radiation can be broadly defined as energy that travels in waves or particles. Radiation is typically broken down into two categories."),
            html.P("Non-Ionizing Radiation is low energy in nature, so it is generally safe. This type of radiation includes microwaves, radio waves, and visible light."),
            html.P("Ionizing Radiation has higher energy and can remove electrons from atoms. X-rays and gamma rays (and some UV rays) are examples."),
            html.P("Gamma Rays can come from sources like PET scans, solar flares, and natural radon gas in soil."),
            html.P("For the most part, even the ionizing radiation we experience on a daily basis is harmless. However, long-term exposure to these low dose sources can accumulate."),
        ]),

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
            html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels."),
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
            html.P("The LNT model assumes all radiation exposure carries some risk, while the Threshold model assumes there is a safe limit."),
            html.P("The Hormesis model suggests that low levels of radiation may be beneficial."),
        ]),

        # FAQ Section
        html.Div(id='faq', children=[
            html.H3("Frequently Asked Questions (FAQ)"),
            html.Details([
                html.Summary("What are Sv and mSv?"),
                html.P("Sv = Sievert, which is 1 Joule per kilogram. mSv = millisievert, which is 1/1000 of a Sv.")
            ]),
            html.Details([
                html.Summary("Is radiation from medical imaging safe?"),
                html.P("CT scans and X-rays use low doses of ionizing radiation. Below 10 mSv, there is no proven increase in cancer risk.")
            ]),
        ]),

        # References Section
        html.Div(id='references', children=[
            html.H3("References"),
            html.Ul([
                html.Li(html.A("Health Physics Society", href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
                html.Li(html.A("CDC - Radiation Facts", href="https://www.cdc.gov/radiation-health/", target="_blank")),
            ]),
        ]),

        # Conclusion Section
        html.Div(id='conclusion', children=[
            html.H3("Conclusion"),
            html.P("Understanding radiation exposure is essential for making informed health decisions."),
            html.P("Radiation is a part of everyday life, and responsible decision-making ensures safety."),
        ]),

        # Video Section
        html.Div(
            id="video",
            children=[
                html.H3("Radiation Exposure Explained - Video Resource"),
                html.Iframe(
                    src="https://www.youtube.com/embed/uzqsnxZBLNE",
                    width="700",
                    height="400",
                    style={"border": "none", "display": "block", "margin": "auto"}
                )
            ]
        )
    ]
)

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
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)

