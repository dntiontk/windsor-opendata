import pandas as pd
from datetime import date
from os import path, walk


base_path = "data/precipitation/"

df_list = []
sanitized = [f for _, _, files in walk(base_path) for f in files if "sanitized" in f]
for df_file in sanitized:
    name = df_file.split("_sanitized")[0]
    df = pd.read_csv(path.join(base_path, df_file))
    df["Gauge"] = name
    df_list.append(df)

combined = pd.concat(df_list)
combined.set_index("DateTime", inplace=True)
combined.index = pd.DatetimeIndex(combined.index)
combined = combined.sort_index()
combined.to_csv(path.join(base_path, "combined_precipitation.csv"))

# ambassador_path = "ambassador_sanitized.csv"
# df = pd.read_csv(path.join(base_path, ambassador_path))
# df.set_index("DateTime", inplace=True)
# df.index = pd.DatetimeIndex(df.index)
#
# unique_years = df.index.year.unique()
# year_opts = sorted(
#    [{"label": year, "value": year} for year in unique_years],
#    key=lambda x: x["label"],
# )
# opts = [{"label": "all", "value": "all"}] + year_opts
#
# app = Dash(__name__)
# app.layout = html.Div(
#    [
#        html.H1("Yearly Rainfall Data Windsor"),
#        html.Div(children="Ambassador Gauge"),
#        html.Hr(),
#        dcc.Dropdown(
#            id="year-dropdown",
#            options=opts,
#            value="all",
#            clearable=False,
#        ),
#        dcc.Graph(id="rainfall-plot"),
#    ]
# )
#
#
# @callback(Output("rainfall-plot", "figure"), Input("year-dropdown", "value"))
# def update_plot(selected_year):
#    if selected_year == "all":
#        filtered_df = df
#    else:
#        filtered_df = df[df.index.year == selected_year]
#
#    x_axis = filtered_df.index.strftime("%Y-%m-%d")
#    fig = go.Figure()
#    fig.add_trace(
#        go.Scatter(
#            x=x_axis,
#            y=filtered_df["Daily Accumulation"],
#            name="Daily Accumulation (mm/hr)",
#            mode="lines",
#        )
#    )
#    fig.add_trace(
#        go.Scatter(
#            x=x_axis,
#            y=filtered_df["Rainfall Total"],
#            name="Rainfall Total (mm/hr)",
#            mode="lines",
#        )
#    )
#
#    return fig
#
#
# if __name__ == "__main__":
#    app.run_server(debug=True)
#
# base_path = "data/precipitation/"
# gauges = {
#    "ambassador": "01 Ambassador.csv",
#    "cmh_woods": "02 CMH Woods.csv",
#    "drouillard": "03 Drouillard.csv",
#    "east_banwell": "04 East Banwell.csv",
#    "grand_marais": "05 Grand Marais.csv",
#    "howard_grade": "06 Howard Grade.csv",
#    "huron_estates": "07 Huron Estates.csv",
#    "lou_romano": "08 Lou Romano.csv",
#    "pillette": "09 Pillette.csv",
#    "pontiac": "10 Pontiac.csv",
#    "provincial": "11 Provincial.csv",
#    "twin_oaks": "12 Twin Oaks.csv",
#    "wellington": "13 Wellington.csv",
# }
#
#
# def clean_string(str):
#    out = str.split('",')[0]
#    out = out.strip('"')
#    out = out.split(",,")[0]
#    return out
#
#
# def parse_header(raw):
#    with open(raw, "r") as f:
#        head = [next(f) for _ in range(2)]
#        location = clean_string(head[0])
#        gauge = clean_string(head[1])
#        timestamp = "Date: {}".format(date.today())
#        return "{}\n{}\n{}".format(location, gauge, timestamp)
#
#
# for name, data in gauges.items():
#    src = path.join(base_path, data)
#
#    header = parse_header(src)
#    dest_meta = path.join(base_path, "{}_metadata.txt".format(name))
#    with open(dest_meta, "w") as f:
#        f.write(header)
#
#    dest_sanitized = path.join(base_path, "{}_sanitized.csv".format(name))
#
#    df = remove_unnamed_columns(pd.read_csv(src, skiprows=2))
#    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
#    df.set_index("DateTime", inplace=True)
#    df.index = pd.DatetimeIndex(df.index)
#    df.to_csv(dest_sanitized, header=True)
#
