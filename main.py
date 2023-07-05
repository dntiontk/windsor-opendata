from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import pandas as pd
import ssl


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(
        ["Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6", "Unnamed: 7"], axis=1
    )

    return df.reset_index(drop=True)


ssl._create_default_https_context = ssl._create_unverified_context

ambassador_url = "https://opendata.citywindsor.ca/Uploads/01%20Ambassador.csv"
ambassador_raw = clean_df(pd.read_csv(ambassador_url, skiprows=2))
ambassador_raw["DateTime"] = pd.to_datetime(
    ambassador_raw["DateTime"], format="%m/%d/%Y %H:%M"
)
ambassador_raw.set_index("DateTime", inplace=True)
ambassador_raw.index = pd.DatetimeIndex(ambassador_raw.index)
ambassador_df = ambassador_raw.resample("D").sum()

unique_years = ambassador_df.index.year.unique()
latest_year = unique_years[len(unique_years) - 1]

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Yearly Rainfall Data Windsor"),
        html.Div(children="Ambassador Gauge"),
        html.Hr(),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in unique_years],
            value=unique_years[len(unique_years) - 1],
            clearable=False,
        ),
        dcc.Graph(id="rainfall-plot"),
    ]
)


@callback(Output("rainfall-plot", "figure"), Input("year-dropdown", "value"))
def update_plot(selected_year):
    filtered_df = ambassador_df[ambassador_df.index.year == selected_year]
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
