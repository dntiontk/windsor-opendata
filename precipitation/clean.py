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
    # instantiate data frame list
    df_list = []
    # get all the csv files in source directory
    raw_files = [f for _, _, files in walk(args.source) for f in files if ".csv" in f]
    # for each file in source
    for f in raw_files:
        src_file = path.join(args.source, f)
        print("processing {}".format(src_file))
        # extract metadata from csv as base64 encoded string
        meta = extract_meta(src_file)
        # read in the csv file
        df = pd.read_csv(src_file, skiprows=2)
        # drop unnamed columns
        df = drop_unnamed_columns(df)
        # convert index to datetime
        df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
        df.set_index("DateTime", inplace=True)
        df.index = pd.DatetimeIndex(df.index)
        # add column for location based on metadata
        df["Gauge Metadata"] = meta
        # add to dataframe list
        df_list.append(df)

    # combine dataframes
    print("combining {} dataframes".format(len(df_list)))
    df = pd.concat(df_list)
    # sort data
    df.sort_index(inplace=True)
    # write to file
    df.to_csv(path.join(args.destination, "windsor-precipitation.csv"))


def clean_header_whitespace(header: str) -> str:
    return header.split('",')[0].strip('"').split(",,")[0]


def extract_meta(raw: str) -> str:
    with open(raw, "r") as f:
        head = [next(f) for _ in range(2)]
        location = clean_header_whitespace(head[0]).split(":")[1].strip()
        gauge = clean_header_whitespace(head[1]).split(":")[1].strip()
        meta = json.dumps({"location": location, "gauge": gauge})
        return b64encode(meta.encode("utf-8")).decode("utf-8")


def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [x for x in df.columns.values if "Unnamed" in x]
    df = df.drop(cols, axis=1, errors="ignore")
    return df.reset_index(drop=True)


if __name__ == "__main__":
    main()
