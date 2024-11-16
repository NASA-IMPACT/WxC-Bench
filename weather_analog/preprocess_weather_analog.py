#!/usr/bin/env python
"""
Script to process MERRA2 data by extracting SLP and T2M variables for a specific region
and time period, saving daily files with the processed data.
"""

import os
import xarray as xr
from datetime import datetime, timedelta
import glob

# Define input and output directories
input_dir = "/data/to/directory/MERRA2_v2/dataset/M2I1NXASM/"
output_dir = "/data/to/directory/MERRA2_v2/dataset/M2I1NXASM_processed_V1/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Configuration parameters
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2021, 12, 31)

# Geographic bounds for the region of interest
LON_BOUNDS = (-15, 0)
LAT_BOUNDS = (42, 58)

def process_single_file(input_file, output_file):
    """Process a single MERRA2 file and save the extracted data."""
    try:
        with xr.open_dataset(input_file) as ds:
            # Select required variables and region
            ds_selected = (ds[['SLP', 'T2M']]
                         .sel(lon=slice(*LON_BOUNDS), 
                              lat=slice(*LAT_BOUNDS))
                         .isel(time=[0]))
            
            # Save processed data
            ds_selected.to_netcdf(output_file)
            print(f"Processed {input_file} -> {output_file}")
            return True
            
    except Exception as e:
        print(f"Failed to process {input_file}: {e}")
        return False

def main():
    """Main processing loop."""
    current_date = START_DATE
    while current_date <= END_DATE:
        date_str = current_date.strftime("%Y%m%d")
        
        # Construct file paths
        try:
            input_file = glob.glob(os.path.join(input_dir, f"MERRA2*.{date_str}.SUB.nc"))[0]
        except IndexError:
            print(f"No input file found for date: {date_str}")
            current_date += timedelta(days=1)
            continue
            
        output_file = os.path.join(output_dir, f"MERRA2_SLP_T2M_{date_str}.nc")

        # Skip if output exists
        if os.path.isfile(output_file):
            print(f"Output file already exists: {output_file}")
            current_date += timedelta(days=1)
            continue

        if os.path.isfile(input_file):
            process_single_file(input_file, output_file)
        else:
            print(f"File not found: {input_file}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
