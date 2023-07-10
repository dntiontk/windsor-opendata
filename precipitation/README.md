# windsor-opendata - precipitation

The provided dataset contains precipitation data collected from multiple gauges over a period of time. Each row represents a specific measurement instance, with the following columns: DateTime, Daily Accumulation, Rainfall Total, and Gauge.

**Daily Accumulation and Rainfall Total** are measured in *mm/hr*.

It is a cleaned and preprocessed version of the data available at the [City of Windsor's OpenData Catalogue](https://opendata.citywindsor.ca/). A raw copy of the datasets used can also be found in the [raw/precipitation](../raw/precipitation/) directory.

The script used to create this dataset is available at [scripts/clean-precipitation.py](../scripts/clean-precipitation.py)
