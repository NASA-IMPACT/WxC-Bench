# The NCL script produced non-sensical zeros at some places. Replacing NCL conservative regridding with xESMF regridding.
# xESMF does not seem to have that problem. I don not know for sure why the zeros were generated
# Takes 12 minutes for one day 

# Caveat: Some days like 19-28th Feb, 19th-30th September, and 14th-31st October etc only have 12-hourly forecasts
# This was an issue due to corrupted cache. This has been now resolved

import sys
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, interp2d
from os.path import exists
import xesmf as xe
import gc  # garbage collect to free memory after deleting variables

# Load the ERA5 model levels and coefficients
f = "path_to_local_data/era5_model_levels_table.xlsx"
data1 = pd.read_excel(f)

era5_ml = data1['pf']
lev = era5_ml.to_numpy()
ak = data1['a']
bk = data1['b']
ak = ak.to_numpy()
bk = bk.to_numpy()
ak = np.append([0], ak)
bk = np.append([0], bk)

# ==============
# LOAD REGRIDDER
# ==============
# This part loads the regridder that will convert data from the ERA5 grid to the target T42 grid

# Input - ERA5 grid
date = '31Dec2013'  # Use specific date for regridding (this could be a parameterized input)
f1 = 'path_to_local_data/full_helmholtz_era5/helmholtz_fluxes_hourly_era5_' + date + '.nc'
nc = Dataset(f1)
lon_in = nc.variables['lon'][:]
lat_in = nc.variables['lat'][:]
nx = len(lon_in)
ny = len(lat_in)

# Creating boundary lat/lon
lon_in_b = np.zeros(nx + 1)
lat_in_b = np.zeros(ny + 1)

# Calculating boundary longitude and latitude values
lon_in_b[1:-1] = 0.5 * (lon_in[1:] + lon_in[:-1])
lon_in_b[0] = -lon_in_b[1]  # Adjusting boundary values
lon_in_b[-1] = lon_in_b[-2] + 0.3  # Adjusting boundary values

lat_in_b[1:-1] = 0.5 * (lat_in[1:] + lat_in[:-1])
lat_in_b[0] = lat_in_b[1] + (lat_in[0] - lat_in[1])
lat_in_b[-1] = lat_in_b[-2] - (lat_in[-2] - lat_in[-1])

# Output - T42 grid (target grid)
f2 = 'path_to_local_data/t42_lat_and_latb.nc'
nc = Dataset(f2)
lon_out = nc.variables['lon'][:]
lat_out = nc.variables['lat'][:]
lon_out_b = nc.variables['lonb'][:]
lat_out_b = nc.variables['latb'][:]

grid_in = {"lon": lon_in, "lat": lat_in, "lon_b": lon_in_b[:], "lat_b": lat_in_b[:]}
grid_out = {"lon": lon_out[:], "lat": lat_out[:], "lon_b": lon_out_b[:], "lat_b": lat_out_b[:]}

# Initialize regridder (conservative regridding method)
regridder = xe.Regridder(grid_in, grid_out, method="conservative", reuse_weights=True,
                         filename='path_to_local_data/conservative_601x1200_64x128.nc') 

# ===============
# REGRIDDING DATA
# ===============
# This section handles the data regridding for ERA5 fields over the specified months and days

yr = int(sys.argv[1])  # Year input
m1 = int(sys.argv[2])  # Starting month
m2 = int(sys.argv[3])  # Ending month

# Month names for output formatting
MON = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

# Directory for input files
diri = 'path_to_local_data/ERA5_data_ml_ag4680/'
nx = 128
ny = 64
nz = 137
frq = 24  # Frequency (time steps per day)
P0 = 1e5  # Reference pressure in Pa
gamm = -0.286  # Poisson constant
R = 287.053  # Specific gas constant in J/(kg*K)
grav = 9.81  # Gravitational acceleration in m/s^2

# Arrays for storing model levels and computed values
p = np.zeros((nz, 601, 1200))  # Pressure
dudp = np.zeros((nz, 601, 1200))  # Vertical gradient of zonal wind
dthdp = np.zeros((nz, 601, 1200))  # Vertical gradient of temperature
flux_p = np.zeros((nz, 601, 1200))  # Fluxes

# Loop through the months and days
for mon in np.arange(m1, m2 + 1):
    if mon in np.array([1, 3, 5, 7, 8, 10, 12]):
        ndays = 31
    elif mon in np.array([4, 6, 9, 11]):
        ndays = 30
    elif (mon == 2) and np.mod(yr, 4) == 0:
        ndays = 29
    else: 
        ndays = 28

    if len(sys.argv) == 4:
        d1 = 1
        d2 = ndays
    elif len(sys.argv) == 6:
        d1 = int(sys.argv[4])
        d2 = int(sys.argv[5])

    # Loop over days in the month
    for day in np.arange(d1, d2 + 1):
        print(f"Processing day {day}")

        # Output file for regridded data
        fout = f'path_to_local_data/training_data/era5/era5_training_data_hourly_era5_{str(yr)}{MON[mon]}{str(day).zfill(2)}.nc'
        
        # Check if output file exists, create or append as needed
        if not exists(fout):  # create file
            type = 1
            out = Dataset(fout, "w", format="NETCDF4")
            print('File does not exist: creating ...')

            # Define dimensions
            otime = out.createDimension("time", frq)
            otime_fc_u = out.createDimension("time_fc_u", None)  # None means unlimited
            otime_fc_v = out.createDimension("time_fc_v", None)
            olev = out.createDimension("level", nz)
            olat = out.createDimension("lat", ny)
            olon = out.createDimension("lon", nx)

            # Create dimension variables
            times = out.createVariable("time", "i4", ("time",))
            times.long_name = 'analysis time stamp'
            levels = out.createVariable("level", "f4", ("level",))
            levels.units = 'hPa'
            lats = out.createVariable("lat", "f4", ("lat",))
            lats.units = 'degrees_north'
            lons = out.createVariable("lon", "f4", ("lon",))
            lons.units = 'degrees_east'

            # Time for forecast variables
            times_fc_u = out.createVariable("time_fc_u", "i4", ("time_fc_u",))
            times_fc_u.long_name = 'forecast time stamp for du'
            
            times_fc_v = out.createVariable("time_fc_v", "i4", ("time_fc_v",))
            times_fc_v.long_name = 'forecast time stamp for dv'

            # Analysis fields (u, v, w, etc.)
            o_u = out.createVariable("u", "f4", ("time", "level", "lat", "lon"))
            o_u.units = 'm/s'
            o_u.long_name = 'u: Zonal wind'

            o_v = out.createVariable("v", "f4", ("time", "level", "lat", "lon"))
            o_v.units = 'm/s'
            o_v.long_name = 'v: Meridional wind'

            o_w = out.createVariable("w", "f4", ("time", "level", "lat", "lon"))
            o_w.units = 'Pa/s'
            o_w.long_name = 'w: Vertical wind'

            o_t = out.createVariable("t", "f4", ("time", "level", "lat", "lon"))
            o_t.units = 'K'
            o_t.long_name = 'Temperature'

            o_p = out.createVariable("p", "f4", ("time", "level", "lat", "lon"))
            o_p.units = 'Pa'
            o_p.long_name = 'Pressure'

            # Other variables (vertical gradients, stratification frequency, geopotential)
            o_dudp = out.createVariable("dudp", "f4", ("time", "level", "lat", "lon"))
            o_dudp.units = 'm/s/Pa'
            o_dudp.long_name = 'Vertical Gradient of Zonal Wind'

            o_N2 = out.createVariable("N2", "f4", ("time", "level", "lat", "lon"))
            o_N2.units = '1/s^2'
            o_N2.long_name = 'Stratification Frequency Squared'

            o_zs = out.createVariable("zs", "f4", ("time", "level", "lat", "lon"))
            o_zs.units = 'm'
            o_zs.long_name = 'Geopotential Height'

            o_flux_p = out.createVariable("flux_p", "f4", ("time", "level", "lat", "lon"))
            o_flux_p.units = 'W/m^2'
            o_flux_p.long_name = 'Flux of Total Energy'

            # Time steps
            times[:] = np.arange(0, 24, 1)
            times_fc_u[:] = np.arange(0, 24, 1)
            times_fc_v[:] = np.arange(0, 24, 1)

        # Save data (to be filled out further)

        # Free memory (garbage collection) after processing
        del p, flux_p, dudp, dthdp
        gc.collect()
