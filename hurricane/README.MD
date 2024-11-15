# Hurricane Track and Intensity Analysis

This project analyzes and visualizes hurricane tracks and intensities from the HURDAT2 (Hurricane Database) dataset maintained by the National Hurricane Center (NHC).

## Data Processing

The project uses the HURDAT2 dataset, which contains detailed information about Atlantic hurricanes from 1851 to 2022. The data includes:
- Storm location (latitude/longitude)
- Maximum sustained wind speeds
- Minimum sea level pressure
- Storm category and status

## Features

### 1. Hurricane Track Visualization (`hurricane_track.py`)
- Plots hurricane tracks on a geographic map
- Color-codes track points based on storm intensity
- Supports visualization of both single storms and entire hurricane seasons
- Uses a color scale representing different hurricane categories (TD, TS, Cat 1-5)

### 2. Hurricane Intensity Analysis (`hurricane_intensity.py`)
- Creates time series plots of hurricane intensity metrics
- Displays both maximum sustained wind speed and minimum sea level pressure
- Supports analysis of individual storms with customizable time ranges

## Usage

### Track Visualization
```python
from hurricane.codes.hurricane_track import main

# Visualize all 2017 Atlantic hurricane tracks
main()
```

### Intensity Analysis
```python
from hurricane.codes.hurricane_intensity import plot_intensity

# Analyze specific hurricanes
plot_intensity(name='harvey', year=2017, start=2)
plot_intensity(name='laura', year=2020, start=2)
```


## Data Source
The hurricane data is sourced from the NHC's HURDAT2 database:
```
https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-042723.txt
```
