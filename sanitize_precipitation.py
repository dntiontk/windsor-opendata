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


base_path = "data/precipitation/"
gauges = {
    "ambassador": "01 Ambassador.csv",
    "cmh_woods": "02 CMH Woods.csv",
    "drouillard": "03 Drouillard.csv",
    "east_banwell": "04 East Banwell.csv",
    "grand_marais": "05 Grand Marais.csv",
    "howard_grade": "06 Howard Grade.csv",
    "huron_estates": "07 Huron Estates.csv",
    "lou_romano": "08 Lou Romano.csv",
    "pillette": "09 Pillette.csv",
    "pontiac": "10 Pontiac.csv",
    "provincial": "11 Provincial.csv",
    "twin_oaks": "12 Twin Oaks.csv",
    "wellington": "13 Wellington.csv",
}


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


for name, data in gauges.items():
    src = path.join(base_path, data)

    header = parse_header(src)
    dest_meta = path.join(base_path, "{}_metadata.txt".format(name))
    with open(dest_meta, "w") as f:
        f.write(header)

    dest_sanitized = path.join(base_path, "{}_sanitized.csv".format(name))

    df = remove_unnamed_columns(pd.read_csv(src, skiprows=2))
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
    df.set_index("DateTime", inplace=True)
    df.index = pd.DatetimeIndex(df.index)
    df.to_csv(dest_sanitized, header=True)
