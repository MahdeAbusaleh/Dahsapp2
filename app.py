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

# Navigation Bar (Updated to use html.A() for smooth scrolling)
html.Div([
    html.A('Exposure Sources | ', href='#exposure', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Dose-Response Models | ', href='#models', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Calculator | ', href='#calculator', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('FAQ | ', href='#faq', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Conclusion', href='#conclusion', style={'cursor': 'pointer', 'textDecoration': 'none'})
], style={'textAlign': 'center', 'marginBottom': 20}),

# JavaScript for smooth scrolling
dcc.Markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
            });
        });
    });
    </script>
""", dangerously_allow_html=True),

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
        html.P("The chart above compares radiation doses from common sources, providing insight into "
               "relative exposure levels."),
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
        html.Summary("What are Sv and mSv?"),
        html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international unit for dose equivalent. "
               "mSv = millisievert, which is 1/1000 of a Sv.")
    ]),

    html.Details([
        html.Summary("What is background radiation? Is it harmful to me?"),
        html.P("Background radiation is natural radiation always present in the environment. "
               "It includes cosmic radiation (from the sun and stars), terrestrial radiation (from the Earth), "
               "and internal radiation (from all living things). Background radiation is NOT harmful at normal exposure levels.")
    ]),

    html.Details([
        html.Summary("How does radiation affect air travel?"),
        html.P("Radiation from flying is due to cosmic radiation. A flight from the East Coast to the West Coast "
               "results in about 0.035 mSv of exposure. Higher altitudes, longer flight durations, and flights "
               "closer to the poles result in more exposure. However, overall, air travel results in very low radiation levels.")
    ]),

    html.Details([
        html.Summary("Is radiation from medical imaging safe?"),
        html.P("Medical imaging, such as CT scans and X-rays, delivers ionizing radiation to a specific part of the body "
               "to visualize internal structures. Though these involve low radiation doses, the benefits generally outweigh "
               "the risks. Below 10 mSv (relevant to medical imaging), there is no data supporting an increase in cancer risk.")
    ]),

    html.Details([
        html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
        html.P("Ionizing radiation (e.g., alpha & beta particles, gamma rays, X-rays, neutrons) can ionize atoms and potentially "
               "damage cells. Non-ionizing radiation (e.g., radio waves, microwaves, visible/infrared/UV light) does not have enough "
               "energy to ionize atoms and is generally considered safer.")
    ]),

    html.Details([
        html.Summary("What is radiation hormesis?"),
        html.P("Radiation hormesis is the hypothesis that low doses of ionizing radiation may have beneficial effects, such as "
               "stimulating immune responses and increasing mean lifespan. This remains a debated topic in radiation safety.")
    ]),

    html.Details([
        html.Summary("Does radiation exposure always cause cancer?"),
        html.P("No. While high doses of radiation may increase cancer risk, public health data does not show increased cancer occurrence "
               "at low radiation doses and low dose rates.")
    ]),

    html.Details([
        html.Summary("Where can I find reliable information on radiation?"),
        html.P("Reliable sources include:"),
        html.Ul([
            html.Li("Health Physics Society"),
            html.Li("International Commission on Radiological Protection (ICRP)"),
            html.Li("National Council on Radiation Protection and Measurements (NCRP)"),
            html.Li("BEIR VII Reports"),
            html.Li("National Institutes of Health (NIH)"),
            html.Li("United States Nuclear Regulatory Commission (U.S. NRC)"),
            html.Li("Centers for Disease Control and Prevention (CDC)")
        ])
    ])
]),

# References Section
html.Div(id='references', children=[
    html.H3("References"),
    html.Ul([
        html.Li([
            "BEIR VII Report (Biological Effects of Ionizing Radiation): ",
            html.A("Learn more", href="https://nap.nationalacademies.org/resource/11340/beir_vii_final.pdf", target="_blank")
        ]),
        html.Li([
            "Health Physics Society Fact Sheets: ",
            html.A("Learn more", href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")
        ]),
        html.Li([
            "International Commission on Radiological Protection (ICRP): ",
            html.A("Learn more", href="https://www.icrp.org/page.asp?id=5", target="_blank")
        ]),
        html.Li([
            "National Council on Radiation Protection and Measurements (NCRP): ",
            html.A("Learn more", href="https://ncrponline.org/", target="_blank")
        ]),
        html.Li([
            "Centers for Disease Control and Prevention (CDC) - Radiation Information: ",
            html.A("Learn more", href="https://www.cdc.gov/", target="_blank")
        ]),
        html.Li([
            "U.S. Nuclear Regulatory Commission (NRC): ",
            html.A("Learn more", href="https://www.nrc.gov/", target="_blank")
        ]),
        html.Li([
            "National Institutes of Health (NIH): ",
            html.A("Learn more", href="https://www.nih.gov/", target="_blank")
        ]),
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
    html.P("This video provides a clear explanation of radiation exposure, different sources of radiation, and its effects on health."),
]),



    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("Understanding radiation exposure and risk is important in making informed decisions about health and safety. While radiation often has a bad stigma attached to it, as being associated with danger, it is also an essential part of modern life, from medical diagnostics to energy production. By breaking down exposure sources, dose response models, and personal risk factors, this website aims to provide clarity on this complex subject, helping users navigate the balance between precaution and practicality.
Different models of radiation risk such as the Linear No-Threshold (LNT), Threshold and Hormesis reflect the ongoing debate among scientists and regulators. The LNT model assumes all exposure carries some risk, while the Threshold model suggests a safe limit, and the Hormesis model argues that low doses may even be beneficial. These perspectives influence safety standards and policies, affecting everything from occupational exposure limits to space exploration guidelines. By understanding these models, individuals can make informed decisions regarding radiation related risks and make informed choices based on scientific evidence rather than fear.
In conclusion, radiation is a part of everyday life, and complete avoidance is neither necessary nor possible. Instead, the key is risk awareness and responsible decision making. Whether considering medical procedures, occupational hazards, or lifestyle choices, having a solid understanding of radiation principles allows individuals to take the correct precautions without unnecessary anxiety. This site serves as a foundation for further exploration and encourages users to continue learning about radiation safety from reliable sources.
."),
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
