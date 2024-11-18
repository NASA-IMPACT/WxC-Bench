# HRRR Weather Data Processing and Caption Generation

This project processes High-Resolution Rapid Refresh (HRRR) weather data and associated forecast reports for machine learning purposes.

## Overview

The project consists of two main scripts that handle:
1. Downloading HRRR weather data files
2. Creating metadata files that pair weather data with corresponding forecast discussions

## Scripts

### 1. download_hrrr.py

This script downloads HRRR weather data files from NOAA's public dataset.

Key features:
- Downloads HRRR grib2 files from NOAA's S3 bucket
- Configurable date range and time intervals
- Supports different forecast hours and dataset types (pressure, natural, surface)
- Automatically creates storage directory if it doesn't exist

Configuration options:
```python
start_date = "20180101-01"  # Format: YYYYMMDD-HH
end_date = "20180102-01"
fhours = [0]  # Forecast hours to download
dt = 24  # Download frequency in hours
```

### 2. create_metadata.py

This script creates a metadata CSV file that pairs HRRR weather data files with their corresponding forecast discussions.

Key features:
- Matches HRRR grib2 files with their corresponding caption files
- Extracts forecast discussions from CSV files
- Creates a metadata file suitable for machine learning training
- Output format: CSV with columns `file_name` and `text`

Usage example:
```python
image_directory = "hrrr"  # Directory containing HRRR files
caption_directory = "csv_reports"  # Directory containing forecast discussions
output_metadata_file = "metadata.csv"
```

## File Format Conventions

- HRRR files: `hrrr.20180101.t01z.wrfnatf00.grib2`
- Caption files: `20180101.csv`
- Output metadata: `metadata.csv`
