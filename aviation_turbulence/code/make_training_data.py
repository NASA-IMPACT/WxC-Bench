### This program extracts MERRA 2 profiles matching
### turbulence detections from PIREPS.
### Christopher Phillips

##### START OPTIONS #####

# Directory with the turbulence files
tdir = './gridded_data/'

# Directory with the MERRA 2 data
mdir = './MERRA2_2021-2022_1000hPa-100hPa/'

# Years to process
years = [2021,2022]

# Levels to process
levels = ['low', 'med', 'high']

# Location to save the new files
sdir = './training_data_20240126/'

#####  END OPTIONS  #####


# Import modules
import netCDF4 as nc
import numpy as np

# Create indices that match the MERRA 2 grid
yinds = np.arange(0, 361, dtype='int')
xinds = np.arange(0, 576, dtype='int')
xg, yg = np.meshgrid(xinds, yinds)

# Loop over the levels
for level in levels:

    # Dictionary to hold the data for writing
    data = {'TURB': [], 'OMEGA': [], 'RH': [], 'T': [], 'U': [], 'V': [], 'H': [], 'PL': [], 'PHIS': []}

    # Loop over the years
    for year in years:
    
        # Open the Turbulence file
        tfn = nc.Dataset(f'{tdir}/{year}_{level}_fl.nc')
        dates = tfn.variables['Dates'][:]
        turbulence = tfn.variables['Turbulence'][:]
        tfn.close()
        
        # Loop over the dates
        mdate = '00000000'
        for i, d in enumerate(dates):
                
            # Check if currently open MERRA 2 file is correct
            if (d != mdate):
            
                # Open matching MERRA2 file
                try:
                    mfn1.close()
                    mfn2.close()
                except:
                    pass
                    
                try:
                    mfn1 = nc.Dataset(f'{mdir}/U_V_T_RH_OMEGA/MERRA2_400.inst3_3d_asm_Nv.{d}.SUB.nc')
                    mfn2 = nc.Dataset(f'{mdir}/H_PL_PHIS/MERRA2_400.inst3_3d_asm_Nv.{d}.SUB.nc')
                    mdate = d
                except Exception as err:
                    try:
                        mfn1 = nc.Dataset(f'{mdir}/U_V_T_RH_OMEGA/MERRA2_401.inst3_3d_asm_Nv.{d}.SUB.nc')
                        mfn2 = nc.Dataset(f'{mdir}/H_PL_PHIS/MERRA2_401.inst3_3d_asm_Nv.{d}.SUB.nc')
                        mdate = d
                    except:
                        print(err)
                        continue
            
            # Extract points that have turbulence (and their indices)
            mask = turbulence[i,:,:] != 2
            turb = turbulence[i,:,:][mask]
            xinds = xg[mask]
            yinds = yg[mask]
            
            # Loop over just those points
            for xind, yind, t in zip(xinds, yinds, turb):
            
                # Store the turbulence data
                data['TURB'].append(t)
            
                # Extract the MERRA 2 weather profile
                for v in ['OMEGA', 'RH', 'T', 'U', 'V']:
                    data[v].append(np.squeeze(mfn1.variables[v][0,:,yind,xind]))
                for v in ['H', 'PL']:
                    data[v].append(np.squeeze(mfn2.variables[v][0,:,yind,xind]))
                data['PHIS'].append(np.squeeze(mfn2.variables['PHIS'][0,yind,xind]))
                    
            
        # Close any MERRA 2 file that remains open
        try:
            mfn1.close()
            mfn2.close()
        except:
            pass
            
    # Save to output file
    out = nc.Dataset(f'{sdir}/training_data_{level}_fl.nc', 'w')
    out.description = 'Training data for the turbulence prediciton benchmark model.\nWeather data are MERRA 2 profiles at 18Z.'
    
    # Create the dimensions
    s_dim = out.createDimension('samples', len(data['TURB']))
    z_dim = out.createDimension('z', 34)
    
    # Create variables
    turb_var = out.createVariable('TURBULENCE', 'float32', ('samples',))
    turb_var.long_name = 'Turbulence Prediction (training labels, 1=turbulence, 0=none)'
    turb_var[:] = np.array(data['TURB'])
    
    t_var = out.createVariable('T', 'float32', ('samples', 'z'))
    t_var.long_name = 'MERRA 2 Temperature Profile'
    t_var.units = 'K'
    t_var.fill_value = 1e+15
    t_var[:] = np.array(data['T'], dtype=np.float32)
    
    u_var = out.createVariable('U', 'float32', ('samples', 'z'))
    u_var.long_name = 'MERRA 2 U Wind Profile'
    u_var.units = 'm s-1'
    u_var.fill_value = 1e+15
    u_var[:] = np.array(data['U'], dtype=np.float32)
    
    v_var = out.createVariable('V', 'float32', ('samples', 'z'))
    v_var.long_name = 'MERRA 2 V Wind Profile'
    v_var.units = 'm s-1'
    v_var.fill_value = 1e+15
    v_var[:] = np.array(data['V'], dtype=np.float32)
    
    o_var = out.createVariable('OMEGA', 'float32', ('samples', 'z'))
    o_var.long_name = 'MERRA 2 Vertical Velocity Profile'
    o_var.units = 'Pa s-1'
    o_var.fill_value = 1e+15
    o_var[:] = np.array(data['OMEGA'], dtype=np.float32)
    
    q_var = out.createVariable('RH', 'float32', ('samples', 'z'))
    q_var.long_name = 'MERRA 2 Relative Humidity Profile'
    q_var.units = '1'
    q_var.fill_value = 1e+15
    q_var[:] = np.array(data['RH'], dtype=np.float32)
    
    h_var = out.createVariable('H', 'float32', ('samples', 'z'))
    h_var.long_name = 'MERRA 2 Height Levels'
    h_var.units = 'm'
    h_var.fill_value = 1e+15
    h_var[:] = np.array(data['H'], dtype=np.float32)
    
    s_var = out.createVariable('PHIS', 'float32', ('samples',))
    s_var.long_name = 'MERRA 2 Surface Geopotential'
    s_var.units = 'm2 s-2'
    s_var.fill_value = 1e+15
    s_var[:] = np.array(data['PHIS'], dtype=np.float32)
    
    p_var = out.createVariable('PL', 'float32', ('samples', 'z'))
    p_var.long_name = 'MERRA 2 Pressure at mid-level'
    p_var.units = 'Pa'
    p_var.fill_value = 1e+15
    p_var[:] = np.array(data['PL'], dtype=np.float32)
    
    # Close the output file
    out.close()