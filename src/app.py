# Load modules
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

# disable Altair limits
alt.data_transformers.disable_max_rows()

# read-in data
business_licences = "business-licences-hackathon.csv"
file = open(business_licences, "r")
reader = pd.read_csv(file, sep=";")


app = dash.Dash(__name__)

# app.layout = html.Div("I am alive!!")

# CSS Styles
css_dd = {
    "font-size": "smaller",
}

css_sources = {
    "font-size": "xx-small",
}

app.layout = dbc.Container(
    [
        html.H1("Business Tracker Dashboard"),
        html.P(
            dcc.Markdown(
                """
                This business tracker allow us to track business across Canada!
                """
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Label("Filter Business Type: "),
                        dcc.RadioItems(
                            id="input_statusß",
                            options=[
                                {"label": stat, "value": stat}
                                for stat in list(reader["Status"].unique())
                            ],
                            value="Issued",
                            style=css_dd,
                            labelStyle={"display": "inline-block"},
                            inputStyle={"margin-left": "20px"},
                        ),
                        html.Br(),
                        # html.Label("Filter Year: "),
                        # dcc.Slider(
                        #     id="input_year",
                        #     value=2016,
                        #     min=1975,
                        #     max=2016,
                        #     step=1,
                        #     included=False,
                        #     marks={i: f"{str(i)}" for i in range(1975, 2017, 5)},
                        # ),
                        # html.Br(),
                        html.Label(
                            [
                                "Filter City:",
                                dcc.Dropdown(
                                    id="input_city",
                                    value=reader["City"].dropna().unique().tolist(),
                                    # multi=True,
                                    clearable=False,
                                    style=css_dd,
                                    options=[
                                        {"label": city, "value": city}
                                        for city in list(
                                            reader["City"].dropna().unique()
                                        )
                                    ],
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Label("Filter Province: "),
                        dcc.Dropdown(
                            id="input_province",
                            value=reader["Province"].dropna().unique().tolist(),
                            multi=False,
                            clearable=False,
                            style=css_dd,
                            options=[
                                {"label": province, "value": province}
                                for province in reader["Province"]
                                .dropna()
                                .unique()
                                .tolist()
                            ],
                        ),
                        html.Br(),
                        html.Label("Filter Business Name: "),
                        dcc.Dropdown(
                            id="input_name",
                            value="Golden Trim Enterprises Inc",
                            multi=True,
                            style=css_dd,
                            options=[
                                {"label": name, "value": name}
                                for name in reader["BusinessName"]
                                .dropna()
                                .unique()
                                .tolist()
                            ],
                        ),
                        html.Br(),
                        # html.Label("Select Year Range: "),
                        # dcc.RangeSlider(
                        #     id="input_year_range",
                        #     value=[1975, 2016],
                        #     min=1975,
                        #     max=2016,
                        #     step=1,
                        #     marks={
                        #         i: "{}".format(i) if i == 1 else str(i)
                        #         for i in range(1975, 2017, 5)
                        #     },
                        # ),
                        html.Hr(),
                        html.P(
                            dcc.Markdown(
                                """
                                This dashboard is created by Data Sleuths. View the source code and contribute [here](https://github.com/jraza19/datasleuths-hackathon).
                                """
                            ),
                            style=css_sources,
                        ),
                    ],
                    md=4,
                    style={
                        "border": "1px solid #d3d3d3",
                        "border-radius": "10px",
                        "background-color": "rgba(173, 216, 230, 0.5)",
                    },
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Iframe(
                                    id="combo_plot",
                                    srcDoc=None,
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "1250px",
                                    },
                                ),
                            ],
                        )
                    ]
                ),
            ],
        ),
        html.Br(),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)