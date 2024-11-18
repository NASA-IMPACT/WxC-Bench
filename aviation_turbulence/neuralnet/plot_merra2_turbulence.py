### This program loads a MERRA 2 file for a day and runs
### the turbulence AI over each grid cell to produce a map
### Christopher Phillips

##### START OPTIONS #####

# Location of the MERRA 2 data
mdir = '/data/to/directory/MERRA2_78vavrs/'

# AI files
checkpoint = '/data/to/directory/checkpoints_low/checkpoint_2024-01-25_1556.pt'
norms_file = '/data/to/directory/checkpoints_low/norm_mean_std_2024-01-25_1556.npz'

# Location to save the plots
sdir = '/data/to/directory/plots/'

#####  END OPTIONS  #####

# Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime
from glob import glob
import matplotlib.pyplot as pp
import netCDF4 as nc
import numpy as np
from sklearn.preprocessing import minmax_scale

from TurbulenceNN import TURBnet

# Create indices that match the MERRA 2 grid
yinds = np.arange(0, 361, dtype='int')
xinds = np.arange(0, 576, dtype='int')
lons = -180.0+0.625*xinds
lats = -90.0+0.5*yinds
long, latg = np.meshgrid(lons, lats)

# Load the AI
tnet = TURBnet(n_features=65)
tnet.load_model(checkpoint)
norms = np.load(norms_file)
nmean = norms['mean']
nstd = norms['std']

# Locate all MERRA 2 files
mfiles = sorted(glob(mdir+'*.nc'))

# Loop over the MERRA 2 files
for mfile in mfiles:

    mdate = datetime.strptime(mfile[-15:-7], '%Y%m%d')
    data = {'OMEGA': [], 'RH': [], 'T': [], 'U': [], 'V': []}

    # Extract all the profiles from MERRA 2
    mfn = nc.Dataset(mfile, 'r')
    for xind in xinds:
        for yind in yinds:
        
            # Extract the MERRA 2 weather profile
            for v in ['OMEGA', 'RH', 'T', 'U', 'V']:
                data[v].append(np.squeeze(mfn.variables[v][7,:,yind,xind])) # Time 7 is 18Z (noonish local)
    mfn.close()
    
    # Adjust the data for use as input to the neural net
    # Open the netCDF file
    dummy = [] # List to temporarily hold input arrays
    dummy.append(data['T'][:])
    dummy.append(data['U'][:])
    dummy.append(data['V'][:])
    dummy.append(data['OMEGA'][:])
    dummy.append(data['RH'][:])
    
    # Clean up memory a bit
    del data
    
    # Concatenate the features array
    X = np.concatenate(dummy, axis=1)

    # Normalize the data
    for i in range(nmean.size):
        X[:,i] = (X[:,i]-nmean[i])/nstd[i]

    # Estimate turbulence at each grid point
    turb = tnet.predict(X)
    
    # Refill the turbulence array
    turbulence = np.zeros(long.shape)
    i = 0
    for xind in xinds:
        for yind in yinds:
            turbulence[yind,xind] = turb[i]
            i += 1
            
    # Re-scale turbulence risk to [0, 100]
    turbulence *= 100.0
            
    # plot
    proj = ccrs.PlateCarree()
    fig, ax = pp.subplots(subplot_kw = {'projection': proj})
    cont = ax.pcolormesh(long, latg, turbulence, vmin=0.0, vmax=100.0, cmap='turbo')
    
    # Colorbar
    cb = fig.colorbar(cont, orientation='horizontal')
    cb.set_label('Turbulence Risk (%)', fontsize=14, fontweight='roman')
    
    # Map features
    ax.coastlines()
    ax.add_feature(cfeature.STATES)
    ax.set_extent([-130, -60, 24, 50])
    
    pp.savefig(sdir+f'/turbulence_{mdate.strftime("%Y%m%d")}.png')
    pp.close()