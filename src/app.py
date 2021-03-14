# Load modules
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px

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

# data wrangling for map 
df_no_nans = df_no_nan.dropna()
df_geom = pd.DataFrame(df_no_nans["Geom"])
df_geom

long_list = []
lat_list = []
long_list_clean = []
lat_list_clean = []

for value in df_geom["Geom"]: 
    if type(value) is str:
        long = value[34:-20]
        lat = value[53:-2]
        long_list.append(long)
        lat_list.append(lat)
        long_list_clean.append(long)
        lat_list_clean.append(lat)
    else:
        long_list.append("NaN")
        lat_list.append("NaN")

df_coordinates = df_no_nans.copy()

df_coordinates["longitude"] = long_list
df_coordinates["latitude"] = lat_list

def map_maker():
    fig = px.scatter_geo(df_coordinates, lat = "latitude", lon = "longitude", scope="north america",
                    #lataxis = [40,70],
                    #lonaxis = [-130,-55],
                     color="LocalArea", # which column to use to set the color of markers
                     hover_name="BusinessName", # column added to hover information
                     size="NumberofEmployees", # size of markers
                     projection="natural earth")

#fig.update_geos(fitbounds="locations")


    fig.update_layout(
        title_text = 'Map',
        geo = dict(
            resolution = 50,
            showland = True,
            showlakes = True,
            landcolor = 'rgb(204, 204, 204)',
            countrycolor = 'rgb(204, 204, 204)',
            lakecolor = 'rgb(255, 255, 255)',
            projection_type = "equirectangular",
            coastlinewidth = 2,
            #lataxis = dict(
            #    range = [48,50],
                #showgrid = True,
                #dtick = 10
            #),
            #lonaxis = dict(
            #    range = [-122,-124],
                #showgrid = True,
                #dtick = 20
            #),
        ))

    return fig

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
        html.H1("Business Tracker"),
        html.P(
            dcc.Markdown(
                """
                This business tracker tracks businesses across Canada!
                """
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Label("To Filter the Review Table Tab, use:", style={"font-weight":"bold"}),
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
                        dcc.Dropdown(id="opt-dropdown", value="Vancouver", style=css_dd),
                        html.Br(),
                        html.Br(),
                        html.Label("To Filter the Visuals, Use:",style={"font-weight":"bold"}),
                        html.Br(),
                        html.Label("Filter by Business Name: "),
                        dcc.Dropdown(
                            id="input_name",
                            value='Tamton Networking Inc',
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
                                    label="License Number Records",
                                    children=[
                                        html.Iframe(
                                            id="issue_plot",
                                            srcDoc=None,
                                            style={
                                                "border-width": "0",
                                                "width": "100%",
                                                "height": "400px",
                                            },
                                        )
                                    ],
                                ),
                                dcc.Tab(
                                    label="License Activity",
                                    children=[
                                        html.Iframe(
                                            id="bar_plot",
                                            srcDoc=None,
                                            style={
                                                "border-width": "0",
                                                "width": "100%",
                                                "height": "400px",
                                            },
                                        )
                                        
                                    ],
                                ),
                                dcc.Tab(
                                    label="Employee Count",
                                    children=[
                                        html.Iframe(
                                            id="employee_plot",
                                            srcDoc=None,
                                            style={
                                                "border-width": "0",
                                                "width": "100%",
                                                "height": "400px",
                                            },
                                        )
                                        
                                    ],
                                ),
                                dcc.Tab(
                                    label="Review Table",
                                    children=[
                                        dash_table.DataTable(id = 'table', page_size=8),
                                        dcc.Dropdown(
                                            id='dropdown',
                                            options=[{"label": col, "value": col} for col in reader.columns],
                                            multi=True,
                                            value=["BusinessType"]

                                        )
                                        
                                    ],
                                ),
                                dcc.Tab(
                                    label="Map",
                                    children=[
                                        dcc.Graph(
                                            figure=map_maker()
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

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('dropdown', 'value'),
    Input('name-dropdown', 'value'),
    Input('opt-dropdown', 'value'))
def update_table(cols, province, city):
    columns=[{"name": col, "id": col} for col in cols]
    filtered_df = reader[(reader['Province'] == province) & (reader['City'] == city)]
    data=filtered_df[cols].to_dict('records')
    return data, columns

@app.callback(
    dash.dependencies.Output("issue_plot", "srcDoc"),
    dash.dependencies.Input("input_name", "value"),
)
def plot_altair(business=None):
    df = df_no_nan.copy()
    df['IssuedDate'] = df['IssuedDate'].str[0:10]
    
    dat = df[(df['BusinessName'] == business)]
    dat = dat[["BusinessName", "ExpiredDate", "IssuedDate", "LicenceNumber"]]
    dat = dat.dropna()

    base = alt.Chart(dat).encode(
        alt.X("LicenceNumber:N", axis=alt.Axis(title="License Number")), tooltip="BusinessName"
    )

    area = base.mark_circle(size=100, opacity=0.5, color="#57A44C").encode(
        alt.Y("IssuedDate", axis=alt.Axis(title="Issued Date", titleColor="#57A44C")),
        alt.Y2("IssuedDate"),
    )

    line = base.mark_line(stroke="#5276A7", interpolate="monotone").encode(
        alt.Y("ExpiredDate", axis=alt.Axis(title="Expired Date", titleColor="#5276A7"))
    )

    chart = alt.layer(area, line).resolve_scale(y="independent").properties(width=200, height =300)

    return chart.to_html()

@app.callback(
    dash.dependencies.Output("bar_plot", "srcDoc"),
    dash.dependencies.Input("input_name", "value"),
)
def plot_barchat(business=None):

    df = df_no_nan.copy()
    df['IssuedDate'] = df['IssuedDate'].str[0:10]

    dat = df[(df['BusinessName'] == business)]
    dat = dat[["BusinessName", "ExpiredDate", "IssuedDate", "FOLDERYEAR", "NumberofEmployees"]]
    dat = dat.dropna()

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
        ).properties(width=200, height =300)
    )

    return chart.to_html()

@app.callback(
    dash.dependencies.Output("employee_plot", "srcDoc"),
    dash.dependencies.Input("input_name", "value"),
)
def graph_EmployeeNumber(company_name=None):
    max_size = reader[reader['BusinessName']==company_name]['NumberofEmployees'].max()
    company_name_list = reader[reader['BusinessName'] == company_name]
    chart = alt.Chart(company_name_list, title = company_name).mark_point().encode(
    y=alt.Y('NumberofEmployees', axis=alt.Axis(title = 'Number of Employees'), scale=alt.Scale(domain=(0,round(1.5*max_size, 0)))),
    x=alt.X('FOLDERYEAR', axis=alt.Axis(title = 'Folder year'), scale=alt.Scale(domain=(13, 21))),
    color = "Status"
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)