import sys
import pandas as pd
from datetime import date
from os import path


def remove_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(
        ["Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6", "Unnamed: 7"],
        axis=1,
        errors="ignore",
    )

    return df.reset_index(drop=True)


def clean_string(str):
    out = str.split('",')[0]
    out = out.strip('"')
    out = out.split(",,")[0]
    return out


def parse_header(raw):
    with open(raw, "r") as f:
        head = [next(f) for _ in range(2)]
        location = clean_string(head[0])
        gauge = clean_string(head[1])
        timestamp = "Date: {}".format(date.today())
        return "{}\n{}\n{}".format(location, gauge, timestamp)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("not enough arguments")
    try:
        assert path.exists(sys.argv[1])
        src = path.split(sys.argv[1])
        basepath = src[0]
        filepath = src[1]
        df_src = path.join(basepath, filepath)
        header = parse_header(df_src)
        dest_meta = path.join(
            basepath, "{}_metadata.txt".format(filepath.split(".")[0])
        )
        with open(dest_meta, "w") as f:
            f.write(header)

        dest = path.join(basepath, "{}_sanitized.csv".format(filepath.split(".")[0]))
        df = remove_unnamed_columns(pd.read_csv(df_src, skiprows=2))
        df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
        df.set_index("DateTime", inplace=True)
        df.index = pd.DatetimeIndex(df.index)
        df.to_csv(dest, header=True)
    except Exception as err:
        exit(1)

# for name, data in gauges.items():
#    src = path.join(base_path, data)
#
#    header = parse_header(src)
#    dest_meta = path.join(base_path, "{}_metadata.txt".format(data))
#    with open(dest_meta, "w") as f:
#        f.write(header)
#
#    dest_sanitized = path.join(base_path, "{}_sanitized.csv".format(data))
#
#    df = remove_unnamed_columns(pd.read_csv(src, skiprows=2))
#    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
#    df.set_index("DateTime", inplace=True)
#    df.index = pd.DatetimeIndex(df.index)
#    df.to_csv(dest_sanitized, header=True)
#
