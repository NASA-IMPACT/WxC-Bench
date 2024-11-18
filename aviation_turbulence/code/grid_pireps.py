### This script takes the downloaded pireps, filters them, and bins them
### by day onto the MERRA 2 grid.
###
### Further, the data is converted to a binary classification indicating whether
### moderate or greater (MOG) turbulence is present.
###
### Christopher Phillips

##### START OPTIONS #####

# Locations of the PIREPS files
fpaths = ['updated_CSVs/low_fl.csv',
          'updated_CSVs/med_fl.csv',
          'updated_CSVs/high_fl.csv']

# Location to save the gridded data
sdir = 'new_gridded_data/'

# Fraction of reports that must be MOG before cell is classified as turbulence
threshold = 0.25

# No data value
nodata = 2

#####  END OPTIONS  #####

# Import the required modules
import matplotlib.pyplot as pp
import netCDF4 as nc
import numpy as np
import pandas as pd

# Helper function for finding minum of 2D array
# From this stack overflow:
# https://stackoverflow.com/questions/30180241/numpy-get-the-column-and-row-index-of-the-minimum-value-of-a-2d-array
def find_min_idx(x):
    k = x.argmin()
    ncol = x.shape[1]
    return int(k//ncol), int(k%ncol)

# Build the MERRA 2 grid
dx = 0.625
dy = 0.5
nx = 576
ny = 361
type = 'deg'
x = np.arange(-180, -180+dx*nx, dx)
y = np.arange(-90, -90+dy*ny, dy)
xg, yg = np.meshgrid(x, y)

# Loop over the input files
for fpath in fpaths:

    # Open the PIREPS file and sort by date
    pdf = pd.read_csv(fpath)
    pdf = pdf.sort_values(by='VALID')

    # Initialize arrays for counting reports and storing turbulence value
    turbulence = np.zeros((y.size, x.size)) # MOG turbulence
    counts = np.zeros((y.size, x.size))     # Report count
    binaries = []   # List to hold turbulence occurrence arrays
    dates = []      # List to hold the dates

    # Loop over each row
    date = str(pdf.VALID.iloc[0])[:8]
    year = date[:4]
    for index, row in pdf.iterrows():
        
        # Grab the new date
        new_date = str(row.VALID)[:8]
        new_year = new_date[:4]

        if (new_year != '2023'):
            date = new_date
            year = new_year
            continue

        if (new_date != date):

            # Append old date to date list
            dates.append(date)

            # Compute turbulence occurence
            dummy = turbulence/counts
            dummy[dummy >= threshold] = 1 # yes turbulence
            dummy[dummy < 1] = 0          # no turbulence
            dummy[counts == 0] = nodata       # no data
            binaries.append(dummy)

            # Reset values
            turbulence = np.zeros((y.size, x.size))
            counts = np.zeros((y.size, x.size))
            date = new_date

        if (new_year != year):

            # Write out the data
            out = nc.Dataset(f"{sdir}/{year}_{fpath.split('/')[-1].replace('csv','nc')}", "w")
            out.description = 'Daily moderate or greater turbulence presence from PIREPS reports gridded onto the MERRA 2 grid.'

            # Data dimensions
            out.createDimension('Time',len(binaries))
            out.createDimension('Y', xg.shape[0])
            out.createDimension('X', xg.shape[1])
            out.createDimension('StringLength', 8)

            # Variables
            turb_var = out.createVariable('Turbulence', 'uint8', ('Time', 'Y', 'X'))
            turb_var.long_name = 'Turbulence Presence (1=Yes, 0=No)'
            turb_var.missing_data_value = str(nodata)
            date_var = out.createVariable('Dates', 'S8', ('Time',))#, 'StringLength'))
            date_var.long_name = 'Date of turbulence report (UTC)'
            lon_var = out.createVariable('Lons', 'f8', ('Y', 'X'))
            lon_var.long_name = 'Longitude (deg)'
            lat_var = out.createVariable('Lats', 'f8', ('Y', 'X'))
            lat_var.long_name = 'Latitude (deg)'

            # Save the data
            turb_var[:] = np.array(binaries)
            date_var[:] = np.array(dates)
            lon_var[:] = xg
            lat_var[:] = yg

            # Close the file
            out.close()

            # Reset variables
            print(year, new_year)
            year = new_year
            binaries = []   # List to hold turbulence occurrence arrays
            dates = []      # List to hold the dates

        # Assign grid point
        dist = (row.LON-xg)**2+(row.LAT-yg)**2
        yind, xind = find_min_idx(dist)
        
        # Determine if report is moderate or greater
        if (row.Intensity >= 2):
            turbulence[yind,xind] += 1
        counts[yind,xind] += 1

    print(len(dates))
    print(dates[:10])

    # Write out the last year
    out = nc.Dataset(f"{sdir}/{year}_{fpath.split('/')[-1].replace('csv','nc')}", "w")
    out.description = 'Daily moderate or greater turbulence presence from PIREPS reports gridded onto the MERRA 2 grid.'

    # Data dimensions
    out.createDimension('Time',len(binaries))
    out.createDimension('Y', xg.shape[0])
    out.createDimension('X', xg.shape[1])
    out.createDimension('StringLength', 8)

    # Variables
    turb_var = out.createVariable('Turbulence', 'uint8', ('Time', 'Y', 'X'))
    turb_var.long_name = 'Turbulence Presence (1=Yes, 0=No)'
    turb_var.missing_data_value = str(nodata)
    date_var = out.createVariable('Dates', 'S8', ('Time',))#, 'StringLength'))
    date_var.long_name = 'Date of turbulence report (UTC)'
    lon_var = out.createVariable('Lons', 'f8', ('Y', 'X'))
    lon_var.long_name = 'Longitude (deg)'
    lat_var = out.createVariable('Lats', 'f8', ('Y', 'X'))
    lat_var.long_name = 'Latitude (deg)'

    # Save the data
    turb_var[:] = np.array(binaries)
    date_var[:] = np.array(dates)
    lon_var[:] = xg
    lat_var[:] = yg

    # Close the file
    out.close()

    # Reset variables
    year = new_year
    binaries = []   # List to hold turbulence occurrence arrays
    dates = []      # List to hold the dates