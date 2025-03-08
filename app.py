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
    html.H5("Created by Mahde Abusaleh", style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

    # Navigation Bar
    html.Div([
        html.A('Exposure Sources | ', href='#exposure'),
        html.A('Dose-Response Models | ', href='#models'),
        html.A('Calculator | ', href='#calculator'),
        html.A('FAQ | ', href='#faq'),
        html.A('Conclusion', href='#conclusion')
    ], style={'textAlign': 'center', 'marginBottom': 20}),

    # Radiation Exposure Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(
                    title="Radiation Dose Comparison (mSv)",
                    xaxis_title="Source",
                    yaxis_title="Dose (mSv)"
                )
            }
        ),
        html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels.")
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
        html.P("The Linear No-Threshold (LNT) model assumes all radiation exposure carries some risk, no matter how "
               "small, while the Threshold model assumes there is a dose below which there is no risk. "
               "The Hormesis model proposes that low levels of radiation may be beneficial."),
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
        html.Summary("What is radiation?"),
        html.P("Radiation is energy that travels through space in the form of waves or particles. It can be classified as ionizing or non-ionizing, depending on its ability to remove electrons from atoms.")
    ]),

    html.Details([
        html.Summary("What are the types of radiation?"),
        html.P("Radiation is categorized into two types: ionizing radiation, which has enough energy to ionize atoms (e.g., X-rays, gamma rays, alpha and beta particles), and non-ionizing radiation, which does not (e.g., radio waves, microwaves, visible light).")
    ]),

    html.Details([
        html.Summary("Where does radiation come from?"),
        html.P("Radiation comes from both natural and man-made sources. Natural sources include cosmic rays, radon gas, and radioactive elements in the earth. Man-made sources include medical imaging, nuclear power plants, and industrial applications.")
    ]),

    html.Details([
        html.Summary("What is background radiation?"),
        html.P("Background radiation refers to the natural radiation present in the environment. It comes from cosmic rays, the earth’s crust, and even food we consume. It is generally low and not harmful to humans.")
    ]),

    html.Details([
        html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
        html.P("Ionizing radiation has enough energy to remove electrons from atoms, potentially causing biological damage. Examples include X-rays and gamma rays. Non-ionizing radiation lacks sufficient energy to ionize atoms and includes radio waves and visible light.")
    ]),

    html.Details([
        html.Summary("What are the effects of radiation exposure on the human body?"),
        html.P("The effects of radiation exposure depend on the dose and duration. High doses can cause radiation sickness, while lower doses over time may increase the risk of cancer. Low doses, such as those from background radiation or medical imaging, generally have minimal effects.")
    ]),

    html.Details([
        html.Summary("How is radiation exposure measured?"),
        html.P("Radiation exposure is measured in units such as Sieverts (Sv) or millisieverts (mSv). These units quantify the biological effect of radiation on human tissue, taking into account the type and energy of radiation.")
    ]),
]),

# References Section
html.Div(id='references', children=[
    html.H3("References"),
    html.Ul([
        html.Li(html.A("Health Physics Society", href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
        html.Li(html.A("International Commission on Radiological Protection (ICRP)", href="https://www.icrp.org/page.asp?id=5", target="_blank")),
        html.Li(html.A("National Council on Radiation Protection and Measurements (NCRP)", href="https://ncrponline.org/", target="_blank")),
        html.Li(html.A("BEIR VII Reports", href="https://nap.nationalacademies.org/resource/11340/beir_vii_final.pdf", target="_blank")),
        html.Li(html.A("National Institutes of Health (NIH)", href="https://www.nih.gov/", target="_blank")),
        html.Li(html.A("United States Nuclear Regulatory Commission (U.S. NRC)", href="https://www.nrc.gov/", target="_blank")),
        html.Li(html.A("Centers for Disease Control and Prevention (CDC)", href="https://www.cdc.gov/", target="_blank")),
    ]),
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
    ]),

    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("Understanding radiation exposure and risk is important in making informed decisions about health and safety.")
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
