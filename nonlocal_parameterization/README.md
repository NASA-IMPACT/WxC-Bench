
# ERA5 Momentum Flux Processing Pipeline

This collection of scripts processes ERA5 reanalysis data to compute and analyze momentum fluxes. The pipeline consists of three main steps:

## 1. Download ERA5 Model Level Data
`download_era5_modellevel_data.py`

Downloads ERA5 model level analysis fields including temperature (T), zonal wind (U), meridional wind (V), and vertical velocity (W) for specified time periods.

**Usage:**
```bash
python download_era5_modellevel_data.py YEAR MONTH [START_DAY END_DAY]
```
- If START_DAY and END_DAY are not provided, processes entire month
- Downloads hourly data at 0.3° resolution
- Outputs NetCDF files to specified directory

## 2. Compute Momentum Fluxes
`compute_momentum_flux_from_era5.py`

Calculates resolved momentum fluxes using Helmholtz decomposition to separate rotational and divergent components.

**Usage:**
```bash
python compute_momentum_flux_from_era5.py YEAR MONTH [START_DAY END_DAY]
```
Key features:
- Computes zonal (uw) and meridional (vw) momentum fluxes
- Uses windspharm for spherical harmonic transformations
- Applies T21 truncation for scale separation
- Outputs hourly NetCDF files with computed fluxes

## 3. Coarse-grain Momentum Fluxes
`coarsegrain_computed_momentum_fluxes.py`

Regrids the high-resolution momentum flux data to a coarser T42 grid and combines with additional derived quantities.

**Usage:**
```bash
python coarsegrain_computed_momentum_fluxes.py YEAR START_MONTH END_MONTH [START_DAY END_DAY]
```
Key features:
- Uses xESMF for conservative regridding
- Computes additional fields like pressure, vertical gradients, and stratification frequency
- Combines resolved and parameterized momentum fluxes
- Outputs comprehensive training dataset in NetCDF format

The final output includes:
- Input fields: u, v, w, temperature, pressure, vertical wind gradients, stratification frequency, surface geopotential
- Output fields: resolved and parameterized momentum fluxes in both zonal and meridional directions