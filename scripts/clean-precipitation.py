#!/usr/bin/env python3

import argparse
from os import path, walk
import json
from base64 import b64encode
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    "--source",
    help="source directory of precipitation dataset",
    default="../data/precipitation",
)
parser.add_argument(
    "-d",
    "--destination",
    help="destination directory of processed precipitation datasets",
    default="./sanitized",
)

args = parser.parse_args()


def main():
    """
    Process precipitation datasets from CSV files.

    Reads CSV files from a source directory, performs data cleaning operations,
    combines the cleaned data into a single DataFrame, and writes it to a CSV file.

    """

    # get all the csv files in source directory
    raw_files = [
        path.join(d, x)
        for d, _, files in walk(args.source)
        for x in files
        if x.endswith(".csv")
    ]
    # collect dataframes and add the gauge name as a column
    df_list = collect_dataframes(raw_files)
    # concatenate dataframes
    combined = pd.concat(df_list, ignore_index=True)
    # set the index to 'DateTime'
    combined.set_index("DateTime", inplace=True)
    combined.sort_index(inplace=True)
    # write to file
    combined.to_csv(path.join(args.destination, "windsor-precipitation.csv"))


def collect_dataframes(files):
    dfs = []
    for f in files:
        gauge_name = extract_gauge(f)
        # read in the csv file
        df = pd.read_csv(
            f, skiprows=2, parse_dates=["DateTime"], date_format="%m/%d/%Y %H:%M"
        )
        df = drop_unnamed_columns(df)
        df["Gauge"] = gauge_name
        dfs.append(df)
    return dfs


def clean_header_whitespace(header: str) -> str:
    return header.split('",')[0].strip('"').split(",,")[0]


def extract_gauge(raw: str) -> str:
    with open(raw, "r") as f:
        head = [next(f) for _ in range(2)]
        return clean_header_whitespace(head[1]).split(":")[1].strip()


def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [x for x in df.columns.values if "Unnamed" in x]
    df = df.drop(cols, axis=1, errors="ignore")
    return df.reset_index(drop=True)


if __name__ == "__main__":
    main()
