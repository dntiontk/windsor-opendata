# windsor-opendata - precipitation

This directory contains a dashboard focused on visualizing precipitation data. The dashboard provides insights and analysis based on the available datasets.

## Usage

To utilize the Precipitation Dashboard, follow these steps:

1. Install python dependencies: `pip install -r requirements.txt`
2. Run the necessary data cleaning scripts and write files to a directory: `python clean.py -d sanitized`
3. Launch the dashboard `python app.py -d sanitized`
4. Explore the visualization at http://localhost:8050

## Data Cleaning Scripts
The `clean.py` script is specifically designed to clean and preprocess the precipitation datasets. This script ensures that the data used for visualization is accurate and properly formatted.

Please refer to the individual script files for detailed information on their usage and how they contribute to the data cleaning process.