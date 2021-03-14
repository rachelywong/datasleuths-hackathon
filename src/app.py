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

# make sure the correct name is listed for business
df_no_nan = reader.dropna(subset=["BusinessName"])
# business_trade_names = list(
#     df_no_nan[df_no_nan["BusinessName"].str.contains("(", regex=False)][
#         "BusinessTradeName"
#     ].unique()
# )
# reg_business_names = list(
#     set(df_no_nan["BusinessName"].unique())
#     - set(df_no_nan[df_no_nan["BusinessName"].str.contains("(", regex=False)])
# )
# all_names = business_trade_names + reg_business_names
# all_names_nan = [name for name in all_names if str(name) != "nan"]


# cities for each province dictionary
province_city_dict = {}
for province in list(reader["Province"].dropna().unique()):
    province_city_dict[province] = (
        reader[reader["Province"] == province]["City"].dropna().unique().tolist()
    )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

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
                        html.Label(
                            [
                                "Filter by Province:",
                                dcc.Dropdown(
                                    id="name-dropdown",
                                    value=list(province_city_dict.keys())[0],
                                    # multi=True,
                                    clearable=False,
                                    style=css_dd,
                                    options=[
                                        {"label": province, "value": province}
                                        for province in list(province_city_dict.keys())
                                    ],
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Label("Filter by City: "),
                        dcc.Dropdown(id="opt-dropdown", style=css_dd),
                        html.Br(),
                        html.Label("OR"),
                        html.Br(),
                        html.Br(),
                        html.Label("Filter by Business Name: "),
                        dcc.Dropdown(
                            id="input_name",
                            value="Golden Trim Enterprises Inc",
                            multi=False,
                            style=css_dd,
                            options=[
                                {"label": name, "value": name}
                                for name in df_no_nan.BusinessName.tolist()
                            ],
                        ),
                        html.Br(),
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
                    style={
                        "border-radius": "0px",
                        "background-color": "rgba(173, 216, 230, 0.5)",
                    },
                    md=4,
                ),
                html.Br(),
                dbc.Col(
                    [
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label="Tab1",
                                    children=[
                                        html.Iframe(
                                            id="issue_plot",
                                            style={
                                                "border-width": "0",
                                                "width": "100%",
                                                "height": "400px",
                                            },
                                        )
                                    ],
                                ),
                                dcc.Tab(
                                    label="Tab2",
                                    children=[
                                        dcc.Graph(
                                            figure={
                                                "data": [
                                                    {
                                                        "x": [1, 2, 3],
                                                        "y": [4, 1, 2],
                                                        "type": "bar",
                                                        "name": "SF",
                                                    },
                                                    {
                                                        "x": [1, 2, 3],
                                                        "y": [2, 4, 5],
                                                        "type": "bar",
                                                        "name": "Montreal",
                                                    },
                                                ]
                                            }
                                        )
                                    ],
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
    ],
)


@app.callback(
    dash.dependencies.Output("opt-dropdown", "options"),
    [dash.dependencies.Input("name-dropdown", "value")],
)
def update_city_dropdown(province):
    return [{"label": i, "value": i} for i in province_city_dict[province]]


# def plot_altair(business=None):

#     dat = df_no_nan[(df_no_nan["BusinessName"] == business)].dropna()

#     base = alt.Chart(dat).encode(
#         alt.X("LicenceNumber:N", axis=alt.Axis(title=None)), tooltip="BusinessName"
#     )

#     area = base.mark_circle(size=100, opacity=0.5, color="#57A44C").encode(
#         alt.Y("IssuedDate", axis=alt.Axis(title="Issued Date", titleColor="#57A44C")),
#         alt.Y2("IssuedDate"),
#     )

#     line = base.mark_line(stroke="#5276A7", interpolate="monotone").encode(
#         alt.Y("ExpiredDate", axis=alt.Axis(title="Expired Date", titleColor="#5276A7"))
#     )

#     chart = alt.layer(area, line).resolve_scale(y="independent")

#     return chart.to_html()
@app.callback(
    dash.dependencies.Output("issue_plot", "srcDoc"),
    dash.dependencies.Input("input_name", "value"),
)
def plot_barchat(business=None):
    df = df_no_nan
    df[‘IssuedDate’] = df[‘IssuedDate’].str[0:10]

    dat = df[(df["BusinessName"] == business)].dropna()

    dat["IssuedDate"] = pd.to_datetime(dat["IssuedDate"], format="%Y-%m-%d")
    dat["ExpiredDate"] = pd.to_datetime(dat["ExpiredDate"])
    dat["DaysActive"] = dat["ExpiredDate"] - dat["IssuedDate"]
    dat["DaysActive"] = dat["DaysActive"].dt.days
    dat["DaysActive"] = dat["DaysActive"].astype(int)

    chart = (
        alt.Chart(dat)
        .mark_bar()
        .encode(
            alt.X(
                "FOLDERYEAR:N", axis=alt.Axis(title="Year (2000s)", titleColor="black")
            ),
            alt.Y("DaysActive", axis=alt.Axis(title="Days Active", titleColor="black")),
            tooltip=["BusinessName", "IssuedDate", "ExpiredDate", "NumberofEmployees"],
        )
    )

    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)