#!/usr/bin/env python3

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from os import path
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-d",
    "--data",
    help="path to input data",
    default="./sanitized/windsor-precipitation.csv",
)

args = parser.parse_args()


def get_first_and_last_year(df):
    df["DateTime"] = pd.DatetimeIndex(df["DateTime"])
    return df["DateTime"].dt.year.min(), df["DateTime"].dt.year.max()


df = pd.read_csv(args.data)
options = df["Gauge"].unique()
first, last = get_first_and_last_year(df)
theme = "plotly_dark"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div(
    [
        html.H4("Windsor precipitation ({}-{})".format(first, last)),
        html.Div(
            [
                html.P("Precipitation per gauge"),
                dcc.Graph(
                    id="total",
                    figure=px.line(
                        df,
                        x="DateTime",
                        y="Rainfall Total",
                        labels={"Rainfall Total": "mm/hr"},
                        color="Gauge",
                        template=theme,
                        title="Rainfall Total",
                    ),
                ),
                html.Hr(),
                dcc.Graph(
                    id="daily",
                    figure=px.line(
                        df,
                        x="DateTime",
                        y="Daily Accumulation",
                        labels={"Daily Accumulation": "mm/hr"},
                        color="Gauge",
                        template=theme,
                        title="Daily Accumulation",
                    ),
                ),
            ]
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
