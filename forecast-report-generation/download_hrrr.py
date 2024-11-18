#!/usr/bin/env python3

"""
Script to download data from the HRRR (High-Resolution Rapid Refresh) archive.

This script downloads HRRR analysis files for a specified range of dates, forecast hours, 
and dataset types. The downloaded files are saved to a specified local directory.

Usage:
    python download_hrrr.py

Example:
    Modify the START OPTIONS section of the script to set the date range, forecast hours, 
    and other parameters before running.
"""

from datetime import datetime, timedelta
import urllib.request as ureq
import os

##### START OPTIONS #####

# Start date for downloading HRRR data (format: YYYYMMDD-HH)
start_date = "20180101-01"

# End date for downloading HRRR data (format: YYYYMMDD-HH)
end_date = "20180102-01"

# Forecast hours to download (list of integers, 0 represents analysis files)
forecast_hours = [0]

# Interval between downloads in hours (integer)
time_interval = 24

# Base URL of the HRRR archive
archive_url = 'https://noaa-hrrr-bdp-pds.s3.amazonaws.com'

# Local directory to save downloaded HRRR files
save_path = "./hrrr/"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# HRRR dataset type [options: "prs", "nat", "sfc"]
dataset_type = 'nat'

##### END OPTIONS #####

# Generate a list of dates within the specified range
start_date_obj = datetime.strptime(start_date, "%Y%m%d-%H")
end_date_obj = datetime.strptime(end_date, "%Y%m%d-%H")
date_range = [
    start_date_obj + timedelta(hours=time_interval * i) 
    for i in range(int(((end_date_obj - start_date_obj).total_seconds() / 3600) // time_interval))
]

# Download files for each date and forecast hour
for current_date in date_range:
    for forecast_hour in forecast_hours:
        try:
            # Construct the file name and URL
            file_name = f"hrrr.t{current_date.strftime('%H')}z.wrf{dataset_type}f{forecast_hour:02d}.grib2"
            save_name = f"hrrr.{current_date.strftime('%Y%m%d')}.t{current_date.strftime('%H')}z.wrf{dataset_type}f{forecast_hour:02d}.grib2"
            file_url = f"{archive_url}/hrrr.{current_date.strftime('%Y%m%d')}/conus/{file_name}"

            print(f"Downloading: {file_url}")
            ureq.urlretrieve(file_url, os.path.join(save_path, save_name))
        except Exception as e:
            print(f"Error: {save_name} file not found. Reason: {e}")
