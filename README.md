<!---- Provide an overview of what is being achieved in this repo ----> 


# WxC-Bench


**WxC-Bench** primary goal is to provide a standardized benchmark for evaluating the performance of AI models in Atmospheric and Earth Sciences across various tasks. 

The complete benchmark dataset is available through the Hugging Face platform at [nasa-impact/WxC-Bench](https://huggingface.co/datasets/nasa-impact/WxC-Bench).

## Dataset Details

WxC-Bench contains datasets for six key tasks:
1. **[Nonlocal Parameterization of Gravity Wave Momentum Flux](nonlocal_parameterization/)**
2. **[Prediction of Aviation Turbulence](aviation_turbulence/)**
3. **[Identifying Weather Analogs](weather_analog/)**
4. **[Generation of Natural Language Weather Forecasts](forecast-report-generation/)**
5. **[Long-Term Precipitation Forecasting](long_term_precipitation_forecast/)**
6. **[Hurricane Track and Intensity Prediction](hurricane/)**

### Code Description

## 1. [Nonlocal Parameterization of Gravity Wave Momentum Flux](nonlocal_parameterization/)

This collection of Python scripts processes ERA5 reanalysis data to analyze atmospheric momentum fluxes and their parameterizations. The workflow:

1. Downloads required ERA5 model level data including temperature, wind components (U, V, W), and surface fields from the Climate Data Store (CDS)

2. Computes resolved momentum fluxes using Helmholtz decomposition:
   - Separates wind fields into rotational and divergent components
   - Applies spatial filtering using spherical harmonics
   - Calculates eddy momentum fluxes

3. Processes both resolved and parameterized momentum fluxes:
   - Regrids data from ERA5's native grid to T42 resolution using conservative remapping
   - Computes vertical gradients and stratification
   - Combines analysis fields with parameterized tendencies
   - Outputs processed data in NetCDF format

The code is designed to process ERA5 data efficiently at hourly intervals, with built-in handling for different calendar months and partial month processing. It uses various scientific Python packages including xESMF for regridding, windspharm for spherical harmonics, and netCDF4 for data I/O.

Refer to the [README](nonlocal_parameterization/README.md) file for more details.


## 2. [Generation of Natural Language Weather Forecasts](forecast-report-generation/)


This project provides a tool for downloading and processing textual weather forecast reports from the Storm Prediction Center (SPC). The main functionality includes:

- Scraping weather forecast reports from the SPC website for a specified date range
- Extracting key information such as date, time, and discussion summaries from the reports
- Organizing the extracted data into a structured format
- Saving the processed data as CSV files for further analysis

The script allows users to specify a start and end date for the reports they wish to collect. It then automatically retrieves the relevant HTML pages, parses the content, and extracts the important forecast information. 
Refer to the [README](forecast-report-generation/README.md) file for more details.


## 3. [Long-Term Precipitation Forecasting](long_term_precipitation_forecast/)


This repository contains code and instructions for a long-term precipitation forecast task. The main goal is to predict global daily accumulated precipitation up to 4 weeks in advance using satellite observations. 
More details can be found in the [overview](long_term_precipitation_forecast/OVERVIEW.md) and [readme](long_term_precipitation_forecast/README.md) files.


## 4. [Aviation Turbulence Prediction](aviation_turbulence/)

This codebase processes and analyzes aviation turbulence data from pilot reports (PIREPs) to help predict areas of potential turbulence. The system combines pilot-reported turbulence observations with meteorological data from the MERRA-2 reanalysis dataset to create a machine learning training dataset for turbulence prediction. Here is the workflow:

1. Collecting and processing pilot reports (PIREPs) that contain information about observed turbulence conditions during flights
2. Filtering and categorizing these reports by flight level (low, medium, high altitude)
3. Matching the turbulence reports with corresponding atmospheric conditions from MERRA-2 weather data
4. Creating gridded binary classifications indicating the presence/absence of moderate-or-greater (MOG) turbulence
5. Generating training data that pairs atmospheric profiles with turbulence observations
6. Producing visualization tools to analyze turbulence patterns and risk ratios

The end goal is to create a robust dataset that can be used to train machine learning models to predict aviation turbulence based on atmospheric conditions. 
Refer to the [README](aviation_turbulence/README.md) file for more details.

<!-- - **License:** MIT License -->

## 5. [Hurricane Track and Intensity Prediction](hurricane/)


This collection of Python scripts provides comprehensive tools for analyzing and visualizing Atlantic hurricane data using the HURDAT2 database from the National Hurricane Center. The codebase enables users to:

- Visualize hurricane tracks across the North Atlantic basin with color-coded intensity classifications
- Generate detailed intensity analysis plots showing the evolution of hurricanes through their lifecycle
- Track both maximum sustained wind speeds and minimum sea-level pressure over time
- Display hurricane categories using the Saffir-Simpson scale (from Tropical Depression to Category 5)

The tools access official NOAA hurricane data and can analyze any Atlantic hurricane from 1851 to present.

Refer to the [README](hurricane/README.MD) file for more details.

<!-- - **License:** MIT License -->

## 6. [Weather Analog Search](weather_analog/)

This codebase contains a python script that processes MERRA2 (Modern-Era Retrospective analysis for Research and Applications, Version 2) weather data by extracting specific variables (Sea Level Pressure and 2-meter Temperature) for a defined geographic region over Western Europe for the period 2019-2021 for weather analog search. The script handles daily weather data files, processes them individually, and saves the filtered data in a new format for further analysis. Here is the workflow:

Steps:

 - Sets up directories and defines parameters including date range (2019-2021) and geographic bounds for Western Europe region.
 - Defines function to process individual files by extracting SLP and T2M variables within specified longitude/latitude bounds.
 - Creates output directory and prepares file structure for processed data storage.
 - Main loop iterates through dates, finds corresponding input files, and checks if processing is needed.
 - Processes each file by extracting required variables, applying geographic filters, and saving to new NetCDF format.

Refer to the [README](weather_analog/README.md) file for more details.
<!-- - **License:** MIT License -->

## Citation
**BibTeX:**
```
@misc{shinde2024wxcbenchnoveldatasetweather,
      title={WxC-Bench: A Novel Dataset for Weather and Climate Downstream Tasks}, 
      author={Rajat Shinde and Christopher E. Phillips and Kumar Ankur and Aman Gupta and Simon Pfreundschuh and Sujit Roy and Sheyenne Kirkland and Vishal Gaur and Amy Lin and Aditi Sheshadri and Udaysankar Nair and Manil Maskey and Rahul Ramachandran},
      year={2024},
      eprint={2412.02780},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2412.02780}, 
}
```

## Dataset Card Authors
- Rajat Shinde
- Christopher E. Phillips
- Sujit Roy
- Ankur Kumar
- Aman Gupta
- Simon Pfreundschuh
- Sheyenne Kirkland
- Vishal Gaur
- Amy Lin
- Aditi Sheshadri
- Manil Maskey
- Rahul Ramachandran
## Dataset Card Contact
For each task, please contact:
- **Nonlocal Parameterization of Gravity Wave Momentum Flux:** [Aman Gupta](https://www.github.com/amangupta2)
- **Aviation Turbulence Prediction:** [Christopher E. Phillips](https://www.github.com/sodoesaburningbus)
- **Identifying Weather Analogs:** [Christopher E. Phillips](https://www.github.com/sodoesaburningbus), [Rajat Shinde](https://www.github.com/omshinde)
- **Natural Language Weather Forecasts:** [Rajat Shinde](https://www.github.com/omshinde), [Sujit Roy](https://www.github.com/sujitroymd)
- **Long-Term Precipitation Forecasting:** [Simon Pfreundschuh](https://www.github.com/simonpf)
- **Hurricane Track and Intensity Prediction:** [Ankur Kumar](https://www.github.com/ankurk017)

