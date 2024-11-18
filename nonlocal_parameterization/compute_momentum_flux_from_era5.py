# Just activate the conda environment : conda activate jupyter_notebook. It has all these packages.
# Takes around 2 hours for one day

import sys
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xlrd
import pandas as pd
from scipy.interpolate import interp1d, interp2d
from os.path import exists
from windspharm.standard import VectorWind as WindVector

# File paths
f = "<path_to_local_dir>/era5_model_levels_table.xlsx"
g = "<path_to_local_dir>/erainterim_model_levels_table.xlsx"

# Load data from Excel
data1 = pd.read_excel(f)
data2 = pd.read_excel(g)

era5_ml = data1['pf']
lev = era5_ml.to_numpy()
ht = data1['z_geom'] / 1000
ak = data1['a']
bk = data1['b']
ht = ht.to_numpy()
ak = ak.to_numpy()
bk = bk.to_numpy()
erai_ml = data2['pf']
ak = np.append([0], ak)
bk = np.append([0], bk)

# ======================
# USER-DEFINED FUNCTIONS
# ======================

def load(nc, var_name):
    """
    Load a variable from a netCDF file.
    
    Parameters:
    nc (netCDF4.Dataset): The netCDF dataset object.
    var_name (str): The variable name to extract from the dataset.
    
    Returns:
    netCDF4.Variable: The extracted variable.
    """
    return nc.variables[var_name]

def whiten(v, cmap):
    """
    Modify the colormap to make the center white for visualizing symmetric data.
    
    Parameters:
    v (array-like): The values to be visualized.
    cmap (str): The name of the colormap to modify.
    
    Returns:
    ListedColormap: The modified colormap.
    """
    from matplotlib.colors import ListedColormap
    nv = len(v)
    A = plt.get_cmap(cmap, nv)
    editcmap = A(np.arange(nv))
    editcmap[int(nv / 2) - int(0.1 * nv) + 1:int(nv / 2) + int(0.1 * nv), 0:4] = 1.
    newcmp = ListedColormap(editcmap)
    
    return newcmp

# Load netCDF data for latitude, longitude
f = '<path_to_local_dir>/t42_lat_lon.nc'
nc = Dataset(f)
lon_t42 = nc.variables['lon'][:]
lat_t42 = nc.variables['lat'][:]

# ===============================================================================================================

# File paths for netCDF data output
outdir = '<path_to_local_dir>/full_helmholtz_era5/'

# Month and gravity constant
mon = ['None', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
g = -9.81
d1 = 1
d2 = 30
frq = 24  # Frequency (hours)

# Determine days in the month
year = int(sys.argv[1])
m = int(sys.argv[2])

if m in np.array([1, 3, 5, 7, 8, 10, 12]):
    ndays = 31
elif m in np.array([4, 6, 9, 11]):
    ndays = 30
elif (m == 2) and (np.mod(year, 4) == 0):
    ndays = 29
else:
    ndays = 28

if len(sys.argv) == 3:
    d1 = 1
    d2 = ndays
elif len(sys.argv) == 5:
    d1 = int(sys.argv[3])
    d2 = int(sys.argv[4])

log_filename = f"<path_to_local_dir>/era5_gwmf_compute_output_{year}_{mon[m]}.txt"

def write_log(*args):
    """
    Write log messages to a file and print them to the console.
    
    Parameters:
    *args: The log messages to write.
    """
    line = ' '.join([str(a) for a in args])
    with open(log_filename, "a") as log_file:
        log_file.write(line + '\n')
    print(line)

# Processing loop for each day in the month
for day in np.arange(d1, d2 + 1):
    f = f'<path_to_local_dir>/ERA5_data_ml_ag4680/U{year}{str(m).zfill(2)}{str(day).zfill(2)}_ml.nc'
    write_log(f)
    nc1 = Dataset(f)
    if day == d1:
        lon = nc1.variables['longitude'][:]
        nx = len(lon)
        lat = nc1.variables['latitude'][:]
        ny = len(lat)
        nz = 137
    
    ucomp = nc1.variables['u']
    f = f'<path_to_local_dir>/ERA5_data_ml_ag4680/V{year}{str(m).zfill(2)}{str(day).zfill(2)}_ml.nc'
    nc2 = Dataset(f)
    vcomp = nc2.variables['v']
    f = f'<path_to_local_dir>/ERA5_data_ml_ag4680/W{year}{str(m).zfill(2)}{str(day).zfill(2)}_ml.nc'
    nc3 = Dataset(f)
    wcomp = nc3.variables['w']

    # Output filename
    outfile = f'helmholtz_fluxes_hourly_era5_{day}{mon[m]}{year}.nc'
    fout = outdir + outfile
    
    if not exists(fout):  # Create file if it does not exist
        type = 1
        out = Dataset(fout, "w", format="NETCDF4")
        write_log('File does not exist: creating ...')
        
        # Define dimension variables
        otime = out.createDimension("time", frq)
        olev = out.createDimension("level", nz)
        olat = out.createDimension("lat", ny)
        olon = out.createDimension("lon", nx)
        
        # Create dimension vectors
        times = out.createVariable("time", "i4", ("time",))
        levels = out.createVariable("level", "f4", ("level",))
        levels.units = 'hPa'
        lats = out.createVariable("lat", "f4", ("lat",))
        lats.units = 'degrees_north'
        lons = out.createVariable("lon", "f4", ("lon",))
        lons.units = 'degrees_east'

        # Full variables
        o_uw = out.createVariable("uw", "f4", ("time", "level", "lat", "lon"))
        o_uw.units = 'Pa'
        o_uw.long_name = 'uw/g: Zonal flux of vertical momentum'

        o_vw = out.createVariable("vw", "f4", ("time", "level", "lat", "lon"))
        o_vw.units = 'Pa'
        o_vw.long_name = 'vw/g: Meridional flux of vertical momentum'

        # Set dimension variables
        times[:] = np.arange(0, frq, 1)
        levels[:] = lev
        lats[:] = lat[:]
        lons[:] = lon[:]
    else:  # Append to the existing file
        type = 2
        out = Dataset(fout, "a", format="NETCDF4")
        write_log('File exists: appending ...')
        o_uw = out.variables['uw']
        o_vw = out.variables['vw']

    # Loop through each time step and level
    for ind in np.arange(0, frq):
        write_log(ind)
        for iz in np.arange(0, 137):
            u = ucomp[ind, iz, :, :]
            v = vcomp[ind, iz, :, :]
            
            # Compute the wind vector and its components
            fld = WindVector(u, v, legfunc='computed')  # Vector field
            udiv, vdiv = fld.irrotationalcomponent()
            udiv21 = fld.truncate(udiv, truncation=21)
            vdiv21 = fld.truncate(vdiv, truncation=21)
            
            # Compute eddy flux
            w = wcomp[ind, iz, :, :]
            wmean = np.mean(w, 1)
            w = w - wmean[:, np.newaxis]
            uw = (udiv - udiv21) * w
            vw = (vdiv - vdiv21) * w
            
            # Write results to the netCDF file
            o_uw[ind, iz, :, :] = uw / g
            o_vw[ind, iz, :, :] = vw / g

    # Close files after processing
    nc1.close()
    nc2.close()
    nc3.close()
    out.close()

write_log('Done')
