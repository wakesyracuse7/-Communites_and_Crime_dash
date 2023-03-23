# load library
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data
df = pd.read_csv("data/processed_communities.csv")

# Select only columns with numerical values
column_list = {"latitude": "Latitude",
               "longitude": "Longitude",
               "population": "Population",
               "PopDens": "Population Density",
               "racepctblack": "Black Race Percentage",
               "racePctWhite": "White Race Percentage",
               "racePctAsian": "Asian Race Percentage",
               "agePct12t29": "Age Percentage (12-29)",
               "agePct65up": "Age Percentage (65+)",
               "medIncome": "Median Income",
               "violent_crime_rate": "Violent Crime Rate",
               "NumStreet": "Number of Streets",
               "PctUnemployed": "Unemployed Percentage"
               }
df = df[column_list]

# rename colunms
df = df.rename(columns = column_list)

# Define app and layout
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Explore Crime Rate With Different Factors"),
                        dcc.Dropdown(
                            id = "scatter-x",
                            options = [{"label": colname, "value": colname} for colname in df.columns],
                            value = "Population"
                        ),
                        dcc.Dropdown(
                            id = "scatter-y",
                            options = [{"label": colname, "value": colname} for colname in df.columns],
                            value = "Violent Crime Rate"
                        ),
                        dcc.Graph(id = "scatter-plot")
                    ],
                    md = 6,
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "correlation-column",
                            options = [{"label": colname, "value": colname} for colname in df.columns],
                            value = "Population"
                        ),
                        html.Table(id = "correlation-table")
                    ],
                    md = 6,
                ),
            ]
        )
    ],
    fluid = True,
)

# Define callbacks
@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"),
    [dash.dependencies.Input("scatter-x", "value"),
     dash.dependencies.Input("scatter-y", "value")]
)

# Scatter plot
def update_scatter_plot(xcol, ycol):
    fig = px.scatter(df, x = xcol, y = ycol)
    return fig

@app.callback(
    dash.dependencies.Output("correlation-table", "children"),
    [dash.dependencies.Input("correlation-column", "value")]
)

# Correlation table
def update_correlation_table(col):
    corr_df = df.corr()[col].reset_index()
    corr_df.columns = ["Column", "Correlation"]
    corr_df = corr_df.round(3)
    corr_table = [html.Tr([html.Th("Column"), html.Th("Correlation")])]
    for i in range(len(corr_df)):
        corr_table.append(html.Tr([
            html.Td(corr_df.iloc[i]["Column"]),
            html.Td(corr_df.iloc[i]["Correlation"])
        ]))
    return corr_table

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)