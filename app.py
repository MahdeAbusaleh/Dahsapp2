import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

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

# LNT Model (only)
dose_values = np.linspace(0, 100, 100)
lnt_risk = dose_values * 0.01

# Layout for the app
app.layout = html.Div([
    # Centering all content and setting a fixed max width
    html.Div([
        html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),
        html.H5("Created by Low Dose Radiation Explanation Group 1 2025", 
                style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

        # Navigation Bar
        html.Div([
            html.A('Exposure Sources | ', href='#exposure'),
            html.A('Dose-Response Models | ', href='#models'),
            html.A('Calculator | ', href='#calculator'),
            html.A('FAQ | ', href='#faq'),
            html.A('References | ', href='#references'),
            html.A('Conclusion', href='#conclusion')
        ], style={'textAlign': 'center', 'marginBottom': 20}),

        # Introduction Section
        html.Div(id='introduction', children=[
            html.H3("Introduction"),
            html.P("Radiation – the word sounds scary. But what is it really? Would it surprise you to know that you experience radiation every day?..."),
        ]),

        # Radiation Exposure Section
        html.Div(id='exposure', children=[
            html.H3("Radiation Exposure from Common Sources"),
            dcc.Graph(
                figure={
                    "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker=dict(color='blue'))],
                    "layout": go.Layout(
                        title="Radiation Dose Comparison (mSv)",
                        xaxis_title="Source",
                        yaxis_title="Dose (mSv)",
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(color="black"),
                        autosize=True,  # Makes the graph responsive
                    )
                }
            ),
            html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels.")
        ]),

    ], style={'maxWidth': '1200px', 'margin': 'auto', 'padding': '20px'}),  # ✅ Centers content

], style={'backgroundColor': 'white', 'minHeight': '100vh', 'padding': '30px'})  # ✅ Ensures full height

    # Dose-Response Models Section (Only LNT)
html.Div(
    id="models",
    children=[
        html.H3("Dose-Response Models: LNT"),
        dcc.Graph(
            figure={
                "data": [
                    go.Scatter(
                        x=dose_values,
                        y=lnt_risk,
                        mode="lines",
                        name="Linear No-Threshold (LNT)",
                        line=dict(color="red"),
                    )
                ],
                "layout": go.Layout(
                    title="Radiation Dose-Response Models",
                    xaxis_title="Radiation Dose (mSv)",
                    yaxis_title="Relative Risk",
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(color="black"),
                ),
            }
        ),
        html.P(
            "The Linear No-Threshold (LNT) model assumes all radiation exposure carries some risk, no matter how small."
        ),
    ],
),

# Calculator Section
html.Div(
    id="calculator",
    children=[
        html.H3("Personal Radiation Exposure Calculator"),
        html.Label("Number of flights per year (NYC to LA equivalent):"),
        dcc.Slider(
            0, 50, 1, 
            value=5, 
            marks={i: str(i) for i in range(0, 51, 10)}, 
            id="flight-slider"
        ),
        html.Label("Number of chest X-rays per year:"),
        dcc.Slider(
            0, 10, 1, 
            value=1, 
            marks={i: str(i) for i in range(0, 11)}, 
            id="xray-slider"
        ),
        html.Div(
            id="total-dose-output", 
            style={"fontSize": 20, "marginTop": 20}
        ),
    ],
),
# FAQ Section
html.Div(id='faq', children=[
    html.H3("Frequently Asked Questions (FAQ)"),

    html.Details([
        html.Summary("What are Sv and mSv?"),
        html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international system unit for dose equivalent. "
               "mSv = millisievert, which is 1/1000 of a Sv."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/sievert-sv.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is background radiation? Is it harmful to me?"),
        html.P("Background radiation is natural radiation that is always present and all around us in the environment. "
               "It includes cosmic radiation (from the sun and stars), terrestrial radiation (from the Earth), "
               "and internal radiation (from all living things)."),
        html.P("Background radiation is NOT harmful at normal exposure levels."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/background-radiation.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("How does radiation affect air travel?"),
        html.P("Radiation from flying is due to cosmic radiation. If you were to travel from the East Coast to the West Coast, "
               "you would receive 0.035 mSv from the flight."),
        html.P("The longer the flight duration, the more radiation you receive."),
        html.P("The higher the altitude, the higher the dose of radiation."),
        html.P("The further north or south from the equator you fly, the more radiation you will receive."),
        html.P("Overall, air travel results in very low radiation levels."),
        html.P(["Source: CDC Facts About Radiation from Air Travel. ", 
                html.A("Learn more", href="https://www.cdc.gov/radiation-health/data-research/facts-stats/air-travel.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("Is radiation from medical imaging safe?"),
        html.P("Medical imaging, such as CT scans and X-rays, delivers beams in the form of ionizing radiation to a specific part of the body "
               "to visualize internal structures."),
        html.P("Although these involve low radiation doses, the benefits outweigh the potential risks. "
               "These procedures are accomplished in a controlled environment by a professional."),
        html.P("Below 10 mSv, which is a dose rate relevant to radiography, nuclear medicine, and CT scans, "
               "there is no data to support an increase in cancer risk."),
        html.P(["(1) Source: CDC - Radiation in Healthcare: Imaging Procedures. ",
                html.A("Learn more", href="https://www.cdc.gov/radiation-health/features/imaging-procedures.html", target="_blank")]),
        html.P(["(2) Source: National Library of Medicine - Radiation Risk from Medical Imaging. ",
                html.A("Learn more", href="https://www.ncbi.nlm.nih.gov/articles/PMC2996147/#T1", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
        html.P("Ionizing radiation includes alpha & beta particles, gamma rays, X-rays, neutrons, and high-speed protons. "
               "These particles are capable of producing ions that can potentially damage cells and are considered more energetic than non-ionizing radiation."),
        html.P("Non-ionizing radiation includes radio waves, microwaves, and visible/infrared/UV light. These do not have the ability to produce ions."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/ionizing-radiation.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is radiation hormesis?"),
        html.P("Radiation hormesis is the hypothesis that low doses of ionizing radiation may be beneficial by stimulating physiological performance, "
               "immune competence, and overall health. Although this is a controversial topic in health physics, some studies suggest "
               "that small doses of radiation may increase lifespan."),
        html.P(["Source: Luckey TD. Radiation Hormesis Study. ", 
                html.A("Learn more", href="https://doi.org/10.2203/dose-response.06-102.Luckey", target="_blank")])
    ]),

    html.Details([
        html.Summary("Does radiation exposure always cause cancer?"),
        html.P("No. While high doses and dose rates may cause cancer, there is no public health data that shows an increased occurrence of cancer "
               "due to low radiation doses and low dose rates."),
        html.P(["Source: U.S. NRC - Radiation Exposure and Cancer. ", 
                html.A("Learn more", href="https://www.nrc.gov/about-nrc/radiation/health-effects/rad-exposure-cancer.html", target="_blank")])
    ])
])  # ✅ Ensures the `faq` section is properly closed

        # References Section
        html.Div(id='references', children=[
            html.H3("References"),
            html.Ul([
                html.Li(html.A("Health Physics Society", href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
                html.Li(html.A("International Commission on Radiological Protection (ICRP)", href="https://www.icrp.org/page.asp?id=5", target="_blank")),
            ]),
        ]),

        # Conclusion Section
        html.Div(id='conclusion', children=[
            html.H3("Conclusion"),
            html.P("Understanding radiation exposure and risk is important in making informed decisions about health and safety...")
        ]),

        # Video Section
        html.Div(id='video', children=[
            html.H3("Radiation Exposure Explained - Video Resource"),
            html.Iframe(
                src="https://www.youtube.com/embed/uzqsnxZBLNE",
                width="700",
                height="400",
                style={"border": "none", "display": "block", "margin": "auto"}
            )
        ]),

    ], style={'width': '100%', 'padding': '40px', 'backgroundColor': 'white', 'color': 'black'})  

], style={'width': '100%', 'minHeight': '100vh', 'backgroundColor': 'white', 'color': 'black'})

