### This module contains teh data loader for the Turbulence Prediction
### training data.
### Christopher Phillips

### Import required modules
import netCDF4 as nc
import numpy as np
import torch
from sklearn.preprocessing import minmax_scale

### The data loader
def load_training_data(fpath):

    # Open the netCDF file
    dummy = [] # List to temporarily hold input arrays
    fn = nc.Dataset(fpath, 'r')
    y = fn.variables['TURBULENCE'][:]
    dummy.append(fn.variables['T'][:])
    dummy.append(fn.variables['U'][:])
    dummy.append(fn.variables['V'][:])
    dummy.append(fn.variables['OMEGA'][:])
    dummy.append(fn.variables['RH'][:])
    dummy.append(fn.variables['H'][:])
    dummy.append(fn.variables['PL'][:])
    #dummy.append(np.expand_dims(fn.variables['PHIS'][:], 1))
    fn.close()
        
    # Concatenate the features array
    X = np.concatenate(dummy, axis=1)
    
    return X, y
    
### A data loader for treating all levels as one data set
def load_all_training_data(fdir):

    fn1 = nc.Dataset(fdir+'training_data_low_fl.nc')
    fn2 = nc.Dataset(fdir+'training_data_med_fl.nc')
    fn3 = nc.Dataset(fdir+'training_data_high_fl.nc')

    # Open the netCDF file
    dummy = [] # List to temporarily hold input arrays
    y = np.concatenate([fn1.variables['TURBULENCE'][:], fn2.variables['TURBULENCE'][:], fn3.variables['TURBULENCE'][:]], axis=0)
    dummy.append(np.concatenate([fn1.variables['T'][:], fn2.variables['T'][:], fn3.variables['T'][:]], axis=0))
    dummy.append(np.concatenate([fn1.variables['U'][:], fn2.variables['U'][:], fn3.variables['U'][:]], axis=0))
    dummy.append(np.concatenate([fn1.variables['V'][:], fn2.variables['V'][:], fn3.variables['V'][:]], axis=0))
    dummy.append(np.concatenate([fn1.variables['OMEGA'][:], fn2.variables['OMEGA'][:], fn3.variables['OMEGA'][:]], axis=0))
    dummy.append(np.concatenate([fn1.variables['RH'][:], fn2.variables['RH'][:], fn3.variables['RH'][:]], axis=0))

    fn1.close()
    fn2.close()
    fn3.close()
    
    # Concatenate the features array
    X = np.concatenate(dummy, axis=1)
    
    return X, y