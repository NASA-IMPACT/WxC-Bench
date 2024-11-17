# Use this script to download analysis fields: T,U,V and W
# Use the bash script analysis_download_general.sh to submit download jobs for custom days, months or years 

import sys
import cdsapi
import numpy as np

# Initialize the CDS API client
c = cdsapi.Client()

def get_days_in_month(year, month):
    """
    Calculate the number of days in a given month and year, accounting for leap years.
    
    Parameters:
    year (int): The year.
    month (int): The month (1-12).
    
    Returns:
    int: The number of days in the month.
    """
    if month in np.array([1, 3, 5, 7, 8, 10, 12]):
        return 31
    elif month in np.array([4, 6, 9, 11]):
        return 30
    elif (month == 2) and (np.mod(year, 4) == 0):
        return 29
    else:
        return 28

def download_data(year, month, d1, d2, param, outfile):
    """
    Download the ERA5 model data for a specific field (T, U, V, or W).
    
    Parameters:
    year (int): The year.
    month (int): The month (1-12).
    d1 (int): The start day of the month.
    d2 (int): The end day of the month.
    param (str): The parameter code for the field to download.
    outfile (str): The output filename where the data will be saved.
    """
    for day in np.arange(d1, d2 + 1):
        date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
        date2 = str(year) + str(month).zfill(2) + str(day).zfill(2)
        
        # Output filename
        print(outfile)
        c.retrieve('reanalysis-era5-complete', {
            'date'    : date,            
            'levelist': '1/to/137/by/1',          
            'levtype' : 'ml',
            'param'   : param,                   
            'stream'  : 'oper',                 
            'time'    : '00/to/23/by/1',         
            'type'    : 'an',
            'grid'    : '0.3/0.3',               
            'format'  : 'netcdf',                
        }, outfile)
	
	# DO NOT DONLOAD THESE EMSEMBLE SURFACE FIELDS
	# RATHER- DOWNLOAD SURFACE FIELDS USING THE surfacefields_download_general.py file
	#outfile='/scratch/groups/aditis2/ERA5_data_ml_ag4680/PS'+date2+'_ml.nc'
        #print(outfile)
        #c.retrieve('reanalysis-era5-single-levels', { # Requests follow MARS syntax
                                                 # Keywords 'expver' and 'class' can be dropped. They are obsolete
                                                 # since their values are imposed by 'reanalysis-era5-complete'
        #    'date'    : date,            # The hyphens can be omitted
        #    'levtype' : 'sfc',
        #    'param'   : '134',                   # Full information at https://apps.ecmwf.int/codes/grib/param-db/
                                         # The native representation for temperature is spherical harmonics
        #    'stream'  : 'oper',                  # Denotes ERA5. Ensemble members are selected by 'enda'
        #    'time'    : '00/to/23/by/1',         # You can drop :00:00 and use MARS short-hand notation, instead of '00/06/12/18'
        #    'type'    : 'an',
        #    #'area'    : 'global',          # North, West, South, East. Default: global
        #    'grid'    : '0.3/0.3',               # Latitude/longitude. Default: spherical harmonics or reduced Gaussian grid
        #    'format'  : 'netcdf',                # Output needs to be regular lat-lon, so only works in combination with 'grid'!
        #}, outfile);     # Output file. Adapt as you wish.


	#outfile='/scratch/groups/aditis2/ERA5_data_ml_ag4680/ZS'+date2+'_ml.nc'
        #print(outfile)
        #c.retrieve('reanalysis-era5-single-levels', { # Requests follow MARS syntax
                                                 # Keywords 'expver' and 'class' can be dropped. They are obsolete
                                                 # since their values are imposed by 'reanalysis-era5-complete'
        #    'date'    : date,            # The hyphens can be omitted
        #    'levtype' : 'sfc',
        #    'param'   : '129',                   # Full information at https://apps.ecmwf.int/codes/grib/param-db/
        #                                 # The native representation for temperature is spherical harmonics
        #    'stream'  : 'oper',                  # Denotes ERA5. Ensemble members are selected by 'enda'
        #    'time'    : '00/to/23/by/1',         # You can drop :00:00 and use MARS short-hand notation, instead of '00/06/12/18'
        #    'type'    : 'an',
        #    #'area'    : 'global',          # North, West, South, East. Default: global
        #    'grid'    : '0.3/0.3',               # Latitude/longitude. Default: spherical harmonics or reduced Gaussian grid
        #    'format'  : 'netcdf',                # Output needs to be regular lat-lon, so only works in combination with 'grid'!
        #}, outfile);     # Output file. Adapt as you wish.

def main():
    # Get input year and month
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    
    # Calculate number of days in the month
    ndays = get_days_in_month(year, month)
    
    # Default days range if not specified
    if len(sys.argv) == 3:
        d1, d2 = 1, ndays
    elif len(sys.argv) == 5:
        d1 = int(sys.argv[3])
        d2 = int(sys.argv[4])

    # Loop over each day and download data
    for day in np.arange(d1, d2 + 1):
        date2 = str(year) + str(month).zfill(2) + str(day).zfill(2)
        
        # Download temperature (T)
        outfile = f'<path_to_local_directory>/ERA5_data_ml_ag4680/T{date2}_ml.nc'
        download_data(year, month, day, day, '130', outfile)

        # Download zonal wind (U)
        outfile = f'<path_to_local_directory>/ERA5_data_ml_ag4680/U{date2}_ml.nc'
        download_data(year, month, day, day, '131', outfile)

        # Download meridional wind (V)
        outfile = f'<path_to_local_directory>/ERA5_data_ml_ag4680/V{date2}_ml.nc'
        download_data(year, month, day, day, '132', outfile)

        # Download vertical wind (W)
        outfile = f'<path_to_local_directory>/ERA5_data_ml_ag4680/W{date2}_ml.nc'
        download_data(year, month, day, day, '135', outfile)

if __name__ == "__main__":
    main()
	# add 'truncation' : '21' to get the T21 field.
	# for netCDF - specifying regular grid is mandatory.
	# The lat/long equivalent of T639 is 0.28125 deg (360/(2*(639+1))). However, the GRIB1 format only supports three decimals, so we recommend that you round the resolution to 0.25 deg (giving 360/0.25=1440 equally-spaced grid points). Specifying a higher resolution is technically possible, e.g. as 'grid':'0.1/0.1', but  this only oversamples the data and does not improve the accuracy of the data. Specifying a coarser resolution is also possible, but in this case, care should be taken to avoid aliasing.

	# Use 'an' for analysis fields and 'fc' for forecast fields like du/dv (235007/235008).

	# T,u,v,w (Pa/s) have code 130/131/132/135 respectively
