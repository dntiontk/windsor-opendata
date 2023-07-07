from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import pandas as pd
from os import path


base_path = "data/precipitation/"
ambassador_path = "01 Ambassador_sanitized.csv"
df = pd.read_csv(path.join(base_path, ambassador_path))
df.set_index("DateTime", inplace=True)
df.index = pd.DatetimeIndex(df.index)

unique_years = df.index.year.unique()
year_opts = sorted(
    [{"label": year, "value": year} for year in unique_years],
    key=lambda x: x["label"],
)
opts = [{"label": "all", "value": "all"}] + year_opts

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Yearly Rainfall Data Windsor"),
        html.Div(children="Ambassador Gauge"),
        html.Hr(),
        dcc.Dropdown(
            id="year-dropdown",
            options=opts,
            value="all",
            clearable=False,
        ),
        dcc.Graph(id="rainfall-plot"),
    ]
)


@callback(Output("rainfall-plot", "figure"), Input("year-dropdown", "value"))
def update_plot(selected_year):
    if selected_year == "all":
        filtered_df = df
    else:
        filtered_df = df[df.index.year == selected_year]

    x_axis = filtered_df.index.strftime("%Y-%m-%d")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=filtered_df["Daily Accumulation"],
            name="Daily Accumulation (mm/hr)",
            mode="lines",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=filtered_df["Rainfall Total"],
            name="Rainfall Total (mm/hr)",
            mode="lines",
        )
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
