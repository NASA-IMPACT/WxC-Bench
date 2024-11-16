# MERRA2 Weather Data Processor

A Python script for processing MERRA2 (Modern-Era Retrospective analysis for Research and Applications, Version 2) meteorological data by extracting specific variables (Sea Level Pressure and 2-meter Temperature) for a defined geographic region.

## Overview

This script processes MERRA2 NetCDF files by:
- Extracting Sea Level Pressure (SLP) and 2-meter Temperature (T2M) variables
- Filtering data for a specific geographic region (42°N-58°N, 15°W-0°E)
- Processing data for a defined time period (2019-2021)
- Saving processed data into daily NetCDF files

## Usage

1. Set up your input and output directories in the script:
```python
input_dir = "/data/to/directory/MERRA2_v2/dataset/M2I1NXASM/"
output_dir = "/data/to/directory/MERRA2_v2/dataset/M2I1NXASM_processed_V1/"
```

2. Configure the time period and geographic bounds if needed:
```python
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2021, 12, 31)
LON_BOUNDS = (-15, 0)
LAT_BOUNDS = (42, 58)
```

3. Run the script:
```bash
python preprocess_weather_analog.py
```

## File Structure

The script processes input files with the format:
- Input: `MERRA2*.YYYYMMDD.SUB.nc`
- Output: `MERRA2_SLP_T2M_YYYYMMDD.nc`

## Features

- **Automatic File Processing**: Processes all files within the specified date range
- **Skip Existing Files**: Avoids reprocessing already processed dates
- **Error Handling**: Robust error handling for missing or corrupt files
- **Progress Tracking**: Prints processing status for each file

## Code Structure

The script is organized into two main functions:

1. `process_single_file(input_file, output_file)`:
   - Opens MERRA2 NetCDF file
   - Extracts SLP and T2M variables
   - Filters for specified geographic region
   - Saves processed data to new NetCDF file

2. `main()`:
   - Iterates through dates in the specified range
   - Handles file path construction
   - Manages file existence checks
   - Orchestrates the processing workflow

The script is designed to be memory-efficient by processing one file at a time and includes comprehensive error handling to ensure robust operation even with missing or problematic input files.