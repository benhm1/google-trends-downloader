# Google Trends Data Downloader

Google Trends is pretty nifty! It tells you the relative popularity of
a search term over time.

One annoyance is that Google Trends will only show you daily data for
short time periods. If you want data over a longer time, Google Trends
aggregates the data into weeks or months, obscuring single-day peaks.

This project has two scripts designed to help you download daily data from
Google Trends over longer periods of time. 

The first script, `download_data.py`, downloads data in 75 day chunks:
a small enough range to get daily fidelity. The second script,
`normalize.py`, normalizes the downloaded data from all the chunks
onto the same scale, allowing comparisons across different chunks.

## Usage

### `download_data.py`

This script takes in arguments to specify the start date and query
string. An optional end date can be provided.

Downloaded CSV files are placed in a directory derived from the query
string.  If the directory already exists, the script will error
out. Rename the directory and rerun the script.

The downloaded CSVs are normalized, with the result being placed in
`normalized.csv` in the same directory.

```
# Download interest data for the string "hello world" from January 1, 2014 to present
python3 download_data.py --start_year=2014 --start_month=1 --start_day=1 --query="hello world"
#  --> Data will be written to data_hello_world/


# Download interest data for the string "cake" from January 1, 2014 - May 5, 2014
python3 download_data.py --start_year=2014 --start_month=1 --start_day=1 --end_year=2014 --end_month=5 --end_day=1 --query="cake"
#  --> Data will be written to data_cake/
```

### `normalize.py`

This script just does the normalization process. It allows you to
normalize data you've downloaded separately. The result is written
to `normalized.csv` in the input directory.

```
# Normalize data in data_hello_world/
python3 normalize.py data_cake
#  --> Creates data_hello_world/normalized.csv

# Normalize data in data_cake/
python3 normalize.py data_cake
#  --> Creates data_cake/normalized.csv
```

## Setup Instructions

You will need a working installation of Python 3, Firefox, and
geckodriver.

You will also need to install the packages specified in
`requirements.txt` with pip.

