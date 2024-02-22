#!/usr/bin/env python3

import argparse
from os import path, walk
import pandas as pd
import re

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


lat_lon_pattern = r"^([-+]?\d+\.\d+), ([-+]?\d+\.\d+)$"


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
    combined.sort_values(by=["DateTime", "Gauge"], ascending=[True, True], inplace=True)
    # write to file
    combined.to_csv(path.join(args.destination, "windsor-precipitation.csv"))


def collect_dataframes(files):
    dfs = []
    for f in files:
        gauge_name = extract_gauge(f)
        location = extract_loc(f)
        if location in loc_map:
            location = loc_map[location]
        match = re.match(lat_lon_pattern, location)
        lat = float(match.group(1))
        lon = float(match.group(2))

        # read in the csv file
        df = pd.read_csv(
            f, skiprows=2, parse_dates=["DateTime"], date_format="%m/%d/%Y %H:%M"
        )
        df = drop_unnamed_columns(df)
        df["Gauge"] = gauge_name
        df["Lat"] = lat
        df["Lon"] = lon

        dfs.append(df)
    return dfs


loc_map = {
    "Riverside at Caron, Windsor, ON N9A 6W7": "42.317658, -83.048579",
    "290 Drouillard Rd": "42.314937, -83.036363",
    "3005 Grand Marais Rd E": "42.292000, -82.978780",
    "2355 Lambton St": "42.261649, -83.046723",
    "4155 Ojibway Pkwy": "42.282390, -83.082769",
    "1840 Provincial Rd": "42.256100, -82.970750",
}


def clean_header_whitespace(header: str) -> str:
    return header.split('",')[0].strip('"').split(",,")[0]


def extract_loc(raw: str) -> str:
    with open(raw, "r") as f:
        head = [next(f) for _ in range(2)]
        return clean_header_whitespace(head[0]).split(":")[1].strip()


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
